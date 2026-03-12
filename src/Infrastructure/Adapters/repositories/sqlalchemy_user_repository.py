from src.Application.Ports.user_repository_port import UserRepositoryPort
from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db


class SqlAlchemyUserRepository(UserRepositoryPort):
    def save(self, user_domain):
        user = User(
            nome=user_domain.nome,
            cnpj=user_domain.cnpj,
            email=user_domain.email,
            celular=user_domain.celular,
            senha=user_domain.senha,
            codigoTwilio=user_domain.codigoTwilio,
        )
        db.session.add(user)
        db.session.commit()
        return self._to_domain(user)

    def list_all(self):
        return [self._to_domain(user) for user in User.query.all()]

    @staticmethod
    def _to_domain(user):
        return UserDomain(
            id=user.id,
            nome=user.nome,
            email=user.email,
            senha=user.senha,
            cnpj=user.cnpj,
            celular=user.celular,
            codigoTwilio=user.codigoTwilio,
        )
