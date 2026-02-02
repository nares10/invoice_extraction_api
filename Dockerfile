FROM python:3.10-slim

WORKDIR /app

# Create venv
RUN python -m venv /opt/venv

# Make venv default
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies into venv
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
