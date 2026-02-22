"""Heuristic-only test fixtures — no DB/custom_keywords needed."""
import pytest
from tests.fixtures.basic_episodes import basic_episodes
from tests.fixtures.seasons import seasons
from tests.fixtures.ranges import ranges
from tests.fixtures.episode_titles import episode_titles
from tests.fixtures.years import years
from tests.fixtures.series_types import series_types
from tests.fixtures.content_types import content_types
from tests.fixtures.release_info import release_info
from tests.fixtures.video_audio import video_audio
from tests.fixtures.complex import complex_cases as complex_fixtures
from tests.fixtures.folder_context import folder_context
from tests.conftest import run_fixture


@pytest.mark.parametrize("fixture", basic_episodes, ids=lambda f: f.file_name[:60])
def test_basic_episodes(fixture):
    run_fixture(fixture)


@pytest.mark.parametrize("fixture", seasons, ids=lambda f: f.file_name[:60])
def test_seasons(fixture):
    run_fixture(fixture)


@pytest.mark.parametrize("fixture", ranges, ids=lambda f: f.file_name[:60])
def test_ranges(fixture):
    run_fixture(fixture)


@pytest.mark.parametrize("fixture", episode_titles, ids=lambda f: f.file_name[:60])
def test_episode_titles(fixture):
    run_fixture(fixture)


@pytest.mark.parametrize("fixture", years, ids=lambda f: f.file_name[:60])
def test_years(fixture):
    run_fixture(fixture)


@pytest.mark.parametrize("fixture", series_types, ids=lambda f: f.file_name[:60])
def test_series_types(fixture):
    run_fixture(fixture)


@pytest.mark.parametrize("fixture", content_types, ids=lambda f: f.file_name[:60])
def test_content_types(fixture):
    run_fixture(fixture)


@pytest.mark.parametrize("fixture", release_info, ids=lambda f: f.file_name[:60])
def test_release_info(fixture):
    run_fixture(fixture)


@pytest.mark.parametrize("fixture", video_audio, ids=lambda f: f.file_name[:60])
def test_video_audio(fixture):
    run_fixture(fixture)


@pytest.mark.parametrize("fixture", complex_fixtures, ids=lambda f: f.file_name[:60])
def test_complex(fixture):
    run_fixture(fixture)


@pytest.mark.parametrize("fixture", folder_context, ids=lambda f: f.path[:60])
def test_folder_context(fixture):
    run_fixture(fixture)
