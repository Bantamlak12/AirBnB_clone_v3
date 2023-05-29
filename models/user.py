#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """Gets the hashed value of the user's password."""
        return self._password

    @password.setter
    def password(self, value):
        """Sets the user's password."""
        if value is not None:
            self._password = hashlib.md5(value.encode()).hexdigest()
        else:
            self._password = None

    @validates('password')
    def validate_password(self, key, password):
        """Validates the user's password."""
        assert password is not None, "Password cannot be None"
        return hashlib.md5(password.encode()).hexdigest()
