FROM python:3.14-slim

WORKDIR /app

# Copy dependency configs first to leverage build caches
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose Render's default port target (documentation indicator)
EXPOSE 10000

# Force the container shell execution string to use Render's dynamic $PORT variable
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}