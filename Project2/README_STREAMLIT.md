# TinyTroupe Customer Service Agents - Streamlit App

An interactive web application where you can chat with AI customer service agents powered by TinyTroupe.

## Features

- **Two Unique Agents:**
  - **Sunny Martinez**: Enthusiastic, warm, and optimistic customer service representative
  - **Alex Chen**: Efficient, professional, and systematic customer service representative

- **Interactive Chat**: Ask questions and receive personalized responses based on each agent's unique personality
- **Conversation History**: Track your conversation throughout the session
- **Agent Profiles**: View detailed information about each agent's personality and strengths

## Running Locally

1. Clone this repository
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Deployment on Streamlit Community Cloud

This app is configured to run on Streamlit Community Cloud. You'll need to add your `OPENAI_API_KEY` to the Secrets section in your Streamlit Cloud deployment settings.

## About the Agents

The agents are defined in JSON files located in the `agents/` directory:
- `sunny.agent.json` - Sunny Martinez's personality specification
- `alex.agent.json` - Alex Chen's personality specification

These specifications define each agent's personality traits, communication style, skills, and behavioral patterns.
