FROM python:3.6

# expone el puerto del container, no se puede acceder directamente a el.
EXPOSE 5000

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD python3 api4.py
