from fastapi import APIRouter, status
from sqlmodel_crud_manager.crud import CRUDManager

from core.sql.database import engine as db_engine
from core.sql.models.company import Company, CompanyCreate

router = APIRouter()

crud = CRUDManager(Company, db_engine)


@router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=Company)
def get_company(pk: int):
    return crud.get(pk)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Company)
def create_company(company: CompanyCreate):
    return crud.create(company)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Company])
def list_companies():
    return crud.list()


@router.put("/", status_code=status.HTTP_200_OK, response_model=Company)
def update_company(company: Company):
    return crud.update(company)


@router.delete("/{pk}", status_code=status.HTTP_200_OK, response_model=Company)
def delete_company(pk: int):
    return crud.delete(pk)
