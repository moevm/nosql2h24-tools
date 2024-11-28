from datetime import datetime, timezone, timedelta
import jwt
import pytest
from src.configs.jwt_config import JWTConfig
from src.core.exceptions.client_error import JWTTokenExpiredError, JWTTokenInvalidError
from src.core.services.authentication.jwt.jwt_token_manager import JWTTokenManager

@pytest.fixture
def jwt_config():
    return JWTConfig()

@pytest.fixture
def jwt_token_manager(jwt_config):
    return JWTTokenManager(jwt_config)

@pytest.mark.parametrize("payload", [
    {"sub": "client_id", "role": "client"},
    {"sub": "worker_id", "role": "worker"}
])
def test_create_and_decode_access_token(jwt_token_manager, payload):
    current_time = datetime.now(timezone.utc)
    token = jwt_token_manager.create_access_token(payload)

    assert isinstance(token, str)

    decoded = jwt_token_manager.decode_access_token(token)

    assert decoded["sub"] == payload["sub"]
    assert decoded["role"] == payload["role"]
    assert "exp" in decoded

    exp_time = datetime.fromtimestamp(decoded["exp"], timezone.utc)
    expected_exp_time = current_time + timedelta(minutes=jwt_token_manager.config.jwt_access_token_expire_minutes)

    assert abs((exp_time - expected_exp_time)).total_seconds() < 5

@pytest.mark.parametrize("payload", [
    {"sub": "client_id", "role": "client"},
    {"sub": "worker_id", "role": "worker"}
])
def test_create_and_decode_refresh_token(jwt_token_manager, payload):
    current_time = datetime.now(timezone.utc)
    token = jwt_token_manager.create_refresh_token(payload)

    assert isinstance(token, str)

    decoded = jwt_token_manager.decode_refresh_token(token)

    assert decoded["sub"] == payload["sub"]
    assert decoded["role"] == payload["role"]
    assert "exp" in decoded

    exp_time = datetime.fromtimestamp(decoded["exp"], timezone.utc)
    expected_exp_time = current_time + timedelta(days=jwt_token_manager.config.jwt_refresh_token_expire_days)

    assert abs((exp_time - expected_exp_time)).total_seconds() < 5

def test_decode_access_token_expired(jwt_token_manager):
    expired_token = jwt.encode(
        {"sub": "user_id", "role": "client", "exp": datetime.now(timezone.utc) - timedelta(seconds=1)},
        jwt_token_manager.config.jwt_access_secret_key,
        algorithm=jwt_token_manager.config.jwt_algorithm
    )

    with pytest.raises(JWTTokenExpiredError):
        jwt_token_manager.decode_access_token(expired_token)


def test_decode_refresh_token_expired(jwt_token_manager):
    expired_token = jwt.encode(
        {"sub": "user_id", "role": "client", "exp": datetime.now(timezone.utc) - timedelta(seconds=1)},
        jwt_token_manager.config.jwt_refresh_secret_key,
        algorithm=jwt_token_manager.config.jwt_algorithm
    )

    with pytest.raises(JWTTokenExpiredError):
        jwt_token_manager.decode_refresh_token(expired_token)

def test_decode_access_token_invalid(jwt_token_manager):
    invalid_token = "invalid.token.format"

    with pytest.raises(JWTTokenInvalidError):
        jwt_token_manager.decode_access_token(invalid_token)

def test_decode_refresh_token_invalid(jwt_token_manager):
    invalid_token = "invalid.token.format"

    with pytest.raises(JWTTokenInvalidError):
        jwt_token_manager.decode_refresh_token(invalid_token)


def test_refresh_access_token(jwt_token_manager):
    payload = {"sub": "user_id", "role": "client"}
    refresh_token = jwt_token_manager.create_refresh_token(payload)

    current_time = datetime.now(timezone.utc)

    new_access_token = jwt_token_manager.refresh_access_token(refresh_token)
    decoded = jwt_token_manager.decode_access_token(new_access_token)

    assert decoded["sub"] == payload["sub"]
    assert decoded["role"] == payload["role"]
    assert "exp" in decoded


    expected_exp_time = current_time + timedelta(minutes=jwt_token_manager.config.jwt_access_token_expire_minutes)
    exp_time = datetime.fromtimestamp(decoded["exp"], timezone.utc)

    assert abs((exp_time - expected_exp_time)).total_seconds() < 5

