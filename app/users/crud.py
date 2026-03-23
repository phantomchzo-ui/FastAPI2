import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.database import async_session
from app.products.models import Post
from app.users.models import User, Profile


async def create_user(session: AsyncSession, name: str) -> User:
    user = User(name=name, email=f"{name}@test.com", password="123456")
    session.add(user)
    await session.commit()
    return user


async def get_user_by_name(session: AsyncSession, name: str) -> User | None:
    stmt = select(User).where(User.name == name)
    user: User | None = await session.scalar(stmt)
    print("found user", name, user)
    return user


async def create_user_profile(
    session: AsyncSession, first_name: str, last_name: str, user_id: int
) -> Profile | None:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name if user.profile else "No profile")


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(
    session: AsyncSession,
):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = (
        select(User)
        .options(
            # joinedload(User.posts),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    # users = await session.scalars(stmt)
    # result: Result = await session.execute(stmt)
    # # users = result.unique().scalars()
    # users = result.scalars()
    users = await session.scalars(stmt)

    # for user in users.unique():  # type: User
    for user in users:  # type: User
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_users_with_posts_and_profiles(
    session: AsyncSession,
):
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)

    for user in users:  # type: User
        print("**" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:  # type: Post
        print("post", post)
        print("author", post.user)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        .where(User.name == "john")
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def main():
    async with async_session() as session:
        # await create_user(session=session, name="john")
        # await create_user(session=session, name="alice")
        # await create_user(session=session, name="sam")

        user_sam = await get_user_by_name(session=session, name="sam")
        user_john = await get_user_by_name(session=session, name="john")
        # await get_user_by_name(session=session, name="alice")

        # await create_user_profile(
        #    session=session,
        #    user_id=user_john.id,
        #    first_name="John",
        #    last_name="Marmont",
        # )

        # await create_user_profile(
        #    session=session,
        #    user_id=user_sam.id,
        #    first_name="Sam",
        #    last_name="White",
        # )

        await show_users_with_profiles(session=session)
        await create_posts(
            session,
            user_john.id,
            "SQLA 2.0",
            "SQLA Joins",
        )
        await create_posts(
            session,
            user_sam.id,
            "FastAPI intro",
            "FastAPI Advanced",
            "FastAPI more",
        )
        await get_users_with_posts(session=session)
        await get_posts_with_authors(session=session)
        await get_users_with_posts_and_profiles(session=session)
        await get_profiles_with_users_and_users_with_posts(session=session)


if __name__ == "__main__":
    asyncio.run(main())
