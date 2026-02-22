"""DB-dependent test fixtures — require custom_keywords (simulated DB lookups)."""
import pytest
from tests.fixtures.basic_episodes import basic_episodes_db
from tests.conftest import run_fixture


@pytest.mark.parametrize("fixture", basic_episodes_db, ids=lambda f: f.file_name[:60])
def test_basic_episodes_db(fixture):
    run_fixture(fixture)
