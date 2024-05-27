FROM python:3.9.19-bookworm

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["reflex", "run"]