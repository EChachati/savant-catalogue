from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from core.api.company import router as company_router

app = FastAPI()


@app.get("/")
def redirect_to_documentation():
    return RedirectResponse(url="/redoc")


app.include_router(
    company_router,
    prefix="/company",
    tags=["Company"],
)
