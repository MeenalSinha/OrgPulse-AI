FROM python:3.11-slim

WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy shared MCP connector layer and mock data, then the backend app
COPY mcp_connectors ./mcp_connectors
COPY data ./data
COPY backend ./backend

WORKDIR /app/backend
ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
