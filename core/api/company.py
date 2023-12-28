from fastapi import APIRouter, status
from sqlmodel_crud_manager.crud import CRUDManager

from core.sql.database import engine as db_engine
from core.sql.models.company import Company, CompanyCreate

router = APIRouter()

crud = CRUDManager(Company, db_engine)


@router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=Company)
def get_company(pk: int):
    """
    The function `get_company` retrieves a company object with the specified
    primary key.

    Arguments:
    * `pk`: The parameter `pk` is an integer that represents the primary key of
    a company. It is used to identify and retrieve a specific company from the
    database.

    Returns:
    the result of the `crud.get(pk)` function call.
    """
    return crud.get(pk)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Company)
def create_company(company: CompanyCreate):
    """
    The function `create_company` creates a new company using the provided data
    and returns the created company.

    Arguments:
    * `company`: The parameter `company` is of type `CompanyCreate`, which is a
    Pydantic model representing the data needed to create a new company. It is
    used to validate the incoming request payload and ensure that it contains
    all the required fields and has the correct data types.

    Returns:
    the result of the `crud.create(company)` function call.
    """
    return crud.create(company)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Company])
def list_companies():
    """
    The function `list_companies` returns a list of Company objects.

    Returns:
    a list of Company objects.
    """
    return crud.list()


@router.put("/", status_code=status.HTTP_200_OK, response_model=Company)
def update_company(company: Company):
    """
    The function `update_company` updates a company record and returns the
    updated company.

    Arguments:
    * `company`: The parameter `company` is of type `Company`, which is the
    model/schema for a company. It is used to represent the data of a company
    that needs to be updated.

    Returns:
    the result of the `crud.update(company)` function call.
    """
    return crud.update(company)


@router.delete("/{pk}", status_code=status.HTTP_200_OK, response_model=Company)
def delete_company(pk: int):
    """
    The above function is a DELETE endpoint that deletes a company with the
    specified primary key and returns the deleted company.

    Arguments:
    * `pk`: The parameter "pk" is an integer that represents the primary key of
    the company that needs to be deleted.

    Returns:
    the result of the `crud.delete(pk)` function call.
    """
    return crud.delete(pk)
