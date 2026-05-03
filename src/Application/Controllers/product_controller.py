from flask import request, jsonify, make_response
from .user_controller import token_required, _build_user_use_case

# Mock de factory (deve seguir seu padrão de injeção)
def _build_product_use_case():
    # Aqui você instanciaria com os repositórios reais
    pass

class ProductController:
    
    @staticmethod
    @token_required
    def cadastrar_produto():
        # O payload do token deve ser passado para identificar o seller_id
        # Assumindo que seu token_required injeta o user_id ou você o recupera do build_user_use_case
        data = request.get_json()
        auth_header = request.headers.get("Authorization").split(" ")[1]
        payload = _build_user_use_case().validar_token(auth_header)
        seller_id = payload['sub'] 

        # Lógica de cadastro...
        return make_response(jsonify({"msg": "Produto cadastrado"}), 201)

    @staticmethod
    @token_required
    def registrar_venda():
        data = request.get_json()
        # Validação de campos obrigatórios
        # Chamada ao UseCase
        return make_response(jsonify({"msg": "Venda realizada"}), 200)