FROM python:3.12
WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

RUN pip install newrelic


COPY ./docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh

COPY . .

ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true

ENV NEW_RELIC_LOG_LEVEL=info

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
EXPOSE 3000
ENTRYPOINT ["newrelic-admin" ,"run-program" ]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]