from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.crud import get_top_products_last_month
from app.rag import run_rag_query

app = FastAPI(title="Sales Insights API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/top-products")
def top_products(db: Session = Depends(get_db)):
    return get_top_products_last_month(db)

@app.get("/sales-insights")
def sales_insights(question: str = Query(..., min_length=10)):
    try:
        response = run_rag_query(question)
        return {"question": question, "answer": response}
    except Exception as e:
        return {"error": str(e)}
