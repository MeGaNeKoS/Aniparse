from aniparse.output_schemas import SequenceNumber, SeriesInfo, Metadata
from tests.conftest import Fixture

folder_context = [
    # 1. Bare episode filename — folder provides title
    Fixture(
        path="My Series/01.mkv",
        metadata=Metadata(
            file_name="01.mkv",
            file_extension="mkv",
            series=[
                SeriesInfo(
                    title="My Series",
                    episode=[SequenceNumber(number=1)],
                )
            ],
        ),
    ),
    # 2. Folder with year
    Fixture(
        path="My Series (2024)/01.mkv",
        metadata=Metadata(
            file_name="01.mkv",
            file_extension="mkv",
            series=[
                SeriesInfo(
                    title="My Series",
                    year=[SequenceNumber(number=2024)],
                    episode=[SequenceNumber(number=1)],
                )
            ],
        ),
    ),
    # 3. Nested folders: title + season from folders, episode from file
    Fixture(
        path="My Series/Season 2/01.mkv",
        metadata=Metadata(
            file_name="01.mkv",
            file_extension="mkv",
            series=[
                SeriesInfo(
                    title="My Series",
                    season=[SequenceNumber(number=2)],
                    episode=[SequenceNumber(number=1)],
                )
            ],
        ),
    ),
    # 4. Multi-season outer narrowed by inner season folder
    Fixture(
        path="series s1+s2+s3/season1/01 - surge.mkv",
        metadata=Metadata(
            file_name="01 - surge.mkv",
            file_extension="mkv",
            series=[
                SeriesInfo(
                    title="series",
                    season=[SequenceNumber(number=1)],
                    episode=[SequenceNumber(number=1, title="surge")],
                )
            ],
        ),
    ),
    # 5. Bare number folder as season (not episode)
    Fixture(
        path="My Series/1/01.mkv",
        metadata=Metadata(
            file_name="01.mkv",
            file_extension="mkv",
            series=[
                SeriesInfo(
                    title="My Series",
                    season=[SequenceNumber(number=1)],
                    episode=[SequenceNumber(number=1)],
                )
            ],
        ),
    ),
    # 6. Bare number folder narrows multi-season outer
    Fixture(
        path="series s1+s2+s3/1/01 - surge.mkv",
        metadata=Metadata(
            file_name="01 - surge.mkv",
            file_extension="mkv",
            series=[
                SeriesInfo(
                    title="series",
                    season=[SequenceNumber(number=1)],
                    episode=[SequenceNumber(number=1, title="surge")],
                )
            ],
        ),
    ),
    # 7. Filename has its own title — folder title does NOT override
    Fixture(
        path="Other Title/[Group] My Title - 01 [1080p].mkv",
        metadata=Metadata(
            file_name="[Group] My Title - 01 [1080p].mkv",
            file_extension="mkv",
            release_group=["Group"],
            video_resolution=[],  # just checking title isn't overridden
            series=[
                SeriesInfo(
                    title="My Title",
                    episode=[SequenceNumber(number=1)],
                )
            ],
        ),
    ),
    # 8. Folder with season inline (S2), episode + title from file
    Fixture(
        path="My Series S2/01 - Episode Title.mkv",
        metadata=Metadata(
            file_name="01 - Episode Title.mkv",
            file_extension="mkv",
            series=[
                SeriesInfo(
                    title="My Series",
                    season=[SequenceNumber(number=2)],
                    episode=[SequenceNumber(number=1, title="Episode Title")],
                )
            ],
        ),
    ),
    # 9. Folder with type (OVA)
    Fixture(
        path="My Series/OVA/01.mkv",
        metadata=Metadata(
            file_name="01.mkv",
            file_extension="mkv",
            series=[
                SeriesInfo(
                    title="My Series",
                    type="OVA",
                    episode=[SequenceNumber(number=1)],
                )
            ],
        ),
    ),
]
