'''
Patrick Prado - 22552018, Bruno Monteiro - 22305939, Samuel Correa Abreu - 22650765, Pedro Postay - 22308711
'''


from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

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
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="67food")


users = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================
# X. Teste
# =======================

class TesteFront(BaseModel):
    nome: str
    localizacao: str


@app.post("/teste-front")
def teste_front(dados: TesteFront):
    return {
        "message": "Dados recebidos com sucesso",
        "nome": dados.nome,
        "localizacao": dados.localizacao
    }

# ==========================================
# 1. BLOCO: USUÁRIOS E AUTENTICAÇÃO
# ==========================================

@app.post("/users", tags=["Usuários"])
def create_user(user: User) -> dict:
    """Cadastrar novo usuário"""
    users.append(user)
    return {"message": "Usuário criado com sucesso", "data": user}

@app.get("/users", tags=["Usuários"])
def get_users(role: Optional[str] = None) -> list[User]:
    """Listar usuários (com filtro opcional por função)"""
    return users

@app.get("/users/{user_id}", tags=["Usuários"])
def get_user(user_id: int):
    """Obter dados do perfil de um usuário específico"""
    return {"id": user_id, "name": "João Silva", "email": "joao@email.com"}

@app.put("/users/{user_id}", tags=["Usuários"])
def update_user(user_id: int, user: User):
    """Atualizar dados do perfil"""
    return {"message": f"Usuário {user_id} atualizado com sucesso"}

@app.delete("/users/{user_id}", tags=["Usuários"])
def delete_user(user_id: int):
    """Desativar ou excluir a conta do usuário"""
    return {"message": f"Usuário {user_id} removido com sucesso"}


@app.post("/users/{user_id}/addresses", tags=["Endereços"])
def create_address(user_id: int, address: Address):
    """Cadastrar novo endereço"""
    return {"message": f"Endereço cadastrado para o usuário {user_id}"}

@app.get("/users/{user_id}/addresses", tags=["Endereços"])
def get_addresses(user_id: int):
    """Listar endereços do cliente"""
    return [{"id": 1, "user_id": user_id, "street": "Rua das Flores", "number": "123"}]

@app.get("/addresses/{address_id}", tags=["Endereços"])
def get_address(address_id: int):
    """Detalhes de um endereço específico"""
    return {"id": address_id, "street": "Rua das Flores", "number": "123"}

@app.put("/addresses/{address_id}", tags=["Endereços"])
def update_address(address_id: int, address: Address):
    """Atualizar logradouro, número ou complemento"""
    return {"message": f"Endereço {address_id} atualizado"}

@app.delete("/addresses/{address_id}", tags=["Endereços"])
def delete_address(address_id: int):
    """Remover endereço do cadastro"""
    return {"message": f"Endereço {address_id} removido"}


# ==========================================
# 2. BLOCO: CARDÁPIO E ESTOQUE
# ==========================================

@app.post("/categories", tags=["Categorias"])
def create_category(category: Category):
    """Criar nova categoria"""
    return {"message": "Categoria criada", "data": category}

@app.get("/categories", tags=["Categorias"])
def get_categories():
    """Listar todas as categorias ativas no cardápio"""
    return [{"id": 1, "name": "Entradas"}, {"id": 2, "name": "Pratos Principais"}]

@app.get("/categories/{category_id}", tags=["Categorias"])
def get_category(category_id: int):
    """Detalhar uma categoria específica"""
    return {"id": category_id, "name": "Pratos Principais"}

@app.put("/categories/{category_id}", tags=["Categorias"])
def update_category(category_id: int, category: Category):
    """Alterar nome, ordem de exibição ou status"""
    return {"message": f"Categoria {category_id} atualizada"}

@app.delete("/categories/{category_id}", tags=["Categorias"])
def delete_category(category_id: int):
    """Remover uma categoria do menu"""
    return {"message": f"Categoria {category_id} removida"}


@app.post("/products", tags=["Produtos"])
def create_product(product: Product):
    """Cadastrar novo produto no cardápio"""
    return {"message": "Produto cadastrado", "data": product}

@app.get("/products", tags=["Produtos"])
def get_products():
    """Listar todos os produtos"""
    return [{"id": 1, "name": "X-Burger", "price": 25.00}]

@app.get("/products/{product_id}", tags=["Produtos"])
def get_product(product_id: int):
    """Ver detalhes do produto"""
    return {"id": product_id, "name": "X-Burger", "price": 25.00}

@app.put("/products/{product_id}", tags=["Produtos"])
def update_product(product_id: int, product: Product):
    """Atualizar preço, descrição ou pausar venda"""
    return {"message": f"Produto {product_id} atualizado"}

@app.delete("/products/{product_id}", tags=["Produtos"])
def delete_product(product_id: int):
    """Excluir produto do sistema"""
    return {"message": f"Produto {product_id} excluído"}


@app.post("/products/{product_id}/option-groups", tags=["Opções e Adicionais"])
def create_option_group(product_id: int, option: OptionGroup):
    """Vincular grupo de complementos a um produto"""
    return {"message": f"Opção adicionada ao produto {product_id}"}

@app.get("/products/{product_id}/option-groups", tags=["Opções e Adicionais"])
def get_product_option_groups(product_id: int):
    """Listar opções disponíveis para o produto"""
    return [{"id": 1, "product_id": product_id, "name": "Ponto da carne"}]

@app.get("/option-groups/{option_id}", tags=["Opções e Adicionais"])
def get_option_group(option_id: int):
    """Detalhar regras da opção"""
    return {"id": option_id, "name": "Ponto da carne", "min": 1, "max": 1}

@app.put("/option-groups/{option_id}", tags=["Opções e Adicionais"])
def update_option_group(option_id: int, option: OptionGroup):
    """Editar preços ou nomes das opções"""
    return {"message": f"Opção {option_id} atualizada"}

@app.delete("/option-groups/{option_id}", tags=["Opções e Adicionais"])
def delete_option_group(option_id: int):
    """Remover grupo de adicionais"""
    return {"message": f"Opção {option_id} removida"}


# ==========================================
# 3. BLOCO: MESAS E OPERAÇÃO LOCAL
# ==========================================

@app.post("/tables", tags=["Mesas"])
def create_table(table: Table):
    """Cadastrar nova mesa"""
    return {"message": "Mesa cadastrada com sucesso", "data": table}

@app.get("/tables", tags=["Mesas"])
def get_tables():
    """Listar status de todas as mesas"""
    return [{"id": 1, "number": 10, "status": "Livre"}]

@app.get("/tables/{table_id}", tags=["Mesas"])
def get_table(table_id: int):
    """Consultar detalhes e comanda atual da mesa"""
    return {"id": table_id, "number": 10, "status": "Ocupada", "order_id": 42}

@app.put("/tables/{table_id}", tags=["Mesas"])
def update_table(table_id: int, table: Table):
    """Alterar status da mesa ou atualizar QR Code"""
    return {"message": f"Mesa {table_id} atualizada"}

@app.delete("/tables/{table_id}", tags=["Mesas"])
def delete_table(table_id: int):
    """Remover mesa do mapa do restaurante"""
    return {"message": f"Mesa {table_id} removida"}


# ==========================================
# 4. BLOCO: PEDIDOS E ATENDIMENTO
# ==========================================

@app.post("/orders", tags=["Pedidos"])
def create_order(order: Order):
    """Criar um novo pedido"""
    return {"message": "Pedido realizado com sucesso", "data": order}

@app.get("/orders", tags=["Pedidos"])
def get_orders(status_filter: Optional[str] = None):
    """Listar pedidos (com filtro opcional por status)"""
    return [{"id": 100, "status": status_filter or "Pendente", "total": 45.90}]

@app.get("/orders/{order_id}", tags=["Pedidos"])
def get_order(order_id: int):
    """Detalhes completos do pedido"""
    return {"id": order_id, "items": ["X-Burger", "Refrigerante"], "total": 45.90}

@app.put("/orders/{order_id}", tags=["Pedidos"])
def update_order(order_id: int, order: Order):
    """Atualizar status do pedido ou cancelar"""
    return {"message": f"Pedido {order_id} atualizado"}

@app.delete("/orders/{order_id}", tags=["Pedidos"])
def delete_order(order_id: int):
    """Cancelar/Estornar pedido"""
    return {"message": f"Pedido {order_id} estornado"}


# ==========================================
# 5. BLOCO: PAGAMENTOS E FATURAMENTO
# ==========================================

@app.post("/orders/{order_id}/payments", tags=["Pagamentos"])
def create_payment(order_id: int, payment: Payment):
    """Registrar tentativa de pagamento"""
    return {"message": f"Pagamento registrado para o pedido {order_id}"}

@app.get("/payments", tags=["Pagamentos"])
def get_payments():
    """Listar histórico financeiro de transações"""
    return [{"id": 1, "order_id": 100, "method": "Pix", "amount": 45.90}]

@app.get("/payments/{payment_id}", tags=["Pagamentos"])
def get_payment(payment_id: int):
    """Detalhes de uma transação específica"""
    return {"id": payment_id, "method": "Pix", "status": "Aprovado"}

@app.put("/payments/{payment_id}", tags=["Pagamentos"])
def update_payment(payment_id: int, payment: Payment):
    """Atualizar status do pagamento"""
    return {"message": f"Pagamento {payment_id} atualizado"}

@app.delete("/payments/{payment_id}", tags=["Pagamentos"])
def delete_payment(payment_id: int):
    """Cancelar registro de pagamento"""
    return {"message": f"Pagamento {payment_id} cancelado"}


# ==========================================
# 6. BLOCO: AVALIAÇÕES E FIDELIDADE
# ==========================================

@app.post("/orders/{order_id}/reviews", tags=["Avaliações"])
def create_review(order_id: int, review: Review):
    """Enviar avaliação do pedido"""
    return {"message": f"Avaliação registrada para o pedido {order_id}"}

@app.get("/reviews", tags=["Avaliações"])
def get_reviews():
    """Listar todas as avaliações recebidas"""
    return [{"id": 1, "order_id": 100, "rating": 5, "comment": "Excelente!"}]

@app.get("/reviews/{review_id}", tags=["Avaliações"])
def get_review(review_id: int):
    """Ver detalhes de uma avaliação individual"""
    return {"id": review_id, "rating": 5, "comment": "Comida maravilhosa"}

@app.put("/reviews/{review_id}", tags=["Avaliações"])
def update_review(review_id: int, review: Review):
    """Responder comentário"""
    return {"message": f"Resposta à avaliação {review_id} salva"}

@app.delete("/reviews/{review_id}", tags=["Avaliações"])
def delete_review(review_id: int):
    """Remover avaliação imprópria"""
    return {"message": f"Avaliação {review_id} removida"}


@app.post("/coupons", tags=["Cupons"])
def create_coupon(coupon: Coupon):
    """Criar novo cupom promocional"""
    return {"message": "Cupom criado", "data": coupon}

@app.get("/coupons", tags=["Cupons"])
def get_coupons():
    """Listar cupons ativos"""
    return [{"id": 1, "code": "PRIMEIRACOMPRA", "discount": 10.0}]

@app.get("/coupons/{coupon_id}", tags=["Cupons"])
def get_coupon(coupon_id: int):
    """Verificar regras e validade do cupom"""
    return {"id": coupon_id, "code": "PRIMEIRACOMPRA", "discount": 10.0}

@app.put("/coupons/{coupon_id}", tags=["Cupons"])
def update_coupon(coupon_id: int, coupon: Coupon):
    """Alterar validade ou valor de desconto"""
    return {"message": f"Cupom {coupon_id} atualizado"}

@app.delete("/coupons/{coupon_id}", tags=["Cupons"])
def delete_coupon(coupon_id: int):
    """Inativar cupom"""
    return {"message": f"Cupom {coupon_id} desativado"}
