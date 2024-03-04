import httpx
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

if __name__ == "__main__":
    engine = create_engine(
        "mysql+pymysql://root:1234@127.0.0.1:3306/admin001000"
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    company_name = "Tiendas 10"
    query = """
    SELECT
        art.codigo as barcode,
        art.nombre as name,
        g.nombre as category,
        art.costoref as cost,
        art.costo,
        art.precio1,
        art.util1 as utility,
        art.impuesto as tax,
        art.factor as factor,
        art.existencia as stock,
        art.fechamodifi as updated_at,
        art.rutafoto as image
    from admin001000.articulo art
    INNER JOIN admin001000.grupos g on art.grupo = g.codigo;
    """

    data = db.execute(text(query)).all()
    df = pd.DataFrame(data)
    df["price"] = round(
        df["cost"] * (1 + (df["utility"] / 100)) * (1 + (df["tax"] / 100)), 2
    )
    df[["name", "category_id"]] = df[["name", "category"]].map(
        lambda x: x.title().replace("\\\\", "\\")
    )

    df["company_id"] = company_name

    df_products = df[
        [
            "barcode",
            "name",
            "category_id",
            "stock",
            "price",
            "company_id",
        ]
    ]
    df_images = df[["barcode", "image", "updated_at"]]

    res = httpx.post(
        "http://localhost:8000/product/create-multiple",
        json=df_products.to_dict(orient="records"),
        timeout=60,
    )
