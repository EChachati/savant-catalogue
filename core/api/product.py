from fastapi import APIRouter, BackgroundTasks, File, UploadFile, status
from sqlmodel import select
from sqlmodel_crud_manager.crud import CRUDManager

from core.controllers.media import FileHandler
from core.sql.database import engine as db_engine
from core.sql.models.product import Product, ProductCreate, ProductResponse

router = APIRouter()

crud = CRUDManager(Product, db_engine)


@router.get(
    "/{pk}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
)
def get_product(pk: int):
    """
    The function `get_product` retrieves a product with the specified primary
    key.

    Arguments:
    * `pk`: The parameter "pk" is of type int and represents the primary key of
    the product that we want to retrieve. It is used to uniquely identify the
    product in the database.

    Returns:
    the product with the primary key (pk) specified in the URL path.
    """
    return crud.get(pk)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponse,
)
def create_product(product: ProductCreate):
    """
    The function `create_product` creates a new product using the data provided
    in the `product` parameter and returns the created product.

    Arguments:
    * `product`: The parameter `product` is of type `ProductCreate`, which is
    a Pydantic model representing the data required to create a new product.

    Returns:
    the result of the `crud.create(product)` function call.
    """
    return crud.create(product)


@router.post(
    "/create-multiple",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
)
async def create_products(
    products: list[ProductCreate],
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        crud.create_or_update_multiple_by_fields,
        products,
        ["barcode", "company_id"],
    )
    return {"message": "Products are being created and updated"}


@router.post(
    "/{pk}/upload-image",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
)
async def upload_image(pk: int, image: UploadFile = File(...)):
    product: Product = crud.get(pk)
    img = FileHandler(
        image,
        filename=f"{product.barcode}_{product.company.name}_product_"
        f"{product.name.lower()}.png".replace(" ", "_"),
    )
    await img.upload_file()
    product.image = img.get_public_url()
    crud.update(product)

    return {"message": "Image uploaded successfully"}


@router.post(
    "/{company_id}/{barcode}/upload-image",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
)
async def upload_img_using_barcode(
    barcode: str,
    company_id: int,
    image: UploadFile = File(...),
):
    product: Product = crud.get_by_fields(
        {"barcode": barcode, "company_id": company_id}
    )
    img = FileHandler(
        image,
        filename=f"{product.barcode}_{product.company.name}_product_"
        f"{product.name.lower()}.png".replace(" ", "_"),
    )
    await img.upload_file()
    product.image = img.get_public_url()
    crud.update(product)
    return {"message": "Image uploaded successfully"}


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ProductResponse],
)
def list_products(
    company_id: int | None = None,
    category_id: int | None = None,
):
    """
    The function `list_products` retrieves a list of products based on optional
    filters for company ID and category ID.

    Arguments:
    * `company_id`: The `company_id` parameter is an optional integer that
    represents the ID of a company. If provided, the function will filter the
    products based on the company ID.
    * `category_id`: The `category_id` parameter is used to filter the products
    by a specific category. If a `category_id` is provided, the query will
    include a condition to only select products that have a matching
    `category_id`.

    Returns:
    a list of products.
    """
    query = select(Product).where(Product.stock > 0)
    if company_id:
        query = query.where(Product.company_id == company_id)
    if category_id:
        query = query.where(Product.category_id == category_id)
    return crud.db.exec(query).all()


@router.put("/", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def update_product(product: Product):
    """
    The function `update_product` updates a product and returns the updated
    product.

    Arguments:
    * `product`: The parameter `product` is of type `Product`, which is the
    model/schema for a product. It is used to represent the data of a product
    that needs to be updated.

    Returns:
    the result of the `crud.update(product)` function call.
    """
    return crud.update(product)


@router.delete(
    "/{pk}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
)
def delete_product(pk: int):
    """
    The above function is a DELETE endpoint that deletes a product with the
    specified primary key and returns the deleted product.

    Arguments:
    * `pk`: The "pk" parameter in the delete_product function represents the
    primary key of the product that needs to be deleted. It is of type int,
    indicating that it should be an integer value.

    Returns:
    the result of the `crud.delete(pk)` function call.
    """
    return crud.delete(pk)
