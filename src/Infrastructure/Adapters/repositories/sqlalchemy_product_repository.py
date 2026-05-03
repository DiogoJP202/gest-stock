from src.config.data_base import db
from src.Infrastructure.Model.product import Product, Sale

class SqlAlchemyProductRepository:
    def save(self, product_domain):
        # Converte Domain para Model do SQLAlchemy
        new_product = Product(
            nome=product_domain.nome,
            preco=product_domain.preco,
            quantidade_estoque=product_domain.quantidade_estoque,
            status=product_domain.status,
            imagem_url=product_domain.imagem_url,
            seller_id=product_domain.seller_id
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product

    def list_by_seller(self, seller_id):
        return Product.query.filter_by(seller_id=seller_id).all()

    def get_by_id(self, product_id):
        return Product.query.get(product_id)

    def register_sale(self, product_id, quantidade):
        product = Product.query.get(product_id)
        # RN: Abatendo o estoque
        product.quantidade_estoque -= quantidade
        
        # Criando o registro de venda
        nova_venda = Sale(
            product_id=product_id,
            quantidade=quantidade,
            preco_no_momento=product.preco
        )
        
        db.session.add(nova_venda)
        db.session.commit()
        return nova_venda