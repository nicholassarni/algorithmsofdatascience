# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is Project1 from an Algorithms of Data Science course. The project focuses on credibility assessment of online news articles using rule-based scoring algorithms and web scraping techniques.

## Core Components

### 1. Article Credibility Scoring System (`AlgOfDataScience,_Deliverable_1.ipynb`)

This notebook contains a comprehensive credibility assessment system for evaluating online news articles. The system is entirely self-contained in a single Python script that can be run independently.

**Main Functions:**
- `score_articles(articles, weights=None)` - Core scoring engine that evaluates article credibility based on multiple factors
- `extract_article_features_from_url(url)` - Web scraper that automatically extracts features from article HTML
- `score_articles_from_urls(urls)` - Convenience function that combines extraction and scoring

**Scoring Components (with default weights):**
- Domain reputation (23%) - TLD analysis (.gov/.edu trusted, .zip/.click suspect), outlet type classification
- Evidence (22%) - Citation counts, links to primary sources, expert quotes
- Transparency (18%) - Bylines, about pages, contact info, corrections policy
- Quality (15%) - Ad density, stock images, press release detection
- Recency (12%) - Publication/update date analysis
- Objectivity (10%) - Subjectivity scores, polarity, opinion markers

**Penalties Applied:**
- Clickbait patterns (e.g., "you won't believe", "shocking", excessive exclamation marks)
- Paywalled content
- Excessive sensationalism

**Output Format:**
Each scored article returns:
- `credibility_score_0_100` - Overall credibility (0-100 scale)
- `objectivity_stars_0_5` - Objectivity rating (0-5 stars)
- `overall_stars_0_5` - Combined overall rating (0-5 stars)
- `rationale` - String explanation of component scores
- `breakdown` - Dictionary with individual component scores

### 2. Technical Documentation (`AlgOfDataScience,_Deliverable_2`)

Contains detailed algorithmic analysis including:
- Scientific justification for feature selection
- Literature review of fact-checking and credibility models
- Methodology validation with empirical examples
- API usage documentation
- Future improvement suggestions (NLP embeddings, social metrics, adaptive weighting)

### 3. Feature Analysis Session (`AlgorithimDataScience,_Session_1.ipynb`)

Contains exploratory data analysis work on California housing dataset using:
- Linear regression modeling
- Feature importance analysis (SelectKBest with f_regression, Random Forest)
- Visualization of feature relationships
- Model performance evaluation (RMSE, R²)

## Development Environment

**Dependencies:**
```python
# Standard library
import math, re, sys
from urllib.parse import urlparse, urljoin
from datetime import datetime, timezone

# External packages (install via pip)
import requests
import beautifulsoup4  # imported as 'from bs4 import BeautifulSoup'

# For Session 1 notebook
import pandas
import numpy
import scikit-learn
import matplotlib
import seaborn
```

**Installation:**
```bash
pip install requests beautifulsoup4 pandas numpy scikit-learn matplotlib seaborn
```

## Running the Code

### Credibility Assessment System

To test a single URL:
```python
from AlgOfDataScience_Deliverable_1 import score_articles_from_urls

url = "https://apnews.com/article/example"
result = score_articles_from_urls(url)[0]

print("Credibility:", result["credibility_score_0_100"])
print("Objectivity:", result["objectivity_stars_0_5"])
print("Overall:", result["overall_stars_0_5"])
print("Rationale:", result["rationale"])
```

To score multiple URLs:
```python
urls = [
    "https://www.university.edu/news/study",
    "https://apnews.com/article/example"
]
results = score_articles_from_urls(urls)
```

### Jupyter Notebooks

Open and run in Jupyter:
```bash
jupyter notebook AlgOfDataScience,_Deliverable_1.ipynb
```

Or execute cells directly in compatible environments (Google Colab, VS Code, etc.)

## Architecture Notes

### Web Scraping Strategy

The system uses a multi-pronged approach to extract article features:
1. **Meta tag extraction** - OpenGraph, Schema.org, standard meta tags for dates/authors
2. **Structural analysis** - BeautifulSoup parsing of semantic HTML elements (footer, nav, time tags)
3. **Text pattern matching** - Regex-based detection of bylines, contact info, corrections policies
4. **Link analysis** - Outbound link counting with primary source detection (.gov, .edu, DOI, PubMed)
5. **Content quality heuristics** - Ad container detection, iframe counting, stock image indicators

### Error Handling

The `extract_article_features_from_url()` function includes fallback behavior:
- Network failures return minimal dict with URL and domain only
- Missing features default to None (scorer handles gracefully)
- 12-second timeout prevents hanging on slow sites

### Customization Points

Weights can be customized when calling `score_articles()`:
```python
custom_weights = {
    "domain": 0.30,      # Increase domain importance
    "evidence": 0.25,    # Increase evidence importance
    "transparency": 0.15,
    "quality": 0.12,
    "recency": 0.10,
    "objectivity": 0.08
}
results = score_articles(articles, weights=custom_weights)
```

## Important Implementation Details

1. **Date Parsing** - Handles multiple formats (ISO 8601, common date formats) with timezone awareness
2. **Domain Classification** - TLD-based (.gov/.edu) plus outlet type hints for universities/journals vs blogs/social
3. **Evidence Scoring** - Uses exponential decay formula `1 - exp(-k * count)` to normalize citation counts
4. **Clickbait Detection** - Pattern matching for common clickbait phrases plus punctuation analysis
5. **Named Expert Detection** - Identifies quotes containing Dr./Prof./PhD/MD markers

## Known Limitations

- HTML parsing depends on site structure (may miss features on non-standard layouts)
- No JavaScript rendering (won't capture dynamically loaded content)
- Heuristic-based (not ML-trained, may miss nuanced signals)
- English-centric pattern matching for clickbait/opinion detection
- No integration with external fact-checking databases
