FROM python:3.9

WORKDIR ./
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "./app.py"]