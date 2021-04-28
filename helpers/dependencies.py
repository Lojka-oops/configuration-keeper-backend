import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from dependency_injector.wiring import inject, Provide

from containers import Container

basic_auth_scheme = HTTPBasic()


@inject
def basic_auth(
    basic_auth_username: str = Depends(Provide[Container.config.basic_auth.username]),
    basic_auth_password: str = Depends(Provide[Container.config.basic_auth.password]),
    credentials: HTTPBasicCredentials = Depends(basic_auth_scheme)
) -> None:
    """Checks basic auth credentials
    
    """

    correct_username = secrets.compare_digest(credentials.username, basic_auth_username)
    correct_password = secrets.compare_digest(credentials.password, basic_auth_password)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"}
        )
