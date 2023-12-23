import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def make_migration():
    os.system("alembic upgrade head")
    return True
