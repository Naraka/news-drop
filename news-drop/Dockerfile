FROM python:3.10
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
