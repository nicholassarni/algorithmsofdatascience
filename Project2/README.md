# Project 2 - TinyTroupe Example

This project demonstrates the use of Microsoft's TinyTroupe library to create AI-powered agent simulations.

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/nicholassarni/algorithmsofdatascience.git
cd algorithmsofdatascience/Project2
```

### 2. Install dependencies

This project uses `uv` for dependency management. If you don't have it installed:
```bash
pip install uv
```

Then install the project dependencies:
```bash
uv sync
```

### 3. Install TinyTroupe

TinyTroupe must be installed from GitHub (not PyPI):
```bash
# Clone TinyTroupe to a shorter path to avoid Windows path length issues
cd C:\Users\[YourUsername]
git clone https://github.com/microsoft/tinytroupe.git

# Install TinyTroupe in editable mode
cd [back-to-project2]
uv pip install -e C:\Users\[YourUsername]\tinytroupe
```

### 4. Set up your OpenAI API key

1. Get an API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and replace `your-api-key-here` with your actual OpenAI API key

**⚠️ IMPORTANT:** Never commit your `.env` file to GitHub! It's already in `.gitignore` to protect your API key.

### 5. Run the example

```bash
uv run main.py
```

## What This Does

The script creates "Lisa the Data Scientist," an AI agent with a defined persona, and asks her to talk about her life. The agent will respond based on her personality, background, and interests defined in TinyTroupe's examples.

## Project Structure

- `main.py` - Main script demonstrating TinyTroupe usage
- `.env` - Your environment variables (not committed to git)
- `.env.example` - Template for environment variables
- `pyproject.toml` - Project dependencies
- `.gitignore` - Files to exclude from git

## Learn More

- [TinyTroupe GitHub](https://github.com/microsoft/tinytroupe)
- [OpenAI API Documentation](https://platform.openai.com/docs)
