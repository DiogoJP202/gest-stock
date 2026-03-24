import secrets
from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

from src.Domain.user import UserDomain

ALGORITHM = "HS256"


class UserUseCase:
    def __init__(self, user_repository, message_service):
        self.user_repository = user_repository
        self.message_service = message_service

    @staticmethod
    def _gerar_codigo(tamanho=4):
        maximo = 10**tamanho
        return f"{secrets.randbelow(maximo):0{tamanho}}"

    @staticmethod
    def _get_secret_key():
        return current_app.config["JWT_SECRET_KEY"]

    @staticmethod
    def criar_token(user_id: int):
        payload = {
            "sub": str(user_id),
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        }
        return jwt.encode(payload, UserUseCase._get_secret_key(), algorithm=ALGORITHM)

    @staticmethod
    def validar_token(token: str):
        try:
            return jwt.decode(token, UserUseCase._get_secret_key(), algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return {"erro": "Token expirado"}
        except jwt.InvalidTokenError:
            return {"erro": "Token invalido"}

    def register_user(self, nome, cnpj, email, celular, senha):
        codigo = self._gerar_codigo()

        user = UserDomain(
            id=None,
            nome=nome,
            email=email,
            senha=generate_password_hash(senha),
            cnpj=cnpj,
            celular=celular,
            codigoTwilio=codigo,
        )

        saved_user = self.user_repository.save(user)
        message_result = self.message_service.send_activation(celular, codigo)
        return saved_user, message_result

    def list_users(self):
        return [user.to_dict() for user in self.user_repository.list_all()]

    def send_test_activation(self, celular):
        codigo = self._gerar_codigo()
        return self.message_service.send_activation(celular, codigo)

    def validar_usuario(self, email, senha):
        usuario = self.user_repository.busca_por_email(email)

        if not usuario:
            return False

        senha_armazenada = usuario.senha or ""
        if senha_armazenada.startswith(("pbkdf2:", "scrypt:")):
            return usuario if check_password_hash(senha_armazenada, senha) else False

        return usuario if senha_armazenada == senha else False

    def ativa_usuario_via_email(self, email, codigoAtivacao):
        return self.user_repository.ativaUsuario(email, codigoAtivacao)
