from datetime import datetime

from sqlalchemy import (MetaData, Table, Column, ForeignKey,
                        String, Integer, TIMESTAMP, JSON, Boolean)

metadata = MetaData()

role = Table(
    'role',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('permissions', JSON),
)


api_user = Table(
    'api_user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('username', String, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('registered_at', TIMESTAMP, default=datetime.utcnow),
    Column('role_id', Integer, ForeignKey(role.c.id, ondelete='CASCADE')),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=True, nullable=False),
    Column('is_verified', Boolean, default=True, nullable=False),
)