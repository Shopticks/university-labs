from pharma_distributor.auth.models import User
from pharma_distributor.common.enums import Role
from pharma_distributor.exceptions import AuthenticationError
from pharma_distributor.interfaces.base import IRepository


class SecurityService:
    """
    Domain service responsible for high-level authentication and authorization logic,
    managing user sessions and role assignments.
    """
    def __init__(self, user_repository: IRepository[User]):
        """
        Args:
           user_repository: Repository interface for accessing User data.
        """
        self.user_repo = user_repository

    def login(self, username: str, password: str) -> User:
        """
        Authenticates a user against the repository.

        Args:
           username: The username to look up.
           password: The plain text password to verify.

        Returns:
           User: The authenticated User object.

        Raises:
           AuthenticationError: If the user is not found, the password is invalid,
                                or the user account is inactive.
        """
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
        """
        Updates the role of a specific user. This action is restricted to Administrators.

        Args:
            admin: The user performing the action (must have ADMIN role).
            target_user: The user whose role is being modified.
            new_role: The new Role to assign.

        Raises:
            PermissionError: If the 'admin' user does not have Administrator privileges.
        """
        if not admin.has_permission(Role.ADMIN):
            raise PermissionError("Only admins can change roles")

        target_user.role = new_role
        self.user_repo.save(target_user)