from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.order import Order, OrderItem
from models.product import Product
from schemas.order import OrderCreate, OrderOut, OrderStatusUpdate
from routers.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderOut)
def place_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    total = 0.0
    order_items = []

    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock_qty < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")

        product.stock_qty -= item.quantity
        total += product.price * item.quantity
        order_items.append(OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price
        ))

    order = Order(
        user_id=current_user.id,
        total_price=round(total, 2),
        status="pending"
    )
    db.add(order)
    db.flush()

    for item in order_items:
        item.order_id = order.id
        db.add(item)

    db.commit()
    db.refresh(order)
    return order

@router.get("/mine", response_model=List[OrderOut])
def my_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Order).filter(Order.user_id == current_user.id).all()

@router.get("/", response_model=List[OrderOut])
def all_orders(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return db.query(Order).all()

@router.patch("/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    valid_statuses = ["pending", "confirmed", "shipped", "delivered"]
    if data.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of {valid_statuses}")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = data.status
    db.commit()
    db.refresh(order)
    return order