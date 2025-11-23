# Enterprise BRD Template Generator - Deployment Guide

## System Requirements

| Component | Requirement |
| :--- | :--- |
| **Operating System** | Linux, macOS, or Windows |
| **Python** | 3.13.3 or higher |
| **RAM** | Minimum 4GB (8GB recommended) |
| **Disk Space** | Minimum 2GB (for dependencies and database) |
| **Internet** | Required for initial setup only |

## Installation Steps

### Step 1: System Preparation

#### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y python3.13 python3.13-venv python3.13-dev
```

#### On macOS:
```bash
brew install python@3.13
```

#### On Windows:
Download and install Python 3.13 from [python.org](https://www.python.org/downloads/)

### Step 2: Project Setup

```bash
# Navigate to project directory
cd /home/ubuntu/brd_streamlit_tool

# Create virtual environment
python3.13 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Ollama Installation (Optional but Recommended)

#### On Linux:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### On macOS:
```bash
brew install ollama
```

#### On Windows:
Download installer from [ollama.ai](https://ollama.ai)

### Step 4: Pull LLM Models

```bash
# Start Ollama service
ollama serve

# In another terminal, pull models:
ollama pull llama3.2
ollama pull mistral
ollama pull deepseek-r1
ollama pull phi4-mini
```

## Running the Application

### Quick Start

```bash
cd /home/ubuntu/brd_streamlit_tool
./run.sh
```

### Manual Start

```bash
cd /home/ubuntu/brd_streamlit_tool
source venv/bin/activate
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Configuration

### Environment Variables

Create a `.env` file in the project root (optional):

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### Database Configuration

The SQLite database is automatically created at `data/brd_projects.db`. To reset:

```bash
rm data/brd_projects.db
```

The database will be recreated on next application startup.

## Production Deployment

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t brd-template-generator .
docker run -p 8501:8501 -v $(pwd)/data:/app/data brd-template-generator
```

### Using Gunicorn (Advanced)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "streamlit.web.cli:main"
```

### Using Nginx Reverse Proxy

```nginx
upstream streamlit {
    server localhost:8501;
}

server {
    listen 80;
    server_name brd-tool.example.com;

    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Performance Optimization

### Database Optimization

```bash
# Vacuum database to optimize size
sqlite3 data/brd_projects.db "VACUUM;"

# Create indexes for faster queries
sqlite3 data/brd_projects.db "CREATE INDEX IF NOT EXISTS idx_project_name ON projects(project_name);"
```

### Streamlit Configuration

Edit `~/.streamlit/config.toml`:

```toml
[client]
showErrorDetails = false

[server]
maxUploadSize = 200
enableXsrfProtection = true
enableCORS = false

[logger]
level = "warning"

[theme]
primaryColor = "#0070C0"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

## Monitoring and Maintenance

### Log Monitoring

```bash
# Run with verbose logging
streamlit run app.py --logger.level=debug

# Check application logs
tail -f ~/.streamlit/logs/streamlit.log
```

### Database Backup

```bash
# Backup database
cp data/brd_projects.db data/brd_projects.db.backup

# Restore database
cp data/brd_projects.db.backup data/brd_projects.db
```

### Regular Maintenance

```bash
# Clean up old files
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# Update dependencies
pip install --upgrade -r requirements.txt
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8502
```

### Memory Issues

```bash
# Monitor memory usage
watch -n 1 'ps aux | grep streamlit'

# Increase available memory or optimize queries
```

### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
killall ollama
ollama serve
```

### Database Corruption

```bash
# Check database integrity
sqlite3 data/brd_projects.db "PRAGMA integrity_check;"

# Rebuild database if corrupted
sqlite3 data/brd_projects.db ".dump" | sqlite3 data/brd_projects_new.db
mv data/brd_projects_new.db data/brd_projects.db
```

## Security Considerations

1. **Authentication**: Add authentication layer using Streamlit authentication or OAuth
2. **HTTPS**: Use SSL/TLS certificates for production
3. **Database**: Encrypt sensitive data in database
4. **File Permissions**: Restrict access to `data/` directory
5. **API Keys**: Store Ollama credentials securely
6. **Input Validation**: All inputs are validated with Pydantic

### Example: Adding Basic Authentication

```python
import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        password = st.text_input("Password", type="password")
        if password == "your_secure_password":
            st.session_state.password_correct = True
            st.rerun()
        else:
            return False
    return True

if check_password():
    # Your app code here
    pass
```

## Scaling Considerations

### For Multiple Users

1. Use a shared database (PostgreSQL instead of SQLite)
2. Implement user authentication and role-based access
3. Use a load balancer (Nginx, HAProxy)
4. Deploy multiple instances of the application

### Database Migration (SQLite to PostgreSQL)

```python
# Install PostgreSQL driver
pip install psycopg2-binary

# Update database.py to use PostgreSQL
# Change DB_PATH to PostgreSQL connection string
```

## Backup and Recovery

### Automated Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="backups"
DB_FILE="data/brd_projects.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp $DB_FILE "$BACKUP_DIR/brd_projects_$TIMESTAMP.db"

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
```

Schedule with cron:
```bash
0 2 * * * /path/to/backup.sh  # Run daily at 2 AM
```

## Support and Troubleshooting

For issues or questions:

1. Check the logs: `~/.streamlit/logs/streamlit.log`
2. Review the Help & Documentation section in the app
3. Check Ollama status: `curl http://localhost:11434/api/tags`
4. Verify database: `sqlite3 data/brd_projects.db ".tables"`

## Version Updates

### Updating Dependencies

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade streamlit

# Generate new requirements
pip freeze > requirements.txt
```

### Backup Before Updates

```bash
# Always backup before updating
cp data/brd_projects.db data/brd_projects.db.backup
```

---

**Last Updated**: 2025-11-20  
**Version**: 1.0
