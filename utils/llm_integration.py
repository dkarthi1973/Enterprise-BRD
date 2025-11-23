"""
LLM integration utilities for Ollama-based content generation.
"""

import requests
import json
from typing import Optional, List, Generator
import streamlit as st


# Default Ollama endpoint
OLLAMA_BASE_URL = "http://localhost:11434"

# Available models
AVAILABLE_MODELS = [
    "llama3.2",
    "mistral",
    "deepseek-r1",
    "phi4-mini"
]


def check_ollama_connection() -> bool:
    """Check if Ollama is running and accessible."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
        return response.status_code == 200
    except Exception as e:
        print(f"Ollama connection error: {e}")
        return False


def get_available_models() -> List[str]:
    """Get list of available models from Ollama."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = [model["name"].split(":")[0] for model in data.get("models", [])]
            return list(set(models))  # Remove duplicates
        return AVAILABLE_MODELS
    except Exception as e:
        print(f"Error fetching models: {e}")
        return AVAILABLE_MODELS


def generate_ui_requirement(
    feature_module: str,
    screen_component: str,
    model: str = "llama3.2",
    temperature: float = 0.7
) -> Generator[str, None, None]:
    """Generate UI requirement description using LLM."""
    prompt = f"""You are an expert UI/UX designer and requirements analyst. 
    
Generate a detailed UI requirement description for the following:
- Feature/Module: {feature_module}
- Screen/Component: {screen_component}

Provide:
1. A comprehensive requirement description (100-200 words)
2. Key validation rules (2-3 rules)
3. Business rules (2-3 rules)
4. Suggest if this is Master or Detail component

Format your response as structured text with clear sections."""

    yield from _stream_ollama_response(prompt, model, temperature)


def generate_api_specification(
    api_name: str,
    endpoint: str,
    method: str = "GET",
    model: str = "mistral",
    temperature: float = 0.5
) -> Generator[str, None, None]:
    """Generate API specification using LLM."""
    prompt = f"""You are an expert API architect and backend developer.

Generate a detailed API specification for:
- API Name: {api_name}
- Endpoint: {endpoint}
- HTTP Method: {method}

Provide:
1. Request payload structure (JSON format)
2. Response payload structure (JSON format)
3. Business rules and validation logic
4. Error handling considerations

Format your response as structured text with clear sections."""

    yield from _stream_ollama_response(prompt, model, temperature)


def generate_llm_prompt(
    use_case: str,
    input_context: str = "",
    model: str = "mistral",
    temperature: float = 0.7
) -> Generator[str, None, None]:
    """Generate LLM prompt template using LLM."""
    prompt = f"""You are an expert prompt engineer specializing in GenAI applications.

Generate a detailed LLM prompt for the following use case:
- Use Case: {use_case}
{f'- Context: {input_context}' if input_context else ''}

Provide:
1. A well-crafted prompt template with placeholders like [VARIABLE_NAME]
2. List of input variables needed
3. Expected output format (JSON or text)
4. Suggested model and temperature parameters
5. Example usage

Format your response as structured text with clear sections."""

    yield from _stream_ollama_response(prompt, model, temperature)


def generate_database_schema(
    feature_description: str,
    model: str = "mistral",
    temperature: float = 0.5
) -> Generator[str, None, None]:
    """Generate database schema suggestions using LLM."""
    prompt = f"""You are an expert database architect and data modeler.

Generate database schema suggestions for the following feature:
- Feature Description: {feature_description}

Provide:
1. Recommended tables and their purposes
2. Key fields for each table with data types
3. Primary and foreign key relationships
4. Constraints and validation rules
5. Indexing suggestions

Format your response as structured text with clear sections and a table format where applicable."""

    yield from _stream_ollama_response(prompt, model, temperature)


def generate_tech_stack_rationale(
    project_requirements: str,
    model: str = "deepseek-r1",
    temperature: float = 0.6
) -> Generator[str, None, None]:
    """Generate technology stack recommendations and rationale."""
    prompt = f"""You are an expert software architect with deep knowledge of modern technology stacks.

Recommend a technology stack for the following project:
- Requirements: {project_requirements}

Provide:
1. Frontend framework recommendation with rationale
2. Backend framework recommendation with rationale
3. Database recommendation with rationale
4. LLM/AI framework recommendation with rationale
5. DevOps and deployment tools
6. Version control strategy

Format your response as structured text with clear sections and detailed rationale for each choice."""

    yield from _stream_ollama_response(prompt, model, temperature)


def _stream_ollama_response(
    prompt: str,
    model: str = "llama3.2",
    temperature: float = 0.7
) -> Generator[str, None, None]:
    """Stream response from Ollama API."""
    try:
        url = f"{OLLAMA_BASE_URL}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": True
        }
        
        response = requests.post(url, json=payload, stream=True, timeout=300)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    if "response" in data:
                        yield data["response"]
                except json.JSONDecodeError:
                    continue
    
    except requests.exceptions.ConnectionError:
        yield "Error: Could not connect to Ollama. Make sure Ollama is running on http://localhost:11434"
    except requests.exceptions.Timeout:
        yield "Error: Request timed out. Ollama is taking too long to respond."
    except Exception as e:
        yield f"Error: {str(e)}"


def generate_completion(
    prompt: str,
    model: str = "llama3.2",
    temperature: float = 0.7,
    max_tokens: int = 2000
) -> str:
    """Generate a single completion from Ollama (non-streaming)."""
    try:
        url = f"{OLLAMA_BASE_URL}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }
        
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        
        data = response.json()
        return data.get("response", "")
    
    except Exception as e:
        return f"Error: {str(e)}"
