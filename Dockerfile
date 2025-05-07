FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs resources

# Set up RAG with sample data
RUN python src/setup.py --setup-rag

# Expose API port
EXPOSE 8000

# Run the application
CMD ["python", "src/main.py"]
