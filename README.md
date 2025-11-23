# Enterprise BRD Template Generator

A comprehensive, enterprise-grade tool for creating and managing Business Requirement Documents (BRD) for Generative AI applications. Built with **Python 3.13.3**, **Streamlit**, **Pydantic**, **SQLite**, and **Ollama** for intelligent content generation.

## Features

- **Project Management**: Create, edit, and delete BRD projects with persistent SQLite storage
- **Comprehensive BRD Structure**: Supports all essential sections including Overview, UI Specifications, API Specifications, LLM Prompts, Database Schema, Technology Stack, and Traceability Matrix
- **AI-Powered Content Generation**: Leverage local LLM models (Ollama) for intelligent suggestions and content generation
- **Multi-Sheet Excel Export**: Generate professional, formatted Excel files with all BRD sections
- **Data Validation**: Built-in Pydantic models ensure data integrity and consistency
- **Master/Detail Support**: Handle complex UI requirements with master-detail relationships
- **Front-End Validation**: Define comprehensive validation rules and business logic
- **Technology Stack Documentation**: Document framework selection with detailed rationale

## Technology Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| **Language** | Python | 3.13.3 |
| **Web Framework** | Streamlit | Latest |
| **Data Validation** | Pydantic | 2.9.2 |
| **Database** | SQLite | Native |
| **LLM Runtime** | Ollama | Latest |
| **LLM Models** | Llama 3.2, Mistral, DeepSeek-R1, Phi4-mini | Latest |
| **Data Processing** | Pandas | 2.2.3 |
| **Excel Export** | openpyxl | 3.1.5 |

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.13.3** or higher
- **Ollama** (for LLM features) - Download from [ollama.ai](https://ollama.ai)
- **Git** (optional, for version control)

## Installation

### Step 1: Clone or Download the Project

```bash
cd /home/ubuntu/brd_streamlit_tool
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Ollama (Optional but Recommended)

To use AI-powered content generation features, you need to install and run Ollama:

1. **Install Ollama** from [ollama.ai](https://ollama.ai)
2. **Start Ollama service**:
   ```bash
   ollama serve
   ```
3. **Pull required models** (in a new terminal):
   ```bash
   ollama pull llama3.2
   ollama pull mistral
   ollama pull deepseek-r1
   ollama pull phi4-mini
   ```

## Usage

### Quick Start

#### Option 1: Using the Startup Script

```bash
cd /home/ubuntu/brd_streamlit_tool
./run.sh
```

#### Option 2: Manual Startup

```bash
cd /home/ubuntu/brd_streamlit_tool
source venv/bin/activate
streamlit run app.py
```

The application will start and open in your default browser at `http://localhost:8501`

### Application Workflow

#### 1. **Home Page**
   - View project statistics
   - Check system status (Ollama connection, database)
   - See recent projects

#### 2. **Create Project**
   - Fill in project overview information:
     - Project Name
     - Project Description
     - Business Goal
     - Document Version
     - Prepared By / Approved By
     - Target Release Date
   - Click "Create Project" to initialize

#### 3. **Manage Projects**
   - Select a project from the dropdown
   - Edit project details across multiple tabs:
     - **Overview**: Project metadata
     - **UI Specs**: User interface requirements
     - **API Specs**: API endpoints and payloads
     - **LLM Prompts**: Generative AI prompts
     - **Database**: Schema and relationships
     - **Tech Stack**: Technology selections
     - **Traceability**: Requirement linking
   - Save changes
   - Export to Excel
   - Delete projects

#### 4. **Export to Excel**
   - Click "Export to Excel" button
   - Generates a professionally formatted multi-sheet Excel file
   - Includes all BRD sections with proper formatting
   - Download the file directly from the browser

## BRD Structure

### Overview
High-level project information including name, description, business goals, and document metadata.

### UI Specification
User interface requirements with:
- Requirement IDs
- Feature/Module mapping
- Screen/Component details
- Validation rules (front-end)
- Business rules (server-side)
- Master/Detail relationships
- Priority (MoSCoW)

### API Specification
API endpoints with:
- API IDs and names
- HTTP methods and endpoints
- Request/Response payloads (JSON)
- Business logic
- API type (Internal, External, Third-Party)

### LLM Prompts
Generative AI configurations with:
- Prompt IDs and use cases
- Prompt templates with variables
- Expected output formats
- Model selection
- Temperature and configuration parameters

### Database Schema
Data model with:
- Table names and fields
- Data types
- Constraints (Primary Key, Foreign Key, etc.)
- Relationships
- Field descriptions

### Technology Stack
Technology selections with:
- Categories (Frontend, Backend, Database, LLM, etc.)
- Technology/Tool names
- Versions
- Rationale for selection
- Repository URLs

### Traceability Matrix
Links between:
- Business requirements
- UI implementations
- API endpoints
- LLM prompts
- Implementation status

## Project Structure

```
brd_streamlit_tool/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── run.sh                          # Startup script
├── README.md                       # This file
├── models/
│   ├── __init__.py
│   └── brd_models.py              # Pydantic data models
├── utils/
│   ├── __init__.py
│   ├── database.py                # SQLite operations
│   ├── llm_integration.py         # Ollama integration
│   └── excel_export.py            # Excel generation
└── data/
    └── brd_projects.db            # SQLite database (auto-created)
```

## Configuration

### Ollama Connection
The application connects to Ollama at `http://localhost:11434` by default. To change this, edit `utils/llm_integration.py`:

```python
OLLAMA_BASE_URL = "http://localhost:11434"
```

### Database Location
The SQLite database is stored at `data/brd_projects.db`. To reset the database, simply delete this file and restart the application.

## Troubleshooting

### Ollama Not Connected
- Ensure Ollama is installed and running
- Check that it's accessible at `http://localhost:11434`
- Restart Ollama service if needed
- Verify models are installed: `ollama list`

### Database Issues
- Delete `data/brd_projects.db` to reset the database
- The database will be recreated automatically on next startup
- Check file permissions in the `data/` directory

### Excel Export Fails
- Ensure you have write permissions in the application directory
- Check that all required fields are filled in
- Try exporting to a different location if permission errors occur

### Streamlit Port Already in Use
- Change the port: `streamlit run app.py --server.port 8502`
- Or kill the existing process: `lsof -i :8501` and `kill -9 <PID>`

## API Reference

### Pydantic Models

All data is validated using Pydantic models in `models/brd_models.py`:

- **OverviewModel**: Project metadata
- **UISpecificationModel**: UI requirements
- **APISpecificationModel**: API endpoints
- **LLMPromptModel**: LLM configurations
- **DatabaseSchemaModel**: Database design
- **TechStackModel**: Technology selections
- **TraceabilityModel**: Requirement tracing
- **BRDProjectModel**: Complete BRD project

### Database Functions

Located in `utils/database.py`:

- `init_database()`: Initialize SQLite database
- `create_project(brd_project)`: Create new project
- `get_project(project_id)`: Retrieve project
- `list_projects()`: List all projects
- `update_project(brd_project)`: Update existing project
- `delete_project(project_id)`: Delete project

### LLM Integration Functions

Located in `utils/llm_integration.py`:

- `check_ollama_connection()`: Verify Ollama availability
- `get_available_models()`: List available LLM models
- `generate_ui_requirement()`: Generate UI specs
- `generate_api_specification()`: Generate API specs
- `generate_llm_prompt()`: Generate LLM prompts
- `generate_database_schema()`: Generate DB schema
- `generate_tech_stack_rationale()`: Generate tech recommendations

### Excel Export

Located in `utils/excel_export.py`:

- `export_brd_to_excel(brd_project, filename)`: Generate Excel file with all BRD sections

## Sample Use Cases

### Customer Feedback Management Platform
A complete example BRD for a GenAI application that analyzes customer feedback using multiple LLM models for sentiment analysis, categorization, and response generation.

### E-Commerce Product Recommendation Engine
BRD for a system that uses LLMs to generate personalized product recommendations based on user behavior and feedback.

### Intelligent Customer Support Chatbot
BRD for a multi-model GenAI system that handles customer inquiries with sentiment analysis, intent classification, and response generation.

## Best Practices

1. **Always fill in the Overview section first** - This establishes project context
2. **Use consistent naming conventions** - Maintain clear ID patterns (UI-001, API-001, etc.)
3. **Link requirements in Traceability Matrix** - Ensure complete coverage and testability
4. **Document business rules clearly** - Separate front-end validation from server-side logic
5. **Specify LLM models explicitly** - Include temperature and other configuration parameters
6. **Export regularly** - Generate Excel files as checkpoints during development
7. **Use Master/Detail appropriately** - Clearly identify complex screen relationships

## Performance Considerations

- **Database**: SQLite is suitable for projects up to 1000+ BRDs
- **LLM Generation**: Responses may take 5-30 seconds depending on model and prompt complexity
- **Excel Export**: Large projects (100+ items per section) may take 10-15 seconds to generate

## Security Notes

- The application stores all data locally in SQLite
- No data is sent to external servers (except Ollama, which runs locally)
- Ensure proper file permissions on the `data/` directory
- Use strong authentication if deploying to a shared server

## Contributing

To extend the application:

1. Add new Pydantic models in `models/brd_models.py`
2. Implement database operations in `utils/database.py`
3. Create UI components in `app.py`
4. Add LLM integration functions in `utils/llm_integration.py`

## License

This project is provided as-is for enterprise use.

## Support

For issues, questions, or feature requests, please refer to the Help & Documentation section within the application.

## Changelog

### Version 1.0 (2025-11-20)
- Initial release
- Core BRD template structure
- Streamlit UI with multi-page navigation
- SQLite persistence
- Ollama LLM integration
- Multi-sheet Excel export
- Pydantic data validation
- Comprehensive documentation

---

**Last Updated**: 2025-11-20  
**Version**: 1.0  
**Author**: Manus AI
