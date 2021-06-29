import os , sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from app import (
    app,
    EventView,
    JSONView,
    XMLView
)

import pytest

@pytest.fixture(scope="module")
def setup():
    EventView.register(app)
    JSONView.register(app)
    XMLView.register(app)

    app.run()