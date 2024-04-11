from fastapi import HTTPException, status

EmailAlreadyExistsException = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
UnauthorizedException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
UserNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
InactiveUserException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
InvalidTokenException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
NoSuperUserException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No super user")