# ── Stage: Flask API container ──────────────────────────────────────
# Base image: official slim Python 3.12
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency list first (Docker caches this layer if requirements.txt didn't change)
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Start the Flask development server
CMD ["python", "app.py"]
