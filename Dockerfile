FROM python:3.11-slim

WORKDIR /app

# Copy files correctly - maintain folder structure
# /app/backend/  <- backend code
# /app/frontend/ <- frontend files
# /app/uploads/  <- for uploaded files
# /app/renders/  <- for rendered images

COPY main.py .
COPY backend/requirements.txt ./backend/
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Create directories
RUN mkdir -p uploads renders

# Expose port
EXPOSE 8080

# Set env
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8080

# Run - set PYTHONPATH to /app so imports work correctly
ENV PYTHONPATH=/app
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
