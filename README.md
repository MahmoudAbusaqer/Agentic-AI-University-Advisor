# 🎓 Agentic AI University Advisor

An autonomous AI agent that assists Missouri State University students with course registration questions using Claude AI and agentic architecture.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)
![Claude](https://img.shields.io/badge/Claude-Sonnet_4-purple.svg)
![Agentic AI](https://img.shields.io/badge/Agentic-AI-orange.svg)

## 📋 Overview

This project implements an autonomous AI agent capable of answering course registration questions for Missouri State University students. The agent uses Claude Sonnet 4 with a custom knowledge base built from official MSU sources.

**Key Features:**
- 🤖 **Agentic Architecture**: Autonomous decision-making and response generation
- 📚 **Knowledge Base**: Built from official MSU Registrar's Office sources
- 💬 **Conversational Interface**: Web-based chat and command-line interfaces
- ✅ **Honest Limitations**: Explicitly states when it doesn't know something
- 🔍 **Source Attribution**: Provides contact information when needed

**Capabilities:**
- Answers questions about registration procedures and policies
- Explains holds, prerequisites, and common registration errors
- Provides information about mixed credit and senior permission
- Handles questions about majors, minors, and certificates
- Directs students to appropriate offices when needed

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

```bash
# Clone the repository
git clone https://github.com/MahmoudAbusaqer/Agentic-AI-University-Advisor.git
cd Agentic-AI-University-Advisor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env

# Run the application
python app.py
```

Open your browser to `http://localhost:5000`

## 💡 Usage

### Web Interface
```bash
python app.py
# Visit http://localhost:5000
```

### Command Line Interface
```bash
python agent.py
# Interactive chat in terminal
```

### Python API
```python
from agent import MSURegistrationAgent

agent = MSURegistrationAgent()
response = agent.ask("What is mixed credit?")
print(response)
```

## 🎯 Example Interactions

**Questions the agent can answer:**
- "My student has a hold. What should they do?"
- "What is the difference between mixed credit and senior permission?"
- "How do I know when my student can register?"
- "Can a certificate be earned by itself?"
- "What is a DG or DX hold?"
- "How do pass/not pass courses affect GPA?"

**Honest responses when information is unavailable:**
- For questions outside the knowledge base, the agent provides appropriate contact information
- Never generates false information or "hallucinations"

## 🏗️ Architecture

### System Components

```
┌─────────────────┐
│   User Input    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask Web App  │
│   (app.py)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   AI Agent      │
│  (agent.py)     │
│                 │
│  • Claude API   │
│  • Knowledge    │
│    Base         │
│  • System       │
│    Prompt       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Response Gen   │
└─────────────────┘
```

### Technical Stack

**Backend:**
- Python 3.9+
- Flask web framework
- Anthropic Claude API (Sonnet 4)

**Data Collection:**
- BeautifulSoup4 for web scraping
- Custom validation and formatting
- Source attribution tracking

**Frontend:**
- Vanilla JavaScript
- HTML5/CSS3
- Responsive design

**Knowledge Base:**
- Official MSU Registrar sources
- Academic Advising resources
- Registration procedures and policies

## 🔧 Project Structure

```
Agentic-AI-University-Advisor/
├── agent.py                 # Core agent logic with Claude API
├── app.py                   # Flask web application
├── data_collector.py        # Web scraper for MSU sources
├── knowledge_base.txt       # Compiled information from MSU
├── templates/
│   └── index.html          # Web interface
├── requirements.txt         # Python dependencies
├── .env                    # API keys (create this - not in repo)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 📚 Data Sources

All information is collected from publicly available Missouri State University sources:

- MSU Registrar's Office - Advisor Toolkit
- Registration Services FAQ
- Academic Advising and Program Declaration
- Student Resources and Policies

**Important:** No student data or confidential information is used.

## 🛠️ Development

### Building the Knowledge Base

```bash
# Scrape MSU sources and build knowledge base
python data_collector.py

# This will create/update knowledge_base.txt
# Takes 5-10 minutes depending on number of sources
```

### Adding New Sources

Edit `data_collector.py` and add URLs to the `SOURCES` list:

```python
SOURCES = [
    "https://www.missouristate.edu/registrar/...",
    # Add more official MSU URLs here
]
```

Then rebuild: `python data_collector.py`

### Testing

```bash
# Basic functionality tests
python test_agent.py

# Accuracy validation
python test_accuracy.py
```

## 🔐 Privacy & Ethics

**Data Privacy:**
- No student personal data is collected
- No user conversations are stored
- API calls are ephemeral

**Information Accuracy:**
- All data from official MSU sources
- Agent clearly states when it doesn't know
- Provides contact information for verification

**Responsible AI:**
- Designed to assist, not replace, human advisors
- Transparent about being an AI system
- Encourages students to verify critical information

## 💻 Technical Implementation

### Agentic Architecture

The agent uses several key techniques:

**1. Contextual Understanding:**
- Analyzes entire conversation history
- Maintains context across multiple questions
- Understands follow-up questions

**2. Autonomous Decision Making:**
- Determines when it has sufficient information
- Decides when to admit uncertainty
- Chooses appropriate response format

**3. Source-Grounded Responses:**
- Only uses information from knowledge base
- Provides source attribution where appropriate
- Never invents information

### API Configuration

Uses Claude Sonnet 4 (`claude-sonnet-4-20250514`) with custom system prompt that:
- Defines agent role and boundaries
- Specifies how to handle uncertainty
- Ensures appropriate tone and formatting
- Provides contact information for escalation

## 📊 Current Status

**Implementation Stage:** Functional prototype  
**Knowledge Base:** Official MSU sources (Registrar, Advising)  
**Testing:** Validated with real student questions  
**Deployment:** Local development (web + CLI)

**Known Limitations:**
- Coverage limited to information in knowledge base
- Manual updates required when policies change
- English language only
- Requires internet connection for API calls

## 📈 Future Enhancements

**Planned Improvements:**
- [ ] User feedback collection system
- [ ] Expanded knowledge base (academic calendar, financial aid)
- [ ] Integration with MSU's student portal
- [ ] Multi-language support
- [ ] Analytics dashboard for common questions
- [ ] Automated knowledge base updates

**Scalability:**
- Architecture designed to work for any university
- Modular data collection system
- Easy to adapt for different institutions

## 📝 License

MIT License - See LICENSE file for details

---

**Note:** This is an independent student project and is not officially affiliated with or endorsed by Missouri State University. All information is sourced from publicly available MSU resources.
