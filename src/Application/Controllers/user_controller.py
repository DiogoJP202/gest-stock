
from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user():
        data = request.get_json()

        nome = data.get("nome")
        cnpj = data.get("cnpj")
        email = data.get("email")
        celular = data.get("celular")
        senha = data.get("senha")

        if not nome or not email or not senha or not celular or not cnpj:
            return make_response(jsonify({"erro": "Um campo nao foi preenchido."}), 400)

        if len(cnpj) < 14:
            return make_response(jsonify("CNPJ invalido. Sao necessarios pelo menos 14 digitos."), 401)

        if len(celular) < 11:
            return make_response(jsonify("Numero de celular invalido. Use um numero valido e funcional."), 401)

        user = UserService.create_user(nome, cnpj, email, celular, senha)

        try:
            twilio_result = UserService.ativacao_twilio(celular)
        except Exception as exc:
            return make_response(
                jsonify(
                    {
                        "erro": "Usuario criado, mas falha ao enviar WhatsApp.",
                        "detalhe": str(exc),
                        "usuario": user.to_dict(),
                    }
                ),
                502,
            )

        return make_response(
            jsonify(
                {
                    "mensagem": "Usuario salvo com sucesso. Verifique o WhatsApp.",
                    "usuarios cadastrados": user.to_dict(),
                    "whatsapp": twilio_result,
                }
            ),
            200,
        )

    @staticmethod
    def testarNumero():
        try:
            result = UserService.ativacao_twilio("5511958942521")
            return make_response(jsonify(result), 200)
        except Exception as exc:
            return make_response(jsonify({"erro": str(exc)}), 500)


