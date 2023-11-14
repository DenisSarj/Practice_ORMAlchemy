from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import Select
from typing import Iterable
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import joinedload

import config
from models import Base, User, Address

engine = create_engine(url=config.SQLALCHEMY_URL,
                       echo=config.SQLALCHEMY_ECHO,
                       )


def create_user(session: Session, name: str, username: str):
    user = User(
        name=name,
        username=username,
    )
    session.add(user)
    session.commit()
    return user


def create_user_with_email(session: Session, name: str, username: str, emails: list[str]):
    addreses = [
        Address(email=email)
        for email in emails
    ]

    user = User(
        name=name,
        username=username,
        addresses=addreses
    )
    session.add(user)

    session.commit()
    return user


def fetch_user(session: Session, username: str) -> User:
    stmt = Select(User).where(User.username == username)
    user: User | None = session.scalar(stmt)
    return user

def add_addresses(session: Session, user: User, *emails: str) -> None:
    user.addresses = [
        Address(email=email)
        for email in emails
    ]
    session.commit()

def show_addresses(session: Session):
    stmt = Select(Address).options(joinedload(
        Address.user)
    )
    addresses: Iterable[Address] = session.scalars(stmt)
    for address in addresses:
        print(address.email)
        print(address.user)


def main():
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        # res = session.execute(text('SELECT 1;'))
        # print(res.all())
        # create_user(session=session,
        #             name='Bob White',
        #             username='Bob',
        #             )
        # create_user_with_email(session=session,
        #             name='Adolf White',
        #             username='Enstein',
        #             emails=[
        #                 'Adolf@mail.ru',
        #                 'Enstein@mail.com'
        #             ]
        #             )
        # user = fetch_user(session=session, username='Bob')
        # print(user)
        # add_addresses(session, user, 'bobWhite@mail.com')

        # stmt = Select(User).options(selectinload(User.addresses))
        # users: Iterable[User] = session.scalars(stmt)
        # for user in users:
        #     print(user)
        #     for address in user.addresses:
        #         print(address.email)
        show_addresses(session)

if __name__ == '__main__':
    main()
