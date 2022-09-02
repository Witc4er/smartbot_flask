from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table, MetaData
from sqlalchemy.sql.sqltypes import DateTime

from db.db_conn import Base, engine, db_session

# таблица для связи many2many

note_m2m_tag = Table(
    "note_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("note", Integer, ForeignKey("notes.id")),
    Column("tag", Integer, ForeignKey("tags.id")),
)


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.now())
    description = Column(String(150), nullable=False)
    done = Column(Boolean, default=False)
    tags = relationship("Tag", secondary="note_m2m_tag", backref="notes")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return self.name


adb_m2m_tel = Table(
    'adb_m2m_tel',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('adb_id', Integer, ForeignKey('addressbook.id')),
    Column('tel_id', Integer, ForeignKey('telephones.id'))
)

adb_m2m_email = Table(
    'adb_m2m_email',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('adb_id', Integer, ForeignKey('addressbook.id')),
    Column('email_id', Integer, ForeignKey('emails.id'))
)


class AddressBook(Base):
    __tablename__ = 'addressbook'
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    address = Column(String)
    email = relationship('Email', secondary='adb_m2m_email', backref='addressbook')
    phone = relationship("Telephone", secondary='adb_m2m_tel', backref='addressbook')
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())


class Telephone(Base):
    __tablename__ = "telephones"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    phone = Column(String(25), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f'<Telephone "{self.phone}">'


class Email(Base):
    __tablename__ = 'emails'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f'<Email "{self.email}">'


if __name__ == "__main__":
    Base.metadata.create_all(engine)