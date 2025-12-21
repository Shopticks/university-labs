from typing import Optional
from src.pharma_distributor.auth.models import User
from src.pharma_distributor.exceptions import AuthenticationError, UserPermissionError
from src.pharma_distributor.common.enums import Role
from src.pharma_distributor.interfaces.base import IRepository


class SecurityService:
    def __init__(self, user_repository: IRepository[User]):
        self.user_repo = user_repository

    def login(self, username: str, password: str) -> User:
        users = self.user_repo.list_all()
        user = next((u for u in users if u.credentials.username == username), None)

        if not user:
            raise AuthenticationError("User not found")

        if not user.credentials.verify_password(password):
            raise AuthenticationError("Invalid password")

        if not user.is_active:
            raise AuthenticationError("User is inactive")

        return user

    def change_user_role(self, admin: User, target_user: User, new_role: Role) -> None:
        if not admin.has_permission(Role.ADMIN):
            raise PermissionError("Only admins can change roles")

        target_user.role = new_role
        self.user_repo.save(target_user)