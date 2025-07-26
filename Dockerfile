# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install LangGraph dependencies
RUN pip install --no-cache-dir langgraph langchain langserve fastapi uvicorn

# Copy your project files
COPY main.py .
COPY langgraph.json .  # Include if using CLI config

# Expose the default port for the LangGraph server
EXPOSE 8000

# Run the server (assumes 'app' is your FastAPI instance in main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
