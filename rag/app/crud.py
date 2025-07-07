from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app.models import Product, Sale

def get_top_products_last_month(db: Session, limit: int = 5):
    last_month = datetime.now() - timedelta(days=30)
    results = (
        db.query(
            Product.name,
            func.sum(Sale.quantity).label("total_quantity")
        )
        .join(Sale, Sale.product_id == Product.id)
        .filter(Sale.sale_date >= last_month)
        .group_by(Product.name)
        .order_by(desc("total_quantity"))
        .limit(limit)
        .all()
    )
    return [{"product_name": name, "total_quantity": qty} for name, qty in results]
