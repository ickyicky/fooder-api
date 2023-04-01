from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--create-tables", action="store_true")
    group.add_argument("--create-user", action="store_true")
    parser.add_argument("--username", type=str, action="store")
    parser.add_argument("--password", type=str, action="store")
    args = parser.parse_args()

    import sqlalchemy
    from sqlalchemy.orm import Session
    from .domain import Base
    from .settings import Settings

    settings = Settings()
    engine = sqlalchemy.create_engine(settings.DB_URI.replace("+asyncpg", ""))

    if args.create_tables:
        Base.metadata.create_all(engine)

    if args.create_user:
        with Session(engine) as session:
            from .domain.user import User

            user = User(
                username=args.username,
            )
            user.set_password(args.password)
            session.add(user)
            session.commit()
