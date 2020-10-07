import io

import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    stpipe import log

    # Turn off default logging when running tests
    buffer = io.BytesIO(b"[*]\n")

    log.load_configuration(buffer)
