from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    """Base from DeclarativeBase"""

    pass


class CommonMixin:
    """define a series of common elements that may be applied to mapped
    classes using this class as a mixin class."""

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """__tablename__.

        :rtype: str
        """
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)
