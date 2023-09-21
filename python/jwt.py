import jwt

from datetime import datetime, timezone, timedelta


class PyjwtJwtHandler:
    """JWT handler using lib `pyjwt`."""

    def __init__(
        self, secret: str, public: str, algorithm: str = "EdDSA"
    ) -> None:
        """Init JWT handler using lib `pyjwt`."""
        self.secret_key = secret
        self.public_key = public
        self.algorithm = algorithm

    def encode_jwt(self, issuer: str, payload: dict) -> str:
        """Encode payload to get jwt token using `jwt.encode`."""
        payload["iss"] = issuer
        payload["iat"] = datetime.utcnow()
        payload["exp"] = datetime.utcnow() + timedelta(minutes=1)

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_jwt(self, jwt_token: str) -> dict:
        """Decode jwt token to get payload using `jwt.decode`."""
        return jwt.decode(jwt_token, self.public_key, leeway=timedelta(seconds=30), algorithms=[self.algorithm])


jwt_handler = PyjwtJwtHandler(
    secret="""-----BEGIN PRIVATE KEY-----
MC4CAQAwBQYDK2VwBCIEINd7x1GTtAIiw3dsKqCiIhBbQMYEUOglRXlqvcfwvgBJ
-----END PRIVATE KEY-----""",
    public="""-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEACzvgzRr6s6wGdHU/YRDCLT3jigx+KQcwDEEC0mF4yXA=
-----END PUBLIC KEY-----"""
)