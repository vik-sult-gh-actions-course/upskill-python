"""User model definition for SQLAlchemy ORM.

This module contains the User model class which represents application users
in the database, including their authentication and authorization attributes.
"""

from sqlalchemy import Column, Integer, String, Boolean
from db import Base # pylint: disable=import-error


class Users(Base):
    """SQLAlchemy model representing application users.

    This class maps to the 'users' table in the 'public' schema and defines
    the structure for storing user account information including authentication
    details and role-based permissions.

    Attributes:
        id (int): Primary key identifier for the user
        email (str): Unique email address for the user
        username (str): Unique username for authentication
        first_name (str): User's first name
        last_name (str): User's last name
        hashed_password (str): Securely hashed password
        is_active (bool): Flag indicating if account is active (default: True)
        role (str): User's role/permission level (e.g., 'admin', 'user')

    Example:
        >>> new_user = Users(
        ...     email="user@example.com",
        ...     username="example_user",
        ...     first_name="John",
        ...     last_name="Doe",
        ...     hashed_password="hashed_value",
        ...     role="user"
        ... )
    """

    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

    def __repr__(self) -> str:
        """Provides a developer-friendly string representation of the user."""
        return (
            f"<User(id={self.id}, username='{self.username}', "
            f"email='{self.email}', role='{self.role}')>"
        )

    def get_full_name(self) -> str:
        """Returns the user's full name by combining first and last names.

        Returns:
            str: Concatenated first and last name with space separation
        """
        return f"{self.first_name} {self.last_name}".strip() # pylint: disable=missing-final-newline