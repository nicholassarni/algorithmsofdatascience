# Streamlit Cloud Deployment Guide

## Quick Deployment to Streamlit Community Cloud

Follow these steps to deploy your TinyTroupe Customer Service Agents app:

### Step 1: Sign in to Streamlit Community Cloud

1. Go to https://share.streamlit.io/
2. Sign in with your GitHub account (nicholassarni)

### Step 2: Deploy New App

1. Click **"New app"** button
2. Fill in the deployment settings:
   - **Repository**: `nicholassarni/algorithmsofdatascience`
   - **Branch**: `main`
   - **Main file path**: `Project2/streamlit_app.py`
   - **App URL** (optional): Choose a custom subdomain like `tinytroupe-agents`

### Step 3: Configure Secrets

Before clicking "Deploy", you need to add your OpenAI API key:

1. Click on **"Advanced settings"**
2. In the **Secrets** section, add the following:

```toml
OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
```

3. Click **"Save"**

### Step 4: Deploy!

1. Click **"Deploy!"**
2. Wait for the app to build and deploy (this may take 3-5 minutes on first deployment)
3. Your app will be live at: `https://[your-app-name].streamlit.app`

## Accessing Your Live App

Once deployed, your app will be accessible at a URL like:
- `https://tinytroupe-agents.streamlit.app` (if you chose this custom name)
- OR `https://algorithmsofdatascience-project2.streamlit.app` (default)

## Updating Your App

Whenever you push changes to the `main` branch in GitHub, Streamlit Cloud will automatically redeploy your app!

## Troubleshooting

### If the app fails to start:

1. **Check the logs** in Streamlit Cloud dashboard
2. **Verify your OpenAI API key** is correctly set in Secrets
3. **Ensure all dependencies** in `requirements.txt` are installing correctly

### Common Issues:

- **Import errors**: Make sure all required packages are in `requirements.txt`
- **API key not found**: Double-check the Secrets configuration
- **Agent files not found**: Ensure the `agents/` folder is committed to GitHub

## Local Testing Before Deployment

To test locally before deploying:

```bash
cd C:\Users\nicho\algorithmsofdatascience\Project2
uv run streamlit run streamlit_app.py
```

Access at: http://localhost:8501

## Support

For Streamlit Cloud issues, visit: https://docs.streamlit.io/streamlit-community-cloud
