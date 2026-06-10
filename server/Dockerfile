FROM python:3.14-slim
WORKDIR /app
RUN pip install --no-cache-dir yt-dlp fastapi uvicorn
COPY . .
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
