from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapper
from sqlalchemy import Integer, BigInteger


class EventHandler:

    @staticmethod
    @listens_for(Mapper, "before_insert")
    def receive_before_insert(mapper, connection, target):
        table = target.__table__
        EventHandler._validate(target.__dict__, table.columns)

    @staticmethod
    @listens_for(Mapper, "before_update")
    def receive_before_update(mapper, connection, target):
        table = target.__table__
        EventHandler._validate(target.__dict__, table.columns)

    @staticmethod
    def _validate(data, columns):
        for column in columns:
            print(column)
            if column.name not in data:
                continue
            value = data[column.name]
            if isinstance(column.type, String):
                length = column.type.length
                if value is None:
                    if not column.nullable:
                        raise ValueError(f"{column.name} cannot be null.")
                    continue
                if len(value) > length:
                    raise ValueError(f"{column.name} is to long. {len(value)} > {length}")


class Base(DeclarativeBase):
    pass


class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[int] = mapped_column(BigInteger())
    endpoint: Mapped[str] = mapped_column(String(200))
    method: Mapped[str] = mapped_column(String(10))
    jwt_id: Mapped[str] = mapped_column(String(200), nullable=True)
    message: Mapped[str] = mapped_column(String(3000))

    def __repr__(self) -> str:
        return f"Log(id={self.id!r})"


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str] = mapped_column(String(200))
    plz: Mapped[int] = mapped_column(Integer())
    city: Mapped[str] = mapped_column(String(200))
    state: Mapped[str] = mapped_column(String(200))
    country: Mapped[str] = mapped_column(String(200))

    def __repr__(self) -> str:
        return f"Address(id={self.id!r})"


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(200))
    lastname: Mapped[str] = mapped_column(String(200))
    gender: Mapped[int] = mapped_column(Integer())
    phone: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200))

    def __repr__(self) -> str:
        return f"Person(id={self.id!r})"


class Stromzaehler(Base):
    __tablename__ = "stromzaehler"
    id: Mapped[int] = mapped_column(primary_key=True)
    secret_key: Mapped[str] = mapped_column(String(200))
    address: Mapped[int] = mapped_column(Integer(), ForeignKey("addresses.id"))
    landlord: Mapped[int] = mapped_column(Integer(), ForeignKey("persons.id"))
    owner: Mapped[int] = mapped_column(Integer(), ForeignKey("persons.id"))

    def __repr__(self) -> str:
        return f"Stromzaehler(id={self.id!r})"


class StromzaehlerLog(Base):
    __tablename__ = "stromzaehler_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    stromzaehler: Mapped[int] = mapped_column(Integer(), ForeignKey("stromzaehler.id"))
    source_id: Mapped[int] = mapped_column(Integer())
    timestamp: Mapped[int] = mapped_column(BigInteger())
    message: Mapped[str] = mapped_column(String(3000))

    def __repr__(self) -> str:
        return f"StromzaehlerLog(id={self.id!r})"


class StromzaehlerReading(Base):
    __tablename__ = "stromzaehler_readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    stromzaehler: Mapped[int] = mapped_column(Integer(), ForeignKey("stromzaehler.id"))
    source_id: Mapped[int] = mapped_column(Integer())
    timestamp: Mapped[int] = mapped_column(BigInteger())
    value: Mapped[str] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"StromzaehlerReading(id={self.id!r})"


class Setting(Base):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(200), primary_key=True)
    value: Mapped[str] = mapped_column(String(200))

    def __repr__(self) -> str:
        return f"Setting(id={self.key!r})"
