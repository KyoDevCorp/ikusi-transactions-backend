from abc import ABC, abstractmethod

class UserServiceClient(ABC):
    @abstractmethod
    def get_user_by_token(self, token: str) -> dict:
        pass