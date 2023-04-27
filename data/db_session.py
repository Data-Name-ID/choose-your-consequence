"""Набор функций для создания базы данных и подключения к ней"""
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    """Инизиализация сессии подключения к базе данных

    Аргументы:
        db_file (str): Имя файла базы данных

    Исключения:
        Exception: Возникает в случае недопустимого названия базы данных
    """
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f"sqlite:///{db_file.strip()}?check_same_thread=False"
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(
        conn_str, echo=False, pool_size=20, max_overflow=0
    )
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    """Создание сессии подключения к базе данных

    Return:
        Session: возвращает объект подключения
    """
    global __factory
    return __factory()
