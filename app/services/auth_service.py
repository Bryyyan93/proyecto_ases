from app.security.password import verify_password
from app.repositories.user_repo import UserRepository


class AuthService:

    @staticmethod
    def authenticate(db, username: str, password: str):
        repo = UserRepository(db)
        user = repo.get_by_username(username)

        if not user:
            return None

        if not verify_password(password, user["password_hash"]):
            return None

        return {
            "id": user["id"],
            "username": user["username"],
            "roles": user["roles"],  # lista de roles
        }
