from src.Application.Controllers.user_controller import UserController
from flask import jsonify, make_response

def init_routes(app):    
    @app.route('/', methods=['GET'])
    def index():
        return make_response(jsonify({
            "message": "Server is running",
        }), 200)

    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
    
    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()
    
    @app.route('/testarNumero', methods=['GET'])
    def testar_numero():
        return UserController.testarNumero()
