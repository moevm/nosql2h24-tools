FROM python:3.11

WORKDIR /app

COPY . .

RUN python -m venv /.venv && /.venv/bin/pip install --no-cache-dir -r requirements.txt

ENV PATH="/.venv/bin:$PATH"
ENV ENV="dev"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]