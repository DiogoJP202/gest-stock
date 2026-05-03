from src.Application.Controllers.user_controller import UserController
# Certifique-se de criar este controller conforme os passos anteriores
from src.Application.Controllers.product_controller import ProductController 

from flask import jsonify, make_response

def init_routes(app):    
    # --- Rotas de Sistema ---
    @app.route('/', methods=['GET'])
    def index():
        return make_response(jsonify({"message": "Server is running"}), 200)

    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({"mensagem": "API - OK; Docker - Up"}), 200)
    
    # --- Rotas de Usuário (Sellers) ---
    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()
    
    @app.route('/testarNumero', methods=['GET'])
    def testar_numero():
        return UserController.testarNumero()

    @app.route('/users', methods=['GET'])
    def ver_usuarios():
        return UserController.verUsuarios()
    
    @app.route('/ativarUsuario', methods=["POST"])
    def ativar_usuario():
        return UserController.ativar_usuario()

    @app.route('/login', methods=['POST'])
    def login_user():
        return UserController.login_user()

    # --- Rotas de Gerenciamento de Produtos (Requisito 3.1) ---
    @app.route('/produtos', methods=['POST'])
    def cadastrar_produto():
        return ProductController.cadastrar_produto()

    @app.route('/produtos', methods=['GET'])
    def listar_produtos():
        return ProductController.listar_produtos()

    @app.route('/produtos/<int:product_id>', methods=['GET'])
    def visualizar_produto(product_id):
        return ProductController.visualizar_produto(product_id)

    @app.route('/produtos/<int:product_id>', methods=['PUT'])
    def editar_produto(product_id):
        return ProductController.editar_produto(product_id)

    @app.route('/produtos/<int:product_id>/inativar', methods=['PATCH'])
    def inativar_produto(product_id):
        return ProductController.inativar_produto(product_id)

    # --- Rotas de Venda (Requisito 3.2) ---
    @app.route('/vendas', methods=['POST'])
    def registrar_venda():
        return ProductController.registrar_venda()