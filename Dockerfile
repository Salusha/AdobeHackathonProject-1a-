FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (PyMuPDF requires libmupdf)
RUN apt-get update && apt-get install -y build-essential gcc && apt-get clean

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --no-deps -r requirements.txt && \
    pip install --no-cache-dir sentence-transformers


# Copy source code and main script
COPY src/ ./src/
COPY main.py .

# Create input/output folders inside container (optional safety)
RUN mkdir -p /app/input /app/output

# Run main script
ENTRYPOINT ["python", "main.py"]
