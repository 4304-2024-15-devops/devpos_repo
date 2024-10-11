
## Ejecución
Require pippenv y python 3.12

Requiere las siguientes variables de entorno
```
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
BEARER_TOKEN=
```
```bash
pipenv install
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Tests

```
pytests tests
pytest --cov=. -v -s --cov-fail-under=70
```