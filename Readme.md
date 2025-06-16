# HealthBot: AI-Powered Patient Education System

A prototype command-line chatbot that helps patients learn about medical topics on demand. HealthBot uses:

- **Tavily** to fetch up-to-date web content on any health topic.
- **OpenAI (gpt-4)** via the LangChain Community wrapper to summarize and quiz.
- **LangGraph** to orchestrate the workflow as a directed graph of “nodes” and shared state.

---

## Table of Contents

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
4. [Configuration](#configuration)  
5. [Usage](#usage)  
6. [How It Works](#how-it-works)  
7. [Project Structure](#project-structure)  
8. [Customization & Extensions](#customization--extensions)  
9. [Contributing](#contributing)  
10. [License](#license)  

---

## Features

- **Topic Exploration**: Ask about any health condition or medical topic.  
- **Automated Search**: Pulls top 5 results from Tavily’s web search.  
- **Patient-Friendly Summaries**: Generates a concise 3–4 paragraph explanation.  
- **Interactive Quiz**: Creates a single comprehension question based strictly on the summary.  
- **Automated Grading**: Grades the patient’s answer (A–F) with citations back to the summary.  
- **Session Loop**: Option to learn another topic without losing context or leaking data.

---

## Prerequisites

- Python **3.8+**  
- A free [Tavily](https://tavily.com/) account and API key  
- An OpenAI API key with GPT-4 access  
- `pip` for installing Python packages  

---

## Installation

1. **Clone this repository**  
   ```bash
   git clone https://github.com/saijithendr/healthbot.git
   cd healthbot

2. Create & activate a virtual environment

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
3. Install dependencies
    ```bash
    pip install --upgrade pip
    pip install \
    langchain==0.2.16 \
    langchain_community==0.1.23 \
    langgraph==0.2.19 \
    tavily-python==0.4.0 \
    python-dotenv
4. **Configuration**
Create a .env file in the project root with your API keys:
    ```bash
    OPENAI_API_KEY="sk-********************************"
    TAVILY_API_KEY="tvly-********************************"
    ```

# Usage

Run the main script:

```
python HealthBot.py
```
* Enter a health topic when prompted.

* Read the generated summary.

* Press Enter to trigger a short quiz.

* Answer the quiz question.

* See your grade & feedback.

* Choose to learn another topic or exit