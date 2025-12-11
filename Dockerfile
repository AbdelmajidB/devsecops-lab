FROM python:3.13-alpine
WORKDIR /app
COPY api/ ./api/
RUN pip install flask
EXPOSE 5000
CMD ["python", "api/app.py"]
