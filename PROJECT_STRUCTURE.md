# Enterprise BRD Template Tool - Project Structure

## 📁 Directory Layout

```
brd_streamlit_tool/
├── app.py                          # Main Streamlit application (FIXED v3.0)
├── requirements.txt                # Python dependencies
├── README.md                        # Project overview
├── QUICKSTART.md                    # 5-minute setup guide
├── DEPLOYMENT_GUIDE.md              # Production deployment
├── PROJECT_STRUCTURE.md             # This file
│
├── models/                          # Pydantic data models
│   ├── __init__.py
│   ├── brd_models.py               # Core BRD models
│   ├── brd_models_enhanced.py      # Enhanced models
│   ├── agent_models.py             # Multi-agent models
│   ├── agent_pattern_models.py     # Agent patterns (ReAct, RAG, etc.)
│   ├── template_models.py          # Template types
│   └── governance_models.py        # LLM governance
│
├── utils/                           # Utility modules
│   ├── __init__.py
│   ├── database.py                 # SQLite operations (FIXED v3.0)
│   ├── excel_export.py             # Excel export (FIXED v3.0)
│   ├── llm_integration.py          # Ollama LLM integration
│   ├── logger.py                   # Logging system
│   ├── config_manager.py           # Configuration management
│   └── template_manager.py         # Template management
│
├── config/                          # Configuration files
│   ├── system.yaml                 # System settings
│   ├── llm_config.yaml             # LLM configuration
│   ├── governance.yaml             # Governance policies
│   └── template_defaults.json      # Template defaults
│
├── data/                            # Auto-created at runtime
│   └── brd_projects.db             # SQLite database
│
├── logs/                            # Auto-created at runtime
│   └── brd_app_YYYYMMDD.log       # Application logs
│
└── exports/                         # Auto-created at runtime
    └── BRD_*.xlsx                  # Exported Excel files
```

## 📋 File Descriptions

### Core Application
- **app.py** - Main Streamlit application with all UI and functionality

### Data Models
- **brd_models.py** - Core BRD data structures
- **agent_models.py** - Multi-agent system models
- **template_models.py** - Three template types
- **governance_models.py** - LLM governance and guardrails

### Utilities
- **database.py** - SQLite CRUD operations
- **excel_export.py** - Multi-sheet Excel export
- **llm_integration.py** - Ollama LLM integration
- **logger.py** - Comprehensive logging

### Configuration
- **system.yaml** - Application settings
- **llm_config.yaml** - LLM model configuration
- **governance.yaml** - Governance policies
- **template_defaults.json** - Template defaults

## 🚀 Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Start Ollama: `ollama serve`
3. Run app: `streamlit run app.py`

## ✅ Features

- Three customized BRD templates (Normal, Agentic, Multi-Agentic)
- Seven BRD sections with full CRUD
- AI-powered suggestions on all pages
- Multi-sheet Excel export
- SQLite data persistence
- Comprehensive logging
- Professional UI with Streamlit

## 🔧 Recent Fixes (v3.0)

- ✅ Fixed project creation
- ✅ Added form validation
- ✅ Added view/edit/delete for all items
- ✅ Fixed form reset
- ✅ Added AI suggestions to all pages
- ✅ Implemented comprehensive logging
- ✅ Fixed data persistence
- ✅ Fixed Excel export

## 📞 Support

See README.md, QUICKSTART.md, and DEPLOYMENT_GUIDE.md for detailed information.
