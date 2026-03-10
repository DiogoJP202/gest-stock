import os
from twilio.rest import Client
import json
import secrets

from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 

def _build_twilio_client():
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    if not account_sid or not auth_token:
        return None

    return Client(account_sid, auth_token)


def _gerar_codigo(tamanho=4):
    maximo = 10**tamanho
    return f"{secrets.randbelow(maximo):0{tamanho}}"

class UserService:
    @staticmethod
    def create_user(nome, cnpj, email, celular, senha):        
        user = User(nome=nome, cnpj=cnpj, email=email, celular=celular, senha=senha, codigoTwilio = _gerar_codigo())       

        db.session.add(user)
        db.session.commit()       

        return UserDomain(user.id, user.nome, user.cnpj, user.email, user.celular, user.senha, user.codigoTwilio)
    
    @staticmethod
    def ativacao_twilio(celular, codigo):
        auth_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        
        client = _build_twilio_client()
        if client is None:
            raise RuntimeError("Twilio credentials are missing. Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN.")

        message = client.messages.create(
            from_ = f"whatsapp:+14155238886",
            to = f"whatsapp:+{celular}",
            content_sid='HX229f5a04fd0510ce1b071852155d3e75',
            content_variables=f'{{"1":"{codigo}"}}',        
        )

        return {
            "sid": message.sid,
            "status": message.status,
            "to": message.to,
        }
        
    @staticmethod
    def get_all_users():
        users = User.query.all()
        return [UserDomain(user.id, user.nome, user.cnpj, user.email, user.celular, user.senha, user.codigoTwilio).to_dict() for user in users]