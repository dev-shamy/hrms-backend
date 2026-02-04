from fastapi import Depends, HTTPException, status, Header
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.core.config import SECRET_KEY, ALGORITHM
from src.db.database import get_db
from src.common import admin as crud_admin
from schema.admin_schema.schema import TokenData, User


def get_current_user(
    db: Session = Depends(get_db),
    authorization: str = Header(..., description="Bearer <token>"),
) -> User:
    """
    Extract token manually from Authorization header.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not authorization.startswith("Bearer "):
        raise credentials_exception

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        role: str | None = payload.get("role")

        if not username:
            raise credentials_exception

        token_data = TokenData(username=username, role=role)

    except JWTError:
        raise credentials_exception

    user = crud_admin.get_user_by_username(db, token_data.username)
    if not user:
        raise credentials_exception

    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required"
        )
    return current_user
