from tests.fixtures.basic_episodes import basic_episodes, basic_episodes_db
from tests.fixtures.seasons import seasons
from tests.fixtures.ranges import ranges
from tests.fixtures.episode_titles import episode_titles
from tests.fixtures.years import years
from tests.fixtures.series_types import series_types
from tests.fixtures.content_types import content_types
from tests.fixtures.release_info import release_info
from tests.fixtures.video_audio import video_audio
from tests.fixtures.complex import complex_cases as complex_fixtures

heuristic = (
    basic_episodes
    + seasons
    + ranges
    + episode_titles
    + years
    + series_types
    + content_types
    + release_info
    + video_audio
    + complex_fixtures
)

with_db = basic_episodes_db

table = heuristic + with_db
