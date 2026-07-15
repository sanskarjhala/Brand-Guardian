# Brand Guardian - Multi Model AI Compliance System

## 📋 Overview

Brand Guardian is an intelligent compliance monitoring system that automates the analysis of brand mentions across video transcripts and documents. It uses multi-agent AI reasoning with LangGraph and GPT-4o to detect compliance violations, analyze sentiment, and generate structured compliance reports—reducing manual review time from hours to minutes.

**Live Demo:** [Coming Soon]  
**GitHub Repository:** [Your GitHub Link]  
**Author:** [Sanskar Jhala](https://github.com/sanskarjhala)

---

## 🎯 Problem Statement

Compliance teams spend significant time manually analyzing:
- Video transcripts for brand mentions
- Document scans (OCR signals)
- Regulatory requirements across large knowledge bases

This process is:
- ❌ **Time-consuming:** Hours per document
- ❌ **Error-prone:** Human oversight and inconsistency
- ❌ **Unscalable:** Can't handle high document volumes
- ❌ **Expensive:** Requires dedicated compliance staff

---

## Solution: Brand Guardian

Brand Guardian automates compliance analysis using AI agents, reducing manual work and improving accuracy.

### Key Capabilities:
- **Multi-Agent Reasoning:** LangGraph orchestrates specialized AI agents
- **Video Analysis:** Extracts and analyzes video transcripts
- **Document Processing:** Handles OCR-extracted text from scanned documents
- **Compliance Detection:** Identifies policy violations in real-time
- **Structured Reports:** Generates JSON compliance reports for easy integration
- **Full Observability:** LangSmith tracing for debugging and monitoring

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│            FastAPI Backend (REST API)                   │
├─────────────────────────────────────────────────────────┤
│  Endpoints:                                             │
│  • POST /analyze (video/document)                       │
│  • GET /reports/{id}                                    │
│  • GET /health                                          │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│       LangGraph Multi-Agent Orchestration               │
├─────────────────────────────────────────────────────────┤
│  1. Parsing Agent    → Extract structured data          │
│  2. Classification Agent → Categorize mentions          │
│  3. Sentiment Agent  → Analyze brand perception         │
│  4. Compliance Agent → Check policy violations          │
└──────────────────┬──────────────────────────────────────┘
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
    ┌─────┐   ┌─────────┐  ┌──────────┐
    │GPT- │   │Knowledge│  │Azure AI  │
    │ 4o  │   │ Base    │  │Services  │
    └─────┘   └─────────┘  └──────────┘
       │           │           │
       └───────────┼───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ LangSmith (Tracing)  │
        │ Azure App Insights   │
        └──────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python)
- **AI/LLM:**
  - LangGraph (multi-agent orchestration)
  - LangChain (LLM utilities)
  - GPT-4o (reasoning engine)
  - OpenAI API

### Cloud & Infrastructure
- **Cloud Platform:** Azure AI Foundry
- **Services:**
  - Azure Blob Storage (document storage)
  - Azure AI Search (knowledge base indexing)
  - Azure App Insights (monitoring)

### Observability
- **LangSmith:** End-to-end LLM tracing
- **Logging:** Python logging + Azure Insights

### Development
- **Language:** Python 3.9+
- **Package Manager:** pip
- **Version Control:** Git

---

## ✅ Features

### 1. Multi-Agent Reasoning
- Each agent handles specific compliance aspects
- Agents collaborate to reach final compliance decision

### 2. Video Transcript Analysis
- Parses video transcripts
- Extracts brand mentions with context
- Analyzes sentiment and tone

### 3. Document Processing
- Handles OCR-extracted text
- Processes scanned regulatory documents
- Extracts compliance-relevant information

### 4. Compliance Detection
- Compares mentions against compliance rules
- Identifies policy violations
- Flags high-risk content

### 5. Structured Output
- Generates JSON compliance reports
- Easy integration with downstream systems
- Machine-readable format

### 6. Full Observability
- LangSmith traces every agent decision
- Debug complex reasoning chains
- Monitor system performance

---


## 🚀 Getting Started

### Prerequisites
```bash
Python 3.9+
pip
Azure account with AI Foundry access
OpenAI API key
```

### API Documentation
Once running, visit: `http://localhost:8000/docs` 

---

## 🔍 How LangGraph Orchestration Works

```
User Request
    │
    ▼
┌──────────────────────────┐
│ 1. Parsing Agent         │
│ Extract content + context│
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 2. Classification Agent  │
│ Categorize mention type  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 3. Sentiment Agent       │
│ Analyze tone/sentiment   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 4. Compliance Agent      │
│ Check policy violations  │
└────────────┬─────────────┘
             │
             ▼
        Final Report (JSON)
```

Each agent:
- Takes input from previous step
- Processes with GPT-4o
- Passes structured output to next agent
- All decisions traced in LangSmith

---

## 🔮 Future Improvements

- [ ] Support for audio files (transcription + analysis)
- [ ] Custom compliance rule builder (UI)
- [ ] Multi-language support
- [ ] Real-time monitoring dashboard
- [ ] Webhook notifications for violations
- [ ] Bulk upload and batch processing
- [ ] Cost optimization (caching, token reduction)


---

## 🛣️ Project Journey

**Timeline:** Jan 2026 - Apr 2026 

- **Week 1-2:** Requirements gathering, architecture design
- **Week 3-4:** LangGraph agent implementation
- **Week 5-6:** Azure deployment, LangSmith integration
- **Week 7-8:** Testing, optimization, documentation

---

##  Learning Outcomes

This project deepened my understanding of:
- ✅ Multi-agent AI systems and orchestration
- ✅ LLM prompt engineering for structured output
- ✅ Production AI application architecture
- ✅ Cloud infrastructure (Azure AI Foundry)
- ✅ Observability in LLM systems
- ✅ Handling unstructured data (text, OCR)
- ✅ Building APIs that integrate with AI pipelines

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---


## 📞 Contact & Links

- **GitHub:** [github.com/sanskarjhala](https://github.com/sanskarjhala)
- **LinkedIn:** [linkedin.com/in/sanskarjhala](https://linkedin.com/in/sanskarjhala)
- **Email:** sanskarjhala@gmail.com

---

##  Acknowledgments

- **LangChain & LangGraph** communities for excellent documentation
- **OpenAI** for GPT-4o capabilities
- **Azure** for reliable cloud infrastructure

---

**Built with ❤️ by Sanskar Jhala**
