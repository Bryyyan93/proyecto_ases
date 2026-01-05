import bcrypt


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        plain.encode(),
        hashed.encode()
    )
