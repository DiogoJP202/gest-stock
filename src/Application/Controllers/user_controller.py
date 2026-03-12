from flask import request, jsonify, make_response
from src.Application.UseCases.user_use_case import UserUseCase
from src.Infrastructure.Adapters.messaging.twilio_message_service import TwilioMessageService
from src.Infrastructure.Adapters.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)


_user_use_case = UserUseCase(
    user_repository=SqlAlchemyUserRepository(),
    message_service=TwilioMessageService(),
)

class UserController:
    @staticmethod
    def register_user():
        data = request.get_json() or {}

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

        try:
            user, twilio_result = _user_use_case.register_user(
                nome=nome,
                cnpj=cnpj,
                email=email,
                celular=celular,
                senha=senha,
            )
        except Exception as exc:
            return make_response(
                jsonify(
                    {
                        "erro": "Falha no cadastro ou no envio do WhatsApp.",
                        "detalhe": str(exc),
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
            result = _user_use_case.send_test_activation("5511958942521")
            return make_response(jsonify(result), 200)
        except Exception as exc:
            return make_response(jsonify({"erro": str(exc)}), 500)
        
    @staticmethod
    def verUsuarios():
        return make_response(jsonify({"usuarios": _user_use_case.list_users()}), 200)


