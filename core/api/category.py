from fastapi import APIRouter, status
from sqlmodel_crud_manager.crud import CRUDManager

from core.sql.database import engine as db_engine
from core.sql.models.category import Category, CategoryCreate

router = APIRouter()

crud = CRUDManager(Category, db_engine)


@router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=Category)
def get_category(pk: int):
    return crud.get(pk)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Category)
def create_category(category: CategoryCreate):
    return crud.create(category)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Category])
def list_companies():
    return crud.list()


@router.put("/", status_code=status.HTTP_200_OK, response_model=Category)
def update_category(category: Category):
    return crud.update(category)


@router.delete("/{pk}", status_code=status.HTTP_200_OK, response_model=Category)
def delete_category(pk: int):
    return crud.delete(pk)
