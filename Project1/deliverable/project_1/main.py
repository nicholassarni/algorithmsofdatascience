import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from ddgs import DDGS
import warnings
import math
import re
from urllib.parse import urlparse, urljoin
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup

warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

st.title("GPT Chatbot with Credibility-Rated Web Search 🔍⭐")

# Initialize the OpenAI client
api_key = os.getenv("OPENAI_API_KEY")

if not api_key or api_key == "your_openai_api_key_here":
    st.error("Please set your OPENAI_API_KEY in the .env file")
    st.info("Get your API key from: https://platform.openai.com/api-keys")
    st.stop()

client = OpenAI(api_key=api_key)

# Add web search toggle in sidebar
with st.sidebar:
    st.header("Settings")
    enable_search = st.toggle("Enable Web Search", value=True)
    force_search = st.checkbox("Force search on ALL queries", value=True)

    if enable_search:
        st.success("🔍 Web search is ENABLED")
        st.caption("Auto-detects when to search based on keywords")
    else:
        st.info("Web search is disabled")

    if force_search:
        st.warning("⚡ Forcing search on EVERY message")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# =============================================================================
# ARTICLE CREDIBILITY SCORING SYSTEM (from Deliverable 1)
# =============================================================================

def score_article_credibility(url):
    """Score a single article URL for credibility. Returns dict with scores."""
    try:
        article_data = extract_article_features(url)
        scores = score_articles([article_data])[0]
        return scores
    except Exception:
        return None

def extract_article_features(url):
    """Extract features from URL for credibility scoring."""
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.content, 'html.parser')
        domain = urlparse(url).netloc

        # Title
        title = soup.title.string.strip() if soup.title else url

        # Date
        published_at = None
        for tag in soup.find_all(['meta', 'time']):
            for attr in ['content', 'datetime']:
                if tag.has_attr(attr):
                    val = tag.get(attr)
                    if val and ('20' in str(val) or 'T' in str(val)):
                        published_at = val
                        break
            if published_at:
                break

        # Evidence signals
        cites_count = 0
        primary_count = 0
        for a in soup.find_all("a", href=True):
            href = a["href"]
            link_domain = urlparse(href).netloc
            if link_domain and domain not in link_domain:
                cites_count += 1
                if any(p in href.lower() for p in ['.gov', '.edu', 'doi.org', 'pubmed']):
                    primary_count += 1

        # Transparency
        has_byline = bool(soup.find(attrs={"name": "author"}) or soup.find("meta", {"property": "article:author"}))
        text = soup.get_text(" ", strip=True).lower()
        has_contact = any(k in text for k in ["contact", "email"])
        has_about = any('about' in (a.get_text() or '').lower() for a in soup.find_all("a"))

        # Quality
        ads_density = min(1.0, len(soup.find_all("iframe")) / 10)

        # Clickbait
        clickbait_score = 0.0
        if title:
            title_l = title.lower()
            if any(p in title_l for p in ['shocking', 'you won', 'what happened']):
                clickbait_score = 0.5
            clickbait_score += min(0.5, title.count('!') * 0.1)

        return {
            "title": title,
            "url": url,
            "domain": domain,
            "outlet_type": "gov" if domain.endswith('.gov') else ("university" if domain.endswith('.edu') else None),
            "published_at": published_at,
            "has_byline": has_byline,
            "has_about_page": has_about,
            "has_contact_info": has_contact,
            "cites_sources_count": cites_count,
            "links_to_primary_sources": primary_count,
            "advertising_density": ads_density,
            "clickbait_score": clickbait_score,
        }
    except Exception:
        return {"title": url, "url": url, "domain": urlparse(url).netloc}

def score_articles(articles, weights=None):
    """Score articles for credibility (simplified from Deliverable 1)."""
    W = weights or {"domain": 0.23, "evidence": 0.22, "transparency": 0.18,
                    "quality": 0.15, "recency": 0.12, "objectivity": 0.10}

    TRUSTED_TLDS = (".gov", ".edu")
    SUSPECT_TLDS = (".zip", ".top", ".click")

    results = []
    for a in articles:
        # Domain score
        domain = (a.get("domain") or "").lower()
        domain_score = 0.5
        if any(domain.endswith(t) for t in TRUSTED_TLDS):
            domain_score = 0.85
        if any(domain.endswith(t) for t in SUSPECT_TLDS):
            domain_score = 0.35
        if a.get("outlet_type") in ("university", "gov"):
            domain_score = max(domain_score, 0.9)

        # Evidence score
        cites = a.get("cites_sources_count") or 0
        primary = a.get("links_to_primary_sources") or 0
        evidence_score = (1 - math.exp(-cites/4)) * 0.6 + (1 - math.exp(-primary/2)) * 0.4

        # Transparency score
        transp_score = 0.3
        if a.get("has_byline"):
            transp_score += 0.25
        if a.get("has_about_page"):
            transp_score += 0.2
        if a.get("has_contact_info"):
            transp_score += 0.15
        transp_score = min(1.0, transp_score)

        # Quality score
        quality_score = 0.7
        ads = a.get("advertising_density") or 0
        quality_score -= min(0.5, ads * 0.6)
        quality_score = max(0.0, quality_score)

        # Recency score (simplified)
        recency_score = 0.5  # Default neutral if no date

        # Objectivity score
        obj_score = 0.7

        # Penalties
        penalty = min(0.5, (a.get("clickbait_score") or 0) * 0.15)

        # Final credibility
        cred_0_1 = (W["domain"]*domain_score + W["evidence"]*evidence_score +
                    W["transparency"]*transp_score + W["quality"]*quality_score +
                    W["recency"]*recency_score + W["objectivity"]*obj_score)
        cred_0_1 = max(0.0, min(1.0, cred_0_1 - penalty))

        credibility_score = round(cred_0_1 * 100, 1)
        overall_stars = round(cred_0_1 * 5, 1)

        results.append({
            "title": a.get("title"),
            "url": a.get("url"),
            "credibility_score_0_100": credibility_score,
            "overall_stars_0_5": overall_stars,
            "breakdown": {
                "domain": round(domain_score, 2),
                "evidence": round(evidence_score, 2),
                "transparency": round(transp_score, 2),
                "quality": round(quality_score, 2),
            }
        })
    return results

# Function to fetch article content
def fetch_article_content(url, timeout=10):
    """Fetch and extract main content from a URL"""
    try:
        import requests
        from bs4 import BeautifulSoup

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()

        # Get text from common article containers
        article_text = ""
        for tag in ['article', 'main', 'div[class*="content"]', 'div[class*="article"]']:
            content = soup.select_one(tag)
            if content:
                article_text = content.get_text(separator='\n', strip=True)
                break

        if not article_text:
            article_text = soup.get_text(separator='\n', strip=True)

        # Limit to first 3000 characters to avoid token limits
        return article_text[:3000] if article_text else None
    except Exception:
        return None

# Function to perform web search
def web_search(query, max_results=3):
    """Search the web using DuckDuckGo and fetch article content with credibility scores"""
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return None

        search_summary = ""
        for i, result in enumerate(results, 1):
            url = result['href']

            search_summary += f"[Source {i}] {result['title']}\n"
            search_summary += f"Summary: {result['body']}\n"
            search_summary += f"URL: {url}\n"

            # Score credibility
            cred_score = score_article_credibility(url)
            if cred_score:
                stars = "⭐" * int(cred_score['overall_stars_0_5'])
                search_summary += f"Credibility: {cred_score['credibility_score_0_100']}/100 {stars}\n"
                breakdown = cred_score['breakdown']
                search_summary += f"Quality Breakdown: Domain={breakdown['domain']}, Evidence={breakdown['evidence']}, Transparency={breakdown['transparency']}, Quality={breakdown['quality']}\n"

            # Fetch actual article content
            article_content = fetch_article_content(url)
            if article_content:
                search_summary += f"Full Content:\n{article_content}\n"

            search_summary += "\n"

        return search_summary
    except Exception as e:
        st.warning(f"Search failed: {str(e)}")
        return None

# Function to determine if web search is needed
def needs_web_search(prompt):
    """Check if the query might benefit from web search"""
    # More comprehensive keyword list
    search_keywords = [
        "latest", "current", "news", "today", "recent", "2024", "2025",
        "what is happening", "what's happening", "what is", "what's",
        "search", "find", "look up", "weather", "temperature", "forecast",
        "stock", "price", "score", "update", "now", "right now",
        "this week", "this month", "this year", "recently", "tell me about",
        "information about", "nyc", "new york"
    ]
    prompt_lower = prompt.lower()
    # Return True if ANY keyword is found
    has_keyword = any(keyword in prompt_lower for keyword in search_keywords)

    # Also search if the query is a question (ends with ?)
    is_question = "?" in prompt

    return has_keyword or is_question

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to talk about?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check if web search is needed and enabled
    search_results = None
    should_search = force_search or needs_web_search(prompt)

    if enable_search and should_search:
        with st.spinner("🔍 Searching..."):
            search_results = web_search(prompt)

    # Prepare messages for OpenAI - build the API messages fresh each time
    messages_for_api = []

    # Add system message with search results if available
    if search_results:
        system_prompt = f"""CRITICAL INSTRUCTIONS - READ CAREFULLY:

The user asked: "{prompt}"

I have performed a LIVE INTERNET SEARCH and retrieved the following CURRENT, UP-TO-DATE information:

=== WEB SEARCH RESULTS ===
{search_results}
=== END OF SEARCH RESULTS ===

YOUR TASK:
1. Read and COMPREHEND the content from the search results above
2. SYNTHESIZE the information and provide a comprehensive answer based on the actual content
3. Structure your response for maximum clarity and readability:
   - Use short paragraphs (2-3 sentences max)
   - Use bullet points or numbered lists when presenting multiple items
   - Use bold text (**text**) for key terms and important information
   - Add spacing between sections for better visual flow
4. DO NOT mention credibility scores in your main answer - they will be shown separately
5. After your main answer, add a "**Sources & Credibility Ratings:**" section
6. Format each source as:
   ```
   **[Source Number]: [Source Title]**
   - URL: [URL]
   - Credibility Score: [X]/100 [star rating]
   - Quality Breakdown: Domain=[X], Evidence=[X], Transparency=[X], Quality=[X]
   ```
7. DO NOT say "I don't have access to real-time information" or "I cannot browse the internet"
8. You MUST extract and summarize the actual CONTENT from the search results

FORMATTING REQUIREMENTS:
- Start with a clear, direct answer to the question
- Break complex information into digestible chunks
- Use markdown formatting (bold, bullets, etc.) to improve readability
- DO NOT mention credibility in your main answer
- End with a detailed "**Sources & Credibility Ratings:**" section showing all ratings"""
        messages_for_api.append({"role": "system", "content": system_prompt})

    # Add only the LAST user message (not full history when we have search results)
    # This prevents the AI from seeing its own previous "I don't have internet" responses
    if search_results:
        messages_for_api.append({"role": "user", "content": prompt})
    else:
        # No search results, use full conversation history
        for msg in st.session_state.messages:
            messages_for_api.append({"role": msg["role"], "content": msg["content"]})

    # Call OpenAI API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Create the message with streaming
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_for_api,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant response to chat history (without the system message)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
