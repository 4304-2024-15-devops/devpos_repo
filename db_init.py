#  Try to init the database
import time
import models
from database import engine

MAX_TRIES = 3
SLEEP = 1


def init_db():
    models.Base.metadata.create_all(bind=engine)


for i in range(MAX_TRIES):
    try:
        init_db()
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(SLEEP)
