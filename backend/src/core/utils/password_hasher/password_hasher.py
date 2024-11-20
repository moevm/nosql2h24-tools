from abc import ABC, abstractmethod

class PasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass