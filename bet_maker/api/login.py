from datetime import timedelta
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from bet_maker.db.session import get_session
from bet_maker.core.hashing import Hasher
from bet_maker.schemas.users import Token
from bet_maker.db.utils.users import get_user, get_user_from_email
from bet_maker.core.security import create_access_token
from bet_maker.core.config import settings

api_router = APIRouter()
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/api/bet-maker/accounts/token')


async def authenticate_user(username: str, password: str, db: AsyncSession):
    user = await get_user(username=username, db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


@api_router.post('/token', response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Incorrect username or password'
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


async def get_current_user_form_token(token: str = Depends(oauth2_schema), db: AsyncSession = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'Could not validate credentials'
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        print(f'username/email extracted is {username}')

        if username is None:
            print('Here???')
            raise credentials_exception
    except JWTError:
        print("Or here???")
        raise credentials_exception

    user = await get_user_from_email(email=username, db=db)
    if user is None:
        raise credentials_exception
    return user
