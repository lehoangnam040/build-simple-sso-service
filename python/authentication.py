from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel


from .jwt import jwt_handler
from .repository import verify_account, retrive_permissions_of_account

class LoginV1RequestBody(BaseModel):

    username: str
    password: str


class LoginV1ResponseBody(BaseModel):

    uid: str
    jwt_token: str


router = APIRouter()

@router.post("/v1/login")
async def login_v1(login_req_body: LoginV1RequestBody, request: Request) -> LoginV1ResponseBody:
    """Handle login by username/password and return JWT token."""
    try:
        account = verify_account(login_req_body.username, login_req_body.password)
    except Exception as err:
        raise HTTPException(status_code=404, detail=str(err))
    

    permissions = retrive_permissions_of_account(account.uid)

    try:
        jwt_token = jwt_handler.encode_jwt(
            issuer=str(request.base_url),
            payload={
                "sub": account.uid,
                "email": account.email,
                "name": account.name,
                "scopes": permissions,
            },
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

    return LoginV1ResponseBody(
        uid=account.uid, 
        jwt_token=jwt_token
    )