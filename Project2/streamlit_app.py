"""
Streamlit App for TinyTroupe Customer Service Agents
====================================================

This app allows users to interact with AI customer service personas:
- Sunny Martinez: Enthusiastic and warm customer service rep
- Alex Chen: Efficient and professional customer service rep

Users can ask questions and receive responses based on each agent's unique personality.
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Import tinytroupe - will be installed via requirements.txt
import tinytroupe
from tinytroupe.agent import TinyPerson

# Load environment variables - works both locally and on Streamlit Cloud
if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
    # Running on Streamlit Cloud with secrets
    os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
else:
    # Running locally with .env file
    load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Customer Service AI Agents",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if 'agents_loaded' not in st.session_state:
    st.session_state.agents_loaded = False
    st.session_state.sunny = None
    st.session_state.alex = None


@st.cache_resource
def load_agents():
    """Load the customer service agent personas from JSON specifications."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    agents_dir = os.path.join(script_dir, "agents")

    # Load agents using absolute paths
    sunny = TinyPerson.load_specification(os.path.join(agents_dir, "sunny.agent.json"))
    alex = TinyPerson.load_specification(os.path.join(agents_dir, "alex.agent.json"))
    return sunny, alex


def get_agent_response(agent, question):
    """
    Get a response from the specified agent based on the user's question.

    Args:
        agent: TinyPerson agent object
        question: User's question string

    Returns:
        str: Agent's response
    """
    try:
        # Use listen_and_act which combines both operations
        agent.listen_and_act(question)

        # Get the response from the agent's current interactions
        interactions = agent.pretty_current_interactions(last_n=1, simplified=True)

        if interactions:
            # Clean up the output by removing simulation metadata
            lines = interactions.split('\n')
            clean_lines = []

            skip_markers = [
                '****',
                'BEGIN SIMULATION',
                'END SIMULATION',
                'TRAJECTORY',
                'Agent simulation',
                '[CURRENT INTERACTION]',
                'Date',
                'Event #'
            ]

            for line in lines:
                # Skip lines with metadata markers
                if any(marker in line for marker in skip_markers):
                    continue

                # Skip empty lines
                if not line.strip():
                    continue

                # Keep lines that look like agent speech/actions
                if line.strip():
                    clean_lines.append(line.strip())

            # Join the clean lines
            if clean_lines:
                response = '\n'.join(clean_lines)
                # Additional cleanup
                response = response.replace('TALK:', '').replace('SAY:', '').replace('SAID:', '')
                response = response.strip()

                if response:
                    return response

        return "I apologize, but I couldn't generate a response. Please make sure the OpenAI API is responding correctly."

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"Error: {str(e)}"


def display_agent_info(agent_name):
    """Display information about the selected agent's personality."""

    agent_info = {
        "Sunny Martinez": {
            "emoji": "😊",
            "title": "Customer Service Representative",
            "personality": "Enthusiastic, warm, and optimistic",
            "style": "Warm, bubbly, and genuinely enthusiastic",
            "strengths": [
                "Making customers feel valued and heard",
                "De-escalating tense situations with positivity",
                "Creating personal connections"
            ],
            "best_for": "General inquiries, emotional support, building rapport"
        },
        "Alex Chen": {
            "emoji": "💼",
            "title": "Senior Customer Service Representative",
            "personality": "Efficient, professional, and systematic",
            "style": "Professional, direct, and clear",
            "strengths": [
                "Technical troubleshooting",
                "Systematic problem-solving",
                "Clear and concise communication"
            ],
            "best_for": "Technical issues, process questions, detailed solutions"
        }
    }

    if agent_name in agent_info:
        info = agent_info[agent_name]
        st.sidebar.markdown(f"### {info['emoji']} {agent_name}")
        st.sidebar.markdown(f"**Role:** {info['title']}")
        st.sidebar.markdown(f"**Personality:** {info['personality']}")
        st.sidebar.markdown(f"**Communication Style:** {info['style']}")
        st.sidebar.markdown("**Strengths:**")
        for strength in info['strengths']:
            st.sidebar.markdown(f"- {strength}")
        st.sidebar.markdown(f"**Best for:** {info['best_for']}")


def main():
    """Main Streamlit app function."""

    # App title and description
    st.title("🤖 Customer Service AI Agents")
    st.markdown("""
    Welcome! Chat with our AI customer service agents. Each agent has a unique personality
    and communication style designed to help you with different types of questions.
    """)

    # Load agents
    if not st.session_state.agents_loaded:
        with st.spinner("Loading AI agents..."):
            try:
                st.session_state.sunny, st.session_state.alex = load_agents()
                st.session_state.agents_loaded = True
            except Exception as e:
                st.error(f"Error loading agents: {str(e)}")
                st.stop()

    # Sidebar - Agent selection and info
    st.sidebar.title("Select an Agent")

    agent_choice = st.sidebar.radio(
        "Choose who you'd like to talk to:",
        ["Sunny Martinez", "Alex Chen"],
        help="Each agent has a different personality and approach to customer service"
    )

    st.sidebar.markdown("---")
    display_agent_info(agent_choice)

    # Get the selected agent
    current_agent = st.session_state.sunny if agent_choice == "Sunny Martinez" else st.session_state.alex

    # Main chat interface
    st.markdown("---")
    st.subheader(f"💬 Chat with {agent_choice}")

    # Display conversation history
    if st.session_state.conversation_history:
        for entry in st.session_state.conversation_history:
            if entry['type'] == 'user':
                st.markdown(f"**You:** {entry['message']}")
            else:
                st.markdown(f"**{entry['agent']}:** {entry['message']}")
            st.markdown("")

    # Clear conversation button
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.conversation_history = []
            st.rerun()

    # User input
    st.markdown("---")
    with st.form(key='question_form', clear_on_submit=True):
        user_question = st.text_area(
            "Ask a question:",
            placeholder="Type your question here...",
            height=100,
            key='user_input'
        )

        submit_button = st.form_submit_button("Send", use_container_width=True)

        if submit_button and user_question.strip():
            # Add user question to history
            st.session_state.conversation_history.append({
                'type': 'user',
                'message': user_question
            })

            # Get agent response
            with st.spinner(f"{agent_choice} is typing..."):
                try:
                    response = get_agent_response(current_agent, user_question)

                    # Add agent response to history
                    st.session_state.conversation_history.append({
                        'type': 'agent',
                        'agent': agent_choice,
                        'message': response
                    })

                except Exception as e:
                    st.error(f"Error getting response: {str(e)}")

            # Rerun to update the chat display
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
    Powered by TinyTroupe | AI-generated personas with unique personalities
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
