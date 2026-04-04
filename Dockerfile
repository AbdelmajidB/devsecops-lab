FROM python:3.11-slim
WORKDIR /app
COPY ../api .
RUN pip install flask
EXPOSE 5000
CMD ["python", "app.py"]
