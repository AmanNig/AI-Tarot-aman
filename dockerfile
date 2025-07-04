# 1. Base image
FROM python:3.10-slim

# 2. Set a working directory
WORKDIR /app

# 3. Install system deps (for pdfplumber, voice, etc.)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libsndfile1 \
      libasound2 \
      ffmpeg \
      # for pdfplumber text extraction
      poppler-utils \
 && rm -rf /var/lib/apt/lists/*

# 4. Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your code
COPY . .

# 6. Expose any ports if you have an API or streamlit (optional)
 EXPOSE 8080

# 7. Set any environment variables



# 8. Default command: launch your main script
CMD ["uvicorn", "api:app"]
