from db import SessionLocal
from models import *
from passlib.context import CryptContext

session = SessionLocal()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# 1. Inserting a new user into the database
new_user = Users(
    email='lingaro.test@test.com',
    username='lingaro.test',
    first_name='lingaro.test',
    last_name='lingaro.test',
    hashed_password=bcrypt_context.hash('lingaroPass123!'),
    is_active=True,
    role='manager',
)
session.add(new_user)
session.commit()

# 2. Batch insert (@see https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#bulk-operations)
users_to_insert = [
    Users(
        email='lingaro.test+1@test.com',
        username='lingaro.test_1',
        first_name='lingaro.test_2',
        last_name='lingaro.test_2',
        hashed_password=bcrypt_context.hash('lingaroPass123!'),
        is_active=True,
        role='manager',
    ),
    Users(
        email='lingaro.test+2@test.com',
        username='lingaro.test_2',
        first_name='lingaro.test_2',
        last_name='lingaro.test_2',
        hashed_password=bcrypt_context.hash('lingaroPass123!'),
        is_active=True,
        role='manager',
    ),
    Users(
        email='lingaro.test+3@test.com',
        username='lingaro.test_3',
        first_name='lingaro.test_3',
        last_name='lingaro.test_3',
        hashed_password=bcrypt_context.hash('lingaroPass123!'),
        is_active=True,
        role='manager',
    )
]
session.bulk_save_objects(users_to_insert)
session.commit()

# Querying all users from the database
all_users = session.query(Users).all()
print('Users in table:', len(all_users))
for user in all_users:
    number = all_users.index(user) + 1
    print(f"{number}. ID {user.email}, e-mail {user.id}, role: {user.role}")

# Close the session
session.close()
