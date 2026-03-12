from abc import ABC, abstractmethod


class UserRepositoryPort(ABC):
    @abstractmethod
    def save(self, user_domain):
        raise NotImplementedError

    @abstractmethod
    def list_all(self):
        raise NotImplementedError
