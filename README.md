# X_automation


This project is an **AI-powered system that automatically generates Twitter posts** in the style of any given Twitter user — just give it a username and a topic!

Inspired by Miguel Otero Pedrido's CrewAI-based LinkedIn automation, this implementation uses **[Agno](https://github.com/agnodice/agno)** — a lightweight, modular framework for building multimodal AI agents — to build an intelligent tweeting agent.

## ✨ What It Does

Given a **Twitter username** and a **topic**, the system will:

1. **Scrape tweets** from the user to understand their tone, style, and language.
2. **Research trending info** on your selected topic.
3. **Generate a new tweet** using the user's style and the latest insights!

---

## 🧠 How It Works

### Agent Architecture (Using Agno)

- **Twitter Scraper Agent**
  - Scrapes the latest tweets from a user's public Twitter profile
  - Learns their tone, writing style, and common phrases

- **Web Researcher Agent**
  - Uses online search tools to collect recent, relevant information on your given topic

- **Doppelgänger Agent**
  - Uses insights from the above agents to generate tweets that look and feel like they're from the selected user

All agents are powered by Groq-hosted LLMs (e.g., LLaMA 3, Gemma 2).

---

## Project structure

.
├── agents.py          # Defines the three AI agents (scraper, researcher, creator)
├── main.py            # Entry point, runs the multi-agent sequence
├── twitter.py         # Twitter scraping logic using Selenium
├── tools/             # (Optional) Extra utility tools
├── .env               # Stores your Twitter login info

