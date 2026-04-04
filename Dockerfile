FROM python:3.14.3-slim-trixie
WORKDIR /app
COPY ../api .
RUN pip install flask
EXPOSE 5000
CMD ["python", "app.py"]
