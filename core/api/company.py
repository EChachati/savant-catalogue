from fastapi import APIRouter, status

from core.controllers.crud import CRUD
from core.sql.models import Company, CompanyCreate

router = APIRouter()

crud = CRUD(Company)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Company)
def create_company(company: CompanyCreate):
    return crud.create(company)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Company])
def list_companies():
    return crud.list()


@router.put("/", status_code=status.HTTP_200_OK, response_model=Company)
def update_company(company: Company):
    return crud.update(company)


@router.delete("/{pk}")
def delete_company(pk: int):
    return crud.delete(pk)
