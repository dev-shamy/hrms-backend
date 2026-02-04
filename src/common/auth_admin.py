from fastapi import HTTPException, status
from src.core.config import ADMIN_USERNAME, ADMIN_PASSWORD


def verify_admin_credentials(username: str, password: str) -> dict:
    """
    Verify admin credentials from .env as demo account
    """
    try:
        # Check if admin credentials are configured
        if not ADMIN_USERNAME or not ADMIN_PASSWORD:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Admin credentials are not properly configured",
            )

        # Validate username
        if username != ADMIN_USERNAME:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if password != ADMIN_PASSWORD:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Return admin info if credentials are valid
        return {"username": ADMIN_USERNAME, "role": "admin"}

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication error: {str(e)}",
        )
