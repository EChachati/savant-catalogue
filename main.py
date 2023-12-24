from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from core.api.category import router as category_router
from core.api.company import router as company_router
from core.api.product import router as product_router

app = FastAPI()


@app.get("/")
def redirect_to_documentation():
    return RedirectResponse(url="/redoc")


app.include_router(
    company_router,
    prefix="/company",
    tags=["Company"],
)

app.include_router(
    category_router,
    prefix="/category",
    tags=["Category"],
)

app.include_router(
    product_router,
    prefix="/product",
    tags=["Product"],
)
