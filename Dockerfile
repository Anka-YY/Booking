FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ДОБАВЬТЕ ЭТУ ПРОВЕРКУ
RUN pip list | grep uvicorn
RUN which uvicorn || echo "uvicorn not found"

COPY . .

RUN useradd --create-home --shell /bin/bash appuser
USER appuser

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]