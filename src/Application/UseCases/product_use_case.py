class ProductUseCase:
    def __init__(self, product_repository, user_repository):
        self.product_repository = product_repository
        self.user_repository = user_repository

    def cadastrar_produto(self, seller_id, data):
        # O seller precisa existir e estar ativo (opcional, mas boa prática)
        return self.product_repository.save(seller_id, data)

    def listar_produtos(self, seller_id):
        return self.product_repository.list_by_seller(seller_id)

    def realizar_venda(self, seller_id, product_id, quantidade):
        # RN: Buscar seller e verificar se está ativo
        seller = self.user_repository.get_by_id(seller_id)
        if not seller or not seller.status:
            return {"erro": "Seller inativo ou não encontrado."}, 403

        # RN: Buscar produto
        produto = self.product_repository.get_by_id(product_id)
        if not produto or produto.seller_id != seller_id:
            return {"erro": "Produto não encontrado ou não pertence ao seller."}, 404

        # RN: Verificar se produto está ativo
        if not produto.status:
            return {"erro": "Produto está inativo."}, 400

        # RN: Verificar estoque
        if produto.quantidade_estoque < quantidade:
            return {"erro": "Estoque insuficiente."}, 400

        # Persistir venda e atualizar estoque
        return self.product_repository.register_sale(produto, quantidade)