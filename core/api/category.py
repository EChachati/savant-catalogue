from fastapi import APIRouter, status
from sqlmodel_crud_manager.crud import CRUDManager

from core.sql.database import engine as db_engine
from core.sql.models.category import Category, CategoryCreate

router = APIRouter()

crud = CRUDManager(Category, db_engine)


@router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=Category)
def get_category(pk: int):
    """
    The function `get_category` retrieves a category with the specified primary
    key.

    Arguments:
    * `pk`: The parameter "pk" is an integer that represents the primary key of
    the category you want to retrieve. It is used to identify and fetch the
    specific category from the database.

    Returns:
    the category object with the primary key (pk) specified in the URL path.
    """
    return crud.get(pk)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Category)
def create_category(category: CategoryCreate):
    """
    The above function creates a new category using the provided data and
    returns the created category.

    Arguments:
    * `category`: The parameter "category" is of type "CategoryCreate".
    It is used to receive the data for creating a new category.

    Returns:
    the result of the `crud.create(category)` function call.
    """
    return crud.create(category)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Category])
def list_companies():
    """
    The function `list_companies` returns a list of categories.

    Returns:
    a list of Category objects.
    """
    return crud.list()


@router.put("/", status_code=status.HTTP_200_OK, response_model=Category)
def update_category(category: Category):
    """
    The function `update_category` updates a category and returns the
    updated category.

    Arguments:
    * `category`: The parameter `category` is of type `Category`, which is the
    model/schema for the category data. It represents the category object that
    will be updated in the database.

    Returns:
    the result of the `crud.update(category)` function call.
    """
    return crud.update(category)


@router.delete("/{pk}", status_code=status.HTTP_200_OK, response_model=Category)
def delete_category(pk: int):
    """
    The above function is a DELETE endpoint that deletes a category with the
    specified primary key and returns the deleted category.

    Arguments:
    * `pk`: The parameter "pk" is an integer that represents the primary key of
    the category that needs to be deleted.

    Returns:
    the result of the `crud.delete(pk)` function call.
    """
    return crud.delete(pk)
