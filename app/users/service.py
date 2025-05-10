from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import UsersOrm
from app.users.schemas import UserCreateSchema, UserReadSchema
from app.users.security import hash_password


async def get_users(session: AsyncSession) -> list[UserReadSchema] | None:
    async with session.begin():
        query = select(UsersOrm)
        result = await session.execute(query)
        users = result.scalars().all()

        from loguru import logger

        logger.info(f"{users=}")

        if users:
            return [UserReadSchema.model_validate(user) for user in users]


async def get_user_by_id(
    session: AsyncSession, user_id: int
) -> UserReadSchema | None:
    async with session.begin():
        query = select(UsersOrm).where(UsersOrm.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user:
            return UserReadSchema.model_validate(user)


async def create_user(session: AsyncSession, user: UserCreateSchema) -> UserReadSchema | None:
    async with session.begin():
        existing_user = await session.scalar(
            select(UsersOrm).where(UsersOrm.username == user.username)
        )
        if existing_user:
            return None

        hashed_password = hash_password(user.password)

        new_user = UsersOrm(
            username=user.username,
            password=hashed_password
        )
        session.add(new_user)
        await session.flush()
        await session.refresh(new_user)

        return UserReadSchema.model_validate(new_user)
