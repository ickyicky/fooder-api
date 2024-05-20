from .client import *  # noqa
from .user import *  # noqa
from .product import *  # noqa
from .meal import *  # noqa
from .entry import *  # noqa
import pytest


@pytest.fixture
def anyio_backend():
    return "asyncio"
