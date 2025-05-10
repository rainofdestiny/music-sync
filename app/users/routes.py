from fastapi import APIRouter, Path, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app.depends import PaginationDep, SessionDep
from app.users import service
from app.users.schemas import UserCreateSchema, UserLoginSchema, UserReadSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    response_model=list[UserReadSchema],
)
async def get_users(
    session: SessionDep, pagination: PaginationDep
) -> list[UserReadSchema]:
    users = await service.get_users(session)

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
        )
    return users


@router.get(
    "/{user_id}",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchema,
)
async def get_user_by_id(
    session: SessionDep, user_id: int = Path(..., ge=1)
) -> UserReadSchema:
    user = await service.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/register")
async def register(user: UserCreateSchema, session: SessionDep):
    new_user = await service.create_user(session, user)

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    return new_user


@router.post("/login")
async def login(user: UserLoginSchema, session: SessionDep):
    user = await service.create_user(session, user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return user
