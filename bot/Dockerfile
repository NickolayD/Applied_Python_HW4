FROM python:3.8-slim
WORKDIR /bot
COPY requirements.txt requirements.txt
COPY requirements1.txt requirements1.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r requirements1.txt
COPY . .
CMD python bot.py
