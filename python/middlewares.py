"""Middleware validate JWT Bearer token in headers."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes

from .models import Account
from .jwt import jwt_handler
from .repository import retrive_permissions_of_account

reusable_oauth2 = HTTPBearer(scheme_name="Authorization")


async def jwt_authentication_middleware(
    http_authorization_credentials: HTTPAuthorizationCredentials = Depends(
        reusable_oauth2
    ),
) -> dict:
    """Validate token and return account info."""
    try:
        payload = jwt_handler.decode_jwt(http_authorization_credentials.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token or expired token.",
        )
    else:
        return payload


async def scope_authorization_middleware(
    security_scopes: SecurityScopes, payload: dict = Depends(
        jwt_authentication_middleware
    ),
) -> Account:
    token_scopes = retrive_permissions_of_account(payload["sub"])
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'},
            )
    try:
        current_account = Account(
            uid=payload["sub"],
            email=payload["email"],
            name=payload["name"],
        )
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{err}")
    else:
        return current_account
