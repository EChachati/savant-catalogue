import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()
DATABASE_URL = os.environ["DB_URI"]


engine = create_engine(DATABASE_URL, echo=True)


def get_db():
    with Session(engine) as session:
        yield session
