FROM python:3.10
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
ENTRYPOINT ["python3", "app.py"]