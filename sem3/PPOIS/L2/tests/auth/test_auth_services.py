import pytest
from unittest.mock import Mock
from pharma_distributor.auth.services import SecurityService
from pharma_distributor.auth.models import User, Credentials
from pharma_distributor.common.models import ContactInfo
from pharma_distributor.common.enums import Role
from pharma_distributor.utils.generators import PasswordHelper
from pharma_distributor.exceptions import AuthenticationError


@pytest.fixture
def mock_user_repo():
    repo = Mock()
    return repo


@pytest.fixture
def security_service(mock_user_repo):
    return SecurityService(user_repository=mock_user_repo)


@pytest.fixture
def existing_user():
    salt = PasswordHelper.generate_salt()
    pwd_hash = PasswordHelper.hash_password("correct_password", salt)
    creds = Credentials(username="jdoe", password_hash=pwd_hash, salt=salt)
    contact = ContactInfo(email="jdoe@example.com", phone="+1234567890")

    return User(
        id=1,
        full_name="John Doe",
        role=Role.MANAGER,
        contact=contact,
        credentials=creds,
        is_active=True
    )


@pytest.fixture
def admin_user():
    salt = PasswordHelper.generate_salt()
    pwd_hash = PasswordHelper.hash_password("adminpass", salt)
    creds = Credentials(username="admin", password_hash=pwd_hash, salt=salt)
    contact = ContactInfo(email="admin@example.com", phone="+1234567890")

    return User(
        id=99,
        full_name="Super Admin",
        role=Role.ADMIN,
        contact=contact,
        credentials=creds,
        is_active=True
    )



def test_login_success(security_service, mock_user_repo, existing_user):
    mock_user_repo.list_all.return_value = [existing_user]

    user = security_service.login("jdoe", "correct_password")

    assert user == existing_user
    assert user.id == 1


def test_login_user_not_found(security_service, mock_user_repo):
    mock_user_repo.list_all.return_value = []

    with pytest.raises(AuthenticationError, match="User not found"):
        security_service.login("unknown", "password")


def test_login_wrong_password(security_service, mock_user_repo, existing_user):
    mock_user_repo.list_all.return_value = [existing_user]

    with pytest.raises(AuthenticationError, match="Invalid password"):
        security_service.login("jdoe", "wrong_password")


def test_login_inactive_user(security_service, mock_user_repo, existing_user):
    existing_user.deactivate()
    mock_user_repo.list_all.return_value = [existing_user]

    with pytest.raises(AuthenticationError, match="User is inactive"):
        security_service.login("jdoe", "correct_password")


def test_change_user_role_success(security_service, mock_user_repo, admin_user, existing_user):
    assert existing_user.role == Role.MANAGER

    security_service.change_user_role(admin_user, existing_user, Role.WAREHOUSE_WORKER)

    assert existing_user.role == Role.WAREHOUSE_WORKER
    mock_user_repo.save.assert_called_once_with(existing_user)


def test_change_user_role_permission_denied(security_service, mock_user_repo, existing_user):
    target_user = User(
        id=3, full_name="Target", role=Role.USER,
        contact=existing_user.contact, credentials=existing_user.credentials
    )

    with pytest.raises(PermissionError, match="Only admins can change roles"):
        security_service.change_user_role(existing_user, target_user, Role.ADMIN)

    mock_user_repo.save.assert_not_called()