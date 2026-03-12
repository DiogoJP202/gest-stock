import secrets

from src.Domain.user import UserDomain


class UserUseCase:
    def __init__(self, user_repository, message_service):
        self.user_repository = user_repository
        self.message_service = message_service

    @staticmethod
    def _gerar_codigo(tamanho=4):
        maximo = 10**tamanho
        return f"{secrets.randbelow(maximo):0{tamanho}}"

    def register_user(self, nome, cnpj, email, celular, senha):
        codigo = self._gerar_codigo()
        user = UserDomain(
            id=None,
            nome=nome,
            email=email,
            senha=senha,
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
