class ProductDomain:
    def __init__(self, id, nome, preco, quantidade_estoque, seller_id, imagem=None, status=True):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque
        self.status = status
        self.imagem = imagem
        self.seller_id = seller_id

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "quantidade_estoque": self.quantidade_estoque,
            "status": "Ativo" if self.status else "Inativo",
            "imagem": self.imagem
        }