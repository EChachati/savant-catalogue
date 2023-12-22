from dataclasses import dataclass
from typing import TypeVar

from sqlmodel import Session, SQLModel, select
from sqlmodel.sql.expression import Select

from core.sql.database import engine

ModelType = TypeVar("ModelType", bound=SQLModel)
ModelCreateType = TypeVar("ModelCreateType", bound=SQLModel)
QueryLike = TypeVar("QueryLike", bound=Select)


@dataclass
class CRUD:
    # The above class provides basic CRUD operations for a given model using a
    # database session.
    model: ModelType

    def __init__(self, model: ModelType):
        """
        The function initializes an object with a model and a database session.

        Arguments:

        * `model`: The model object represents a specific model or entity in the
        application. It could be a database model, a machine learning model, or
        any other type of model
        """
        self.model = model
        self.db = Session(engine)

    def create(self, object: ModelCreateType) -> ModelType:
        """
        The function creates a new object in the database and returns it.

        Arguments:

        * `object`: The "object" parameter is of type ModelCreateType, which is
        the type of the object that you want to create.

        Returns:

        The `create` method is returning an object of type `ModelType`.
        """
        with self.db:
            obj = self.model.model_validate(object)
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
        return obj

    def list(self, query: QueryLike = None) -> list[ModelType]:
        """
        The function returns a list of all the records in the database that
        match the given query.

        Arguments:

        * `query`: The `query` parameter is an optional argument of type
        `QueryLike`. It represents a query that will be executed on the
        database. If no query is provided, the function will use a default
        query that selects all records from the `ModelType` table.

        Returns:

        a list of objects of type `ModelType`.
        """
        if query is None:
            query = select(self.model)
        return self.db.exec(query).all()

    def get(self, pk: int) -> ModelType:
        """
        The function retrieves a model instance from the database based on its
        primary key.

        Arguments:

        * `pk`: The parameter "pk" stands for "primary key" and it is of type
        "int". It is used to specify the primary key value of the model
        instance that we want to retrieve from the database.

        Returns:

        The `get` method is returning an instance of `ModelType` that matches
        the given primary key `pk`.
        """
        query = select(self.model).where(self.model.id == pk)
        return self.db.exec(query)
