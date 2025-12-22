import pytest
from pharma_distributor.auth.models import User, Credentials
from pharma_distributor.common.models import ContactInfo
from pharma_distributor.common.enums import Role
from pharma_distributor.utils.generators import PasswordHelper
from pharma_distributor.exceptions import ValidationError, AuthenticationError


@pytest.fixture
def valid_contact():
    return ContactInfo(email="test@example.com", phone="+1234567890")


@pytest.fixture
def valid_credentials():
    salt = PasswordHelper.generate_salt()
    pwd_hash = PasswordHelper.hash_password("secret123", salt)
    return Credentials(username="user1", password_hash=pwd_hash, salt=salt)


@pytest.fixture
def user_admin(valid_contact, valid_credentials):
    return User(
        id=1,
        full_name="Admin User",
        role=Role.ADMIN,
        contact=valid_contact,
        credentials=valid_credentials,
        is_active=True
    )


@pytest.fixture
def user_manager(valid_contact, valid_credentials):
    return User(
        id=2,
        full_name="Manager User",
        role=Role.MANAGER,
        contact=valid_contact,
        credentials=valid_credentials,
        is_active=True
    )



def test_credentials_verify_password(valid_credentials):
    assert valid_credentials.verify_password("secret123") is True
    assert valid_credentials.verify_password("wrongpass") is False


def test_credentials_update_password(valid_credentials):
    old_hash = valid_credentials.password_hash
    old_salt = valid_credentials.salt
    old_time = valid_credentials.last_password_change

    valid_credentials.update_password("new_secret_password")

    assert valid_credentials.verify_password("new_secret_password") is True
    assert valid_credentials.password_hash != old_hash
    assert valid_credentials.salt != old_salt
    assert valid_credentials.last_password_change > old_time


def test_credentials_update_password_too_short(valid_credentials):
    with pytest.raises(ValidationError, match="Password is too short"):
        valid_credentials.update_password("short")



def test_user_activation_deactivation(user_manager):
    assert user_manager.is_active is True

    user_manager.deactivate()
    assert user_manager.is_active is False

    user_manager.activate()
    assert user_manager.is_active is True


def test_user_update_contact_info(user_manager):
    original_phone = user_manager.contact.phone

    user_manager.update_contact_info(new_email="new@example.com")

    assert user_manager.contact.email == "new@example.com"
    assert user_manager.contact.phone == original_phone

    user_manager.update_contact_info(new_phone="+9876543210", new_website="https://example.com")
    assert user_manager.contact.phone == "+9876543210"
    assert user_manager.contact.website == "https://example.com"


def test_user_permissions_admin(user_admin):
    assert user_admin.has_permission(Role.ADMIN) is True
    assert user_admin.has_permission(Role.MANAGER) is True
    assert user_admin.has_permission(Role.WAREHOUSE_WORKER) is True


def test_user_permissions_specific_role(user_manager):
    assert user_manager.has_permission(Role.MANAGER) is True
    assert user_manager.has_permission(Role.ADMIN) is False
    assert user_manager.has_permission(Role.WAREHOUSE_WORKER) is False


def test_user_permissions_inactive(user_admin):
    user_admin.deactivate()
    assert user_admin.has_permission(Role.ADMIN) is False


def test_user_change_password_success(user_manager):
    user_manager.change_password("secret123", "new_long_password")
    assert user_manager.credentials.verify_password("new_long_password") is True


def test_user_change_password_wrong_old(user_manager):
    with pytest.raises(AuthenticationError, match="Old password is correct"):
        user_manager.change_password("wrong_old", "new_long_password")


def test_user_change_password_invalid_new(user_manager):
    with pytest.raises(ValidationError):
        user_manager.change_password("secret123", "short")