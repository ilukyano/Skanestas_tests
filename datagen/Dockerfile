FROM python:3.9.15-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY datagen.py ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./datagen.py" ]