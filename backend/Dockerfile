FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml /app/
# pip fallback if not using poetry
RUN apt-get update && apt-get install -y build-essential
COPY src/ /app/src/
RUN pip install --upgrade pip
RUN pip install fastapi uvicorn python-multipart sentence-transformers faiss-cpu PyPDF2 openai aiofiles
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
