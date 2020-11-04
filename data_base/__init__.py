#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from contextlib import contextmanager

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
from sqlalchemy.orm import relationship, mapper, sessionmaker

from github import Repository
from note import Note

import sqlite3
creator = lambda: sqlite3.connect('file::memory:?cache=shared', uri=True)

STRING_LENGTH = 50
engine = create_engine('sqlite://',creator = creator, echo=True)
metadata = MetaData()


repository_table = Table('repository', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('owner', String(STRING_LENGTH)),
                         Column('repo_name', String(STRING_LENGTH))
                         )
repository_property = {}

note_table = Table('note', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('user_id', Integer),
                    Column('text', String(STRING_LENGTH)),
                    Column('repo_id',
                            Integer,
                            ForeignKey('repository.id'),
                            nullable=True),
                    Column('data', String(STRING_LENGTH)),
                    )


mapper(Repository, repository_table)
mapper(Note, note_table)

metadata.bind = engine
metadata.create_all(engine)

Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
