FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN pip install --upgrade flask-restx

COPY . .

EXPOSE 5000

CMD [ "python3", "app.py"]
