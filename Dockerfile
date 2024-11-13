FROM python:3.12
WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy


COPY ./docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh

COPY . .


RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
EXPOSE 3000
ENTRYPOINT ["/bin/sh", "./docker-entrypoint.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]