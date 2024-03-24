from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.requests import ProductCreateRequest
from app.schemas.responses import ProductResponse
from app.api import deps


router = APIRouter()


@router.post("/new", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: str,
    session: AsyncSession = Depends(deps.get_session),
):
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await session.delete(product)
    await session.commit()
