import typing

from .models import Account, Role, Permission


# dict map from email to uid
_email_2_account = {
    "root@company.com": Account(
        uid="1",
        email="root@company.com",
        name="Root account"
    ),
    "tracy@company.com": Account(
        uid="2",
        email="tracy@company.com",
        name="Tracy"
    ),
    "namlh@gmail.com": Account(
        uid="10",
        email="namlh@gmail.com",
        name="Nam Le Hoang",
    )
}

# dict map from account to list of roles
_role_binding = {
    "1": ["admin"],
    "2": ["moderator", "guest"],
    "10": ["guest"],
}

# dict map from role to list of permissions
_permission_binding = {
    "admin": ["accounts:all"],
    "moderator": ["airports:list", "flights:list", "flights:create", "flights:modify", ],
    "guest": ["airports:list", "flights:list", "flights:book"],
}

def verify_account(email: str, password: str) -> Account:
    if email not in _email_2_account:
        raise Exception("not found")

    hashed_password = email[::-1]

    if hashed_password != password:
        raise Exception("password verification failed")
    
    return _email_2_account[email]

def retrive_permissions_of_account(uid: str) -> typing.List[str]:
    roles = _role_binding[uid]

    perms = []
    for role in roles:
        for perm in _permission_binding[role]:
            perms.append(perm)
    return perms
