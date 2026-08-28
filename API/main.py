'''
Patrick Prado - 22552018, Bruno Monteiro - 22305939, Samuel Correa Abreu - 22650765, Pedro Postay - 22308711
'''
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json

from bd import get_connection, create_tables
from models.user import User
from models.address import Address
from models.category import Category
from models.coupon import Coupon
from models.OptionGroup import OptionGroup
from models.order import Order
from models.payment import Payment
from models.product import Product
from models.review import Review
from models.table import Table

app = FastAPI(title="67food")

# Cria as tabelas do banco ao ligar o servidor
@app.on_event("startup")
def startup_event():
    create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 1. BLOCO: USUÁRIOS E AUTENTICAÇÃO
# ==========================================

@app.post("/users", tags=["Usuários"], status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, email, role) VALUES (?, ?, ?)",
            (user.name, user.email, user.role)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, "name": user.name, "email": user.email, "role": user.role}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar usuário: {str(e)}")
    finally:
        conn.close()

@app.get("/users", tags=["Usuários"])
def get_users(role: Optional[str] = None):
    conn = get_connection()
    cursor = conn.cursor()
    if role:
        cursor.execute("SELECT * FROM users WHERE role = ?", (role,))
    else:
        cursor.execute("SELECT * FROM users")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users

@app.get("/users/{user_id}", tags=["Usuários"])
def get_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return dict(row)

@app.put("/users/{user_id}", tags=["Usuários"])
def update_user(user_id: int, user: User):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name = ?, email = ?, role = ? WHERE id = ?",
        (user.name, user.email, user.role, user_id)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": f"Usuário {user_id} atualizado com sucesso"}

@app.delete("/users/{user_id}", tags=["Usuários"])
def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": f"Usuário {user_id} removido com sucesso"}


# Endereços
@app.post("/users/{user_id}/addresses", tags=["Endereços"], status_code=status.HTTP_201_CREATED)
def create_address(user_id: int, address: Address):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO addresses (user_id, street, number, complement, city) VALUES (?, ?, ?, ?, ?)",
            (user_id, address.street, address.number, address.complement, address.city)
        )
        conn.commit()
        address_id = cursor.lastrowid
        return {"id": address_id, "user_id": user_id, **address.model_dump()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao cadastrar endereço: {str(e)}")
    finally:
        conn.close()

@app.get("/users/{user_id}/addresses", tags=["Endereços"])
def get_addresses(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM addresses WHERE user_id = ?", (user_id,))
    addresses = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return addresses

@app.get("/addresses/{address_id}", tags=["Endereços"])
def get_address(address_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM addresses WHERE id = ?", (address_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return dict(row)

@app.put("/addresses/{address_id}", tags=["Endereços"])
def update_address(address_id: int, address: Address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE addresses SET street = ?, number = ?, complement = ?, city = ? WHERE id = ?",
        (address.street, address.number, address.complement, address.city, address_id)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return {"message": f"Endereço {address_id} atualizado com sucesso"}

@app.delete("/addresses/{address_id}", tags=["Endereços"])
def delete_address(address_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM addresses WHERE id = ?", (address_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return {"message": f"Endereço {address_id} removido"}


# ==========================================
# 2. BLOCO: CARDÁPIO E ESTOQUE
# ==========================================

@app.post("/categories", tags=["Categorias"], status_code=status.HTTP_201_CREATED)
def create_category(category: Category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (name, active) VALUES (?, ?)", (category.name, category.active))
    conn.commit()
    cat_id = cursor.lastrowid
    conn.close()
    return {"id": cat_id, **category.model_dump()}

@app.get("/categories", tags=["Categorias"])
def get_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    categories = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return categories

@app.get("/categories/{category_id}", tags=["Categorias"])
def get_category(category_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return dict(row)

@app.put("/categories/{category_id}", tags=["Categorias"])
def update_category(category_id: int, category: Category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE categories SET name = ?, active = ? WHERE id = ?",
        (category.name, category.active, category_id)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return {"message": f"Categoria {category_id} atualizada"}

@app.delete("/categories/{category_id}", tags=["Categorias"])
def delete_category(category_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return {"message": f"Categoria {category_id} removida"}


# Produtos
@app.post("/products", tags=["Produtos"], status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO products (name, price, category_id, description) VALUES (?, ?, ?, ?)",
            (product.name, product.price, product.category_id, product.description)
        )
        conn.commit()
        prod_id = cursor.lastrowid
        return {"id": prod_id, **product.model_dump()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar produto: {str(e)}")
    finally:
        conn.close()

@app.get("/products", tags=["Produtos"])
def get_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return products

@app.get("/products/{product_id}", tags=["Produtos"])
def get_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return dict(row)

@app.put("/products/{product_id}", tags=["Produtos"])
def update_product(product_id: int, product: Product):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE products SET name = ?, price = ?, category_id = ?, description = ? WHERE id = ?",
        (product.name, product.price, product.category_id, product.description, product_id)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": f"Produto {product_id} atualizado"}

@app.delete("/products/{product_id}", tags=["Produtos"])
def delete_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": f"Produto {product_id} excluído"}


# Opções e Adicionais
@app.post("/products/{product_id}/option-groups", tags=["Opções e Adicionais"], status_code=status.HTTP_201_CREATED)
def create_option_group(product_id: int, option: OptionGroup):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO option_groups (product_id, name, min_options, max_options) VALUES (?, ?, ?, ?)",
        (product_id, option.name, option.min_options, option.max_options)
    )
    conn.commit()
    opt_id = cursor.lastrowid
    conn.close()
    return {"id": opt_id, "product_id": product_id, **option.model_dump()}

@app.get("/products/{product_id}/option-groups", tags=["Opções e Adicionais"])
def get_product_option_groups(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM option_groups WHERE product_id = ?", (product_id,))
    options = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return options

@app.get("/option-groups/{option_id}", tags=["Opções e Adicionais"])
def get_option_group(option_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM option_groups WHERE id = ?", (option_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Opção não encontrada")
    return dict(row)

@app.put("/option-groups/{option_id}", tags=["Opções e Adicionais"])
def update_option_group(option_id: int, option: OptionGroup):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE option_groups SET name = ?, min_options = ?, max_options = ? WHERE id = ?",
        (option.name, option.min_options, option.max_options, option_id)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Opção não encontrada")
    return {"message": f"Opção {option_id} atualizada"}

@app.delete("/option-groups/{option_id}", tags=["Opções e Adicionais"])
def delete_option_group(option_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM option_groups WHERE id = ?", (option_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Opção não encontrada")
    return {"message": f"Opção {option_id} removida"}


# ==========================================
# 3. BLOCO: MESAS E OPERAÇÃO LOCAL
# ==========================================

@app.post("/tables", tags=["Mesas"], status_code=status.HTTP_201_CREATED)
def create_table(table: Table):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        data = table.model_dump()
        cursor.execute("INSERT INTO tables (number, status) VALUES (?, ?)", (data.get("number", 0), data.get("status", "Livre")))
        conn.commit()
        table_id = cursor.lastrowid
        return {"id": table_id, **data}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar mesa: {str(e)}")
    finally:
        conn.close()

@app.get("/tables", tags=["Mesas"])
def get_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tables")
    tables = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return tables

@app.get("/tables/{table_id}", tags=["Mesas"])
def get_table(table_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tables WHERE id = ?", (table_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    return dict(row)

@app.put("/tables/{table_id}", tags=["Mesas"])
def update_table(table_id: int, table: Table):
    conn = get_connection()
    cursor = conn.cursor()
    data = table.model_dump()
    cursor.execute("UPDATE tables SET number = ?, status = ? WHERE id = ?", (data.get("number"), data.get("status"), table_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    return {"message": f"Mesa {table_id} atualizada"}

@app.delete("/tables/{table_id}", tags=["Mesas"])
def delete_table(table_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tables WHERE id = ?", (table_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    return {"message": f"Mesa {table_id} removida"}


# ==========================================
# 4. BLOCO: PEDIDOS E ATENDIMENTO
# ==========================================

@app.post("/orders", tags=["Pedidos"], status_code=status.HTTP_201_CREATED)
def create_order(order: Order):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        items_as_text = json.dumps(order.items)
        cursor.execute(
            "INSERT INTO orders (user_id, total, status, items_json) VALUES (?, ?, ?, ?)",
            (order.user_id, order.total, order.status, items_as_text)
        )
        conn.commit()
        order_id = cursor.lastrowid
        return {"id": order_id, **order.model_dump()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao realizar pedido: {str(e)}")
    finally:
        conn.close()

@app.get("/orders", tags=["Pedidos"])
def get_orders(status_filter: Optional[str] = None):
    conn = get_connection()
    cursor = conn.cursor()
    if status_filter:
        cursor.execute("SELECT * FROM orders WHERE status = ?", (status_filter,))
    else:
        cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    orders = []
    for r in rows:
        item = dict(r)
        item["items"] = json.loads(item["items_json"]) if item["items_json"] else []
        del item["items_json"]
        orders.append(item)
    conn.close()
    return orders

@app.get("/orders/{order_id}", tags=["Pedidos"])
def get_order(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    order = dict(row)
    order["items"] = json.loads(order["items_json"]) if order["items_json"] else []
    del order["items_json"]
    return order

@app.put("/orders/{order_id}", tags=["Pedidos"])
def update_order(order_id: int, order: Order):
    conn = get_connection()
    cursor = conn.cursor()
    items_as_text = json.dumps(order.items)
    cursor.execute(
        "UPDATE orders SET user_id = ?, total = ?, status = ?, items_json = ? WHERE id = ?",
        (order.user_id, order.total, order.status, items_as_text, order_id)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"message": f"Pedido {order_id} atualizado com sucesso"}

@app.delete("/orders/{order_id}", tags=["Pedidos"])
def delete_order(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"message": f"Pedido {order_id} cancelado/estornado"}


# ==========================================
# 5. BLOCO: PAGAMENTOS E FATURAMENTO
# ==========================================

@app.post("/orders/{order_id}/payments", tags=["Pagamentos"], status_code=status.HTTP_201_CREATED)
def create_payment(order_id: int, payment: Payment):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO payments (order_id, method, amount) VALUES (?, ?, ?)",
            (order_id, payment.method, payment.amount)
        )
        conn.commit()
        pay_id = cursor.lastrowid
        return {"id": pay_id, "order_id": order_id, **payment.model_dump()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao registrar pagamento: {str(e)}")
    finally:
        conn.close()

@app.get("/payments", tags=["Pagamentos"])
def get_payments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payments")
    payments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return payments

@app.get("/payments/{payment_id}", tags=["Pagamentos"])
def get_payment(payment_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payments WHERE id = ?", (payment_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return dict(row)

@app.delete("/payments/{payment_id}", tags=["Pagamentos"])
def delete_payment(payment_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM payments WHERE id = ?", (payment_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return {"message": f"Pagamento {payment_id} cancelado"}


# ==========================================
# 6. BLOCO: AVALIAÇÕES E FIDELIDADE
# ==========================================

@app.post("/orders/{order_id}/reviews", tags=["Avaliações"], status_code=status.HTTP_201_CREATED)
def create_review(order_id: int, review: Review):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO reviews (order_id, rating, comment) VALUES (?, ?, ?)",
            (order_id, review.rating, review.comment)
        )
        conn.commit()
        rev_id = cursor.lastrowid
        return {"id": rev_id, "order_id": order_id, **review.model_dump()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar avaliação: {str(e)}")
    finally:
        conn.close()

@app.get("/reviews", tags=["Avaliações"])
def get_reviews():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews")
    reviews = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return reviews

@app.get("/reviews/{review_id}", tags=["Avaliações"])
def get_review(review_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return dict(row)

@app.delete("/reviews/{review_id}", tags=["Avaliações"])
def delete_review(review_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return {"message": f"Avaliação {review_id} removida"}


# Cupons
@app.post("/coupons", tags=["Cupons"], status_code=status.HTTP_201_CREATED)
def create_coupon(coupon: Coupon):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO coupons (code, discount_percentage, active) VALUES (?, ?, ?)",
            (coupon.code, coupon.discount_percentage, coupon.active)
        )
        conn.commit()
        cupom_id = cursor.lastrowid
        return {"id": cupom_id, **coupon.model_dump()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao cadastrar cupom: {str(e)}")
    finally:
        conn.close()

@app.get("/coupons", tags=["Cupons"])
def get_coupons():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coupons")
    coupons = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return coupons

@app.get("/coupons/{coupon_id}", tags=["Cupons"])
def get_coupon(coupon_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coupons WHERE id = ?", (coupon_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return dict(row)

@app.put("/coupons/{coupon_id}", tags=["Cupons"])
def update_coupon(coupon_id: int, coupon: Coupon):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE coupons SET code = ?, discount_percentage = ?, active = ? WHERE id = ?",
        (coupon.code, coupon.discount_percentage, coupon.active, coupon_id)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return {"message": f"Cupom {coupon_id} atualizado"}

@app.delete("/coupons/{coupon_id}", tags=["Cupons"])
def delete_coupon(coupon_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM coupons WHERE id = ?", (coupon_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return {"message": f"Cupom {coupon_id} desativado"}
