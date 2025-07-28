# FROM --platform=linux/amd64 python:3.10-slim

# # Set working directory
# WORKDIR /app

# # Install system dependencies required for PyMuPDF and other packages
# RUN apt-get update && \
#     apt-get install -y build-essential gcc && \
#     apt-get clean && rm -rf /var/lib/apt/lists/*

# # Copy requirements first for better caching
# COPY requirements.txt ./

# # Install Python dependencies (including NLP + sentence-transformers model)
# RUN pip install --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt && \
#     python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# # Copy source files
# COPY src/ ./src/
# COPY main.py .

# # Optional fallback folders (not mandatory to mount them externally)
# RUN mkdir -p /app/input /app/output

# # Default command
# ENTRYPOINT ["python", "main.py"]
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for PyMuPDF and others
RUN apt-get update && \
    apt-get install -y build-essential gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download sentence-transformer model offline (AFTER it's installed)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy your source code
COPY src/ ./src/
COPY main.py .

# Create input/output folders
RUN mkdir -p /app/input /app/output

# Entry point
ENTRYPOINT ["python", "main.py"]
