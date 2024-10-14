FROM python:3.11-buster
WORKDIR /app

RUN pip install poetry
COPY . .
RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "python3", "-m", "backend"]
