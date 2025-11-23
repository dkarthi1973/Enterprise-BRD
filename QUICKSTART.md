# Enterprise BRD Template Generator - Quick Start Guide

## 5-Minute Setup

### Prerequisites
- Python 3.13.3 or higher
- Ollama (optional, for AI features)

### Installation

```bash
# 1. Navigate to project directory
cd /home/ubuntu/brd_streamlit_tool

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

The application opens at `http://localhost:8501`

## First Steps

### 1. Create Your First BRD Project

1. Click **"Create Project"** in the sidebar
2. Fill in the project details:
   - **Project Name**: e.g., "Customer Feedback Management"
   - **Project Description**: Brief overview of the application
   - **Business Goal**: Primary objective (e.g., "Automate feedback analysis")
   - **Prepared By**: Your name (default: "Local AI")
3. Click **"✅ Create Project"**

### 2. Edit Your Project

1. Go to **"Manage Projects"**
2. Select your project from the dropdown
3. Use tabs to edit different sections:
   - **Overview**: Project metadata
   - **UI Specs**: User interface requirements
   - **API Specs**: API endpoints
   - **LLM Prompts**: AI configurations
   - **Database**: Schema design
   - **Tech Stack**: Technology selections
   - **Traceability**: Requirement linking

### 3. Add Content to Each Section

#### UI Specifications Example
- **Requirement ID**: UI-001
- **Feature/Module**: Customer Profile Management
- **Screen/Component**: Customer Details Form
- **Requirement Description**: Display customer information and interaction history
- **Validation Rule**: Email must be valid format
- **Business Rule**: Cannot delete customer with open tickets
- **Master/Detail**: Master
- **Priority**: Must

#### API Specifications Example
- **API ID**: API-001
- **API Name**: Create New Customer
- **Method**: POST
- **Endpoint**: `/api/v1/customers`
- **Request Payload**: `{"name": "string", "email": "string"}`
- **Response Payload**: `{"customer_id": "integer", "status": "success"}`

#### LLM Prompts Example
- **Prompt ID**: LLM-001
- **Use Case**: Customer Sentiment Analysis
- **Prompt Template**: "Analyze sentiment of: [FEEDBACK_TEXT]"
- **Model**: llama3.2
- **Temperature**: 0.2

### 4. Use AI Assistance

If Ollama is running:

1. In **UI Specs** tab, scroll to "🤖 AI-Powered Suggestions"
2. Enter feature and screen names
3. Click **"🚀 Generate UI Requirement"**
4. AI generates suggestions based on your input

### 5. Export to Excel

1. Click **"📊 Export to Excel"** button
2. Click **"⬇️ Download Excel File"** to save
3. Opens in Excel with all sections formatted

## Common Tasks

### Add Multiple UI Requirements

1. Go to **Manage Projects** → **UI Specs** tab
2. Fill in the "Add New UI Specification" form
3. Click **"➕ Add UI Specification"**
4. Repeat for each requirement

### Link Requirements in Traceability

1. Go to **Traceability** tab
2. Create business requirement: "System must allow users to submit feedback"
3. Link to UI-001, API-001, LLM-001
4. Set status to "Approved"

### Generate API Documentation

1. Go to **API Specs** tab
2. Use **"🤖 AI-Powered Suggestions"** to generate API specs
3. Review and refine the generated content
4. Add to project

### Create Database Schema

1. Go to **Database** tab
2. Add tables and fields:
   - Table: Customers, Field: customer_id, Type: INT, Constraints: Primary Key
   - Table: Customers, Field: email, Type: VARCHAR(255), Constraints: NOT NULL, UNIQUE
3. Define relationships and constraints

## Tips & Best Practices

1. **Start with Overview**: Always fill in project overview first
2. **Use Consistent IDs**: Follow patterns like UI-001, API-001, LLM-001
3. **Document Business Rules**: Clearly separate validation (client) from business logic (server)
4. **Link Everything**: Use Traceability Matrix to ensure complete coverage
5. **Export Regularly**: Generate Excel files as checkpoints
6. **Leverage AI**: Use Ollama suggestions to accelerate documentation

## Keyboard Shortcuts

| Action | Shortcut |
| :--- | :--- |
| Save Changes | `Ctrl+S` (after filling form) |
| Refresh Page | `F5` |
| Open Help | Click **"Help & Documentation"** |

## Troubleshooting

### Application Won't Start

```bash
# Check Python version
python3 --version  # Should be 3.13.3+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check port availability
lsof -i :8501
```

### Ollama Not Connected

```bash
# Start Ollama service
ollama serve

# In new terminal, pull models
ollama pull llama3.2
ollama pull mistral
```

### Database Issues

```bash
# Reset database
rm data/brd_projects.db

# Restart application
streamlit run app.py
```

## Sample Project Templates

### Customer Feedback Management
- **Overview**: Platform for analyzing customer feedback
- **UI**: Feedback submission form, analysis dashboard
- **API**: Submit feedback, get analysis, list interactions
- **LLM**: Sentiment analysis, categorization, response generation
- **Database**: Feedback table, Analysis results table
- **Tech Stack**: FastAPI, Streamlit, Ollama, SQLite

### E-Commerce Product Recommendation
- **Overview**: AI-powered product recommendations
- **UI**: Product list, recommendation cards, user preferences
- **API**: Get recommendations, log interactions, update preferences
- **LLM**: Product description generation, recommendation reasoning
- **Database**: Products, Users, Recommendations, Interactions
- **Tech Stack**: Next.js, FastAPI, Ollama, PostgreSQL

### Intelligent Customer Support
- **Overview**: AI chatbot for customer support
- **UI**: Chat interface, ticket management, knowledge base
- **API**: Send message, create ticket, search knowledge base
- **LLM**: Intent classification, response generation, ticket categorization
- **Database**: Conversations, Tickets, Knowledge base articles
- **Tech Stack**: React, FastAPI, Ollama, MongoDB

## Next Steps

1. **Explore All Sections**: Familiarize yourself with each tab
2. **Create Sample Project**: Practice with a test project
3. **Read Full Documentation**: Check README.md for detailed info
4. **Set Up Ollama**: Install and configure for AI features
5. **Export and Review**: Generate Excel to see final output

## Support

- **Help & Documentation**: Available in the app sidebar
- **README.md**: Comprehensive documentation
- **DEPLOYMENT_GUIDE.md**: Production setup instructions

---

**Happy BRD Creating! 🚀**
