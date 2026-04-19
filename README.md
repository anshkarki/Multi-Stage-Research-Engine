<h1 align="center"><b>🔬 Multi-Stage Research Engine</b></h2>

A multi-agent AI system that automates the complete research workflow - from web search to structured report generation and evaluation.
<div align="center">

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agents-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![OpenAI](https://img.shields.io/badge/GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Tavily](https://img.shields.io/badge/Tavily-Search-0EA5E9?style=for-the-badge&logo=googlechrome&logoColor=white)](https://tavily.com)

<br/>

> **Drop a topic. Get a full research report — automatically.**  
> A 4-agent AI pipeline that searches the web, reads sources, writes a structured report, and critiques it. No hand-holding required.

<br/>

</div>

---

## ⚡ What It Does

```
You type a topic → AI does the rest
```

| Step | Agent | What happens |
|------|-------|-------------|
| 🔍 **01** | Search Agent | Queries Tavily for the 5 most relevant web results |
| 📖 **02** | Reader Agent | Picks the best URL and scrapes its full content |
| ✍️ **03** | Writer Chain | Drafts an Introduction → Key Findings → Conclusion report |
| 🧐 **04** | Critic Chain | Reviews and scores the report out of 10 with feedback |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────┐
│                      ResearchAI                      │
│                                                      │
│   Topic Input                                        │
│       │                                              │
│       ▼                                              │
│  ┌─────────────┐    Tavily API    ┌───────────────┐  │
│  │ Search Agent│ ─────────────►   │  Web Results  │  │
│  └─────────────┘                  └─────┬─────────┘  │
│                                         │            │
│       ┌─────────────────────────────────┘            │
│       ▼                                              │
│  ┌─────────────┐   BeautifulSoup  ┌───────────────┐  │
│  │ Reader Agent│ ─────────────►   │ Scraped Text  │  │
│  └─────────────┘                  └─────┬─────────┘  │
│                                         │            │
│       ┌─────────────────────────────────┘            │
│       ▼                                              │
│  ┌─────────────┐    GPT-4o-mini   ┌───────────────┐  │
│  │Writer Chain │ ─────────────►   │Final Report   │  │
│  └─────────────┘                  └─────┬─────────┘  │
│                                         │            │
│       ┌─────────────────────────────────┘            │
│       ▼                                              │
│  ┌─────────────┐    GPT-4o-mini   ┌───────────────┐  │
│  │ Critic Chain│ ─────────────►   │Score + Notes  │  │
│  └─────────────┘                  └───────────────┘  │
└──────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```bash
researchai/
│
├── 📄 app.py              # Streamlit UI — run this
├── 🔁 pipeline.py         # CLI orchestration & pipeline logic
├── 🤖 agents.py           # LangGraph agents + writer/critic chains
├── 🛠️  tools.py            # web_search (Tavily) & scrape_url (BS4) tools
├── 📦 requirements.txt    # All dependencies
└── 🔐 .env                # Your API keys (never commit this)
```

---

## 🚀 Quick Start

### 1️⃣ Clone the repo

```bash
git clone https://github.com/your-username/researchai.git
cd researchai
```

### 2️⃣ Create & activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3️⃣ Install all dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up your `.env` file

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxx
```

<details>
<summary>🔑 Where to get your API keys</summary>

<br/>

| Key | Link |
|-----|------|
| `OPENAI_API_KEY` | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| `TAVILY_API_KEY` | [app.tavily.com](https://app.tavily.com) |

</details>

---

## ▶️ Run the App

### 🖥️ Streamlit UI *(recommended)*

```bash
streamlit run app.py
```

Open **[http://localhost:8501](http://localhost:8501)** in your browser. Type a topic, hit **Run Research** and watch the pipeline execute step by step.

### 💻 CLI Mode

```bash
python pipeline.py
```

```
Enter a research topic: Impact of AI on healthcare
```

All 4 steps will print live to your terminal.

---

## 📋 Sample Report Output

```
📌 INTRODUCTION
───────────────
Artificial intelligence is transforming healthcare through ...

🔍 KEY FINDINGS
────────────────
1. Diagnostic accuracy improved by up to 94% using deep learning models ...
2. AI-powered drug discovery is reducing R&D timelines from years to months ...
3. Remote patient monitoring systems are cutting hospital readmissions by ...

✅ CONCLUSION
─────────────
The integration of AI into healthcare represents a paradigm shift ...

🔗 SOURCES
───────────
• https://www.nejm.org/ai-healthcare-2024
• https://www.who.int/news/ai-diagnostics
```

---

## 🧑‍💻 Tech Stack

<div align="center">

| | Technology | Role |
|--|-----------|------|
| 🧠 | GPT-4o-mini | LLM powering all agents and chains |
| 🕸️ | LangGraph | ReAct agent framework |
| 🔗 | LangChain | Prompt templates, output parsers |
| 🔍 | Tavily | Real-time web search API |
| 🍜 | BeautifulSoup4 | Web scraping & HTML parsing |
| 🖥️ | Streamlit | Frontend UI |
| 🔐 | python-dotenv | Environment variable management |

</div>

---

## 🔒 Security Reminder

Add this to your `.gitignore` before your first commit:

```gitignore
# Secrets
.env

# Python
.venv/
__pycache__/
*.pyc
*.pyo
.DS_Store
```

---

## 🗺️ Roadmap

- [x] Multi-agent search → scrape → write → critique pipeline
- [x] Streamlit UI with step-by-step progress
- [x] Downloadable report output
- [x] PDF export of the final report
- [ ] Support for multiple URLs scraped in parallel
- [ ] Memory across sessions for recurring research topics
- [ ] Switch between GPT-4o / Claude / Gemini via UI toggle

---

## 📄 License

```
MIT License — free to use, modify, and distribute.
Give credit if you build something cool with it 🙌
```

---

<div align="center">

Made with 🤖 + ☕ &nbsp;|&nbsp; Star ⭐ the repo if it saved you hours of manual research

</div>
