FROM python:3.11-slim

WORKDIR /app
COPY ./src/poetry.lock ./src/pyproject.toml ./src/run.sh ./

RUN python -m pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY ./src/ ./

RUN chmod +x ./run.sh

EXPOSE 7777

CMD ["./run.sh"]
