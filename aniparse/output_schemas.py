import numbers
from dataclasses import dataclass, field
from typing import Optional, Dict, List, TypeVar, Generic, Union

from aniparse.token_tags import Descriptor


@dataclass
class VideoResolution:
    height: Optional[int] = None
    width: Optional[int] = None
    scan_method: Optional[str] = None

    def to_dict(self) -> dict:
        data = {
            Descriptor.VIDEO_HEIGHT.value: self.height,
            Descriptor.VIDEO_WIDTH.value: self.width,
            Descriptor.SCAN_METHOD.value: self.scan_method
        }
        data = {key: value for key, value in data.items() if value}
        return data

    @staticmethod
    def from_dict(data: dict, custom_mapper: Optional[Dict[str, str]] = None) -> 'VideoResolution':
        default_mapper = {
            Descriptor.VIDEO_HEIGHT.value: "height",
            Descriptor.VIDEO_WIDTH.value: "width",
            Descriptor.SCAN_METHOD.value: "scan_method"
        }

        if isinstance(custom_mapper, dict):
            default_mapper.update(custom_mapper)

        normalized_data = {default_mapper.get(k, k): v for k, v in data.items() if default_mapper.get(k, None)}
        return VideoResolution(**normalized_data)


@dataclass
class SequenceNumber:
    number: numbers.Number
    total: Optional[numbers.Number] = None
    release_version: Optional[str] = None
    title: Optional[str] = None
    part: Optional[str] = None
    alternative: Optional[List['SequenceNumber']] = field(default_factory=list)

    def to_dict(self) -> dict:
        data = {
            Descriptor.SEQUENCE_NUMBER.value: self.number,
            Descriptor.SEQUENCE_TOTAL.value: self.total,
            Descriptor.RELEASE_VERSION.value: self.release_version,
            Descriptor.SEQUENCE_TITLE.value: self.title,
            Descriptor.SEQUENCE_PART.value: self.part,
            Descriptor.SEQUENCE_ALTERNATIVE.value: [alt.to_dict() for alt in
                                                    self.alternative] if self.alternative else None
        }
        data = {key: value for key, value in data.items() if value}
        return data

    @staticmethod
    def from_dict(data: dict, custom_mapper: Optional[Dict[str, str]] = None) -> 'SequenceNumber':
        default_mapper = {
            Descriptor.SEQUENCE_NUMBER.value: "number",
            Descriptor.SEQUENCE_ALTERNATIVE.value: "alternative",
            Descriptor.SEQUENCE_TOTAL.value: "total",
            Descriptor.RELEASE_VERSION.value: "release_version",
            Descriptor.SEQUENCE_TITLE.value: "title",
            Descriptor.SEQUENCE_PART.value: "part"
        }

        if custom_mapper:
            default_mapper.update(custom_mapper)

        normalized_data = {default_mapper.get(k, k): v for k, v in data.items() if default_mapper.get(k, None)}

        if 'alternative' in normalized_data:
            normalized_data['alternative'] = [
                SequenceNumber.from_dict(alt) for alt in normalized_data['alternative']
            ]

        return SequenceNumber(**normalized_data)


@dataclass
class SequenceIdentifierNumber(SequenceNumber):
    identifier: Optional[str] = None
    number: Optional[numbers.Number] = None
    alternative: Optional[List['SequenceIdentifierNumber']] = field(default_factory=list)

    def to_dict(self) -> dict:
        base_data = super().to_dict()

        base_data[Descriptor.CONTENT_IDENTIFIER.value] = self.identifier

        data = {key: value for key, value in base_data.items() if value}
        return data

    @staticmethod
    def from_dict(data: dict, custom_mapper: Optional[Dict[str, str]] = None) -> 'SequenceIdentifierNumber':
        default_mapper = {
            Descriptor.CONTENT_IDENTIFIER.value: "identifier"
        }

        if custom_mapper:
            default_mapper.update(custom_mapper)

        normalized_data = {default_mapper.get(k, k): v for k, v in data.items() if default_mapper.get(k, None)}

        return SequenceIdentifierNumber(**normalized_data)


T = TypeVar('T', SequenceNumber, SequenceIdentifierNumber)


@dataclass
class SequenceRange(Generic[T]):
    start: T
    end: T
    alternative: Optional[List['SequenceRange[T]']] = field(default_factory=list)

    def __post_init__(self):
        if type(self.start) is not type(self.end):
            print(f"Start: {self.start} - {type(self.start)}")
            print(f"End: {self.end} - {type(self.end)}")
            raise ValueError("Start and end must be of the same type")

    def to_dict(self) -> dict:
        data = {
            Descriptor.SEQUENCE_START.value: self.start.to_dict(),
            Descriptor.SEQUENCE_END.value: self.end.to_dict()
        }
        data = {key: value for key, value in data.items() if value}
        return data

    @staticmethod
    def from_dict(data: dict, custom_mapper: Optional[Dict[str, str]] = None) -> 'SequenceRange[T]':
        default_mapper = {
            Descriptor.SEQUENCE_START.value: "start",
            Descriptor.SEQUENCE_END.value: "end"
        }
        if custom_mapper:
            default_mapper.update(custom_mapper)

        normalized_data = {default_mapper.get(k, k): v for k, v in data.items() if default_mapper.get(k, None)}

        if "start" in normalized_data:
            if "identifier" in normalized_data["start"]:
                normalized_data['start'] = SequenceIdentifierNumber.from_dict(normalized_data["start"])
            else:
                normalized_data['start'] = SequenceNumber.from_dict(normalized_data["start"])
        if "end" in normalized_data:
            if "identifier" in normalized_data["end"]:
                normalized_data['end'] = SequenceIdentifierNumber.from_dict(normalized_data["end"])
            else:
                normalized_data['end'] = SequenceNumber.from_dict(normalized_data["end"])

        return SequenceRange(**normalized_data)


Sequence = Union[T, SequenceRange[T]]


@dataclass
class SeriesInfo:
    title: Optional[str] = None
    type: Optional[str] = None
    year: Optional[List[Sequence[SequenceNumber]]] = None
    season: Optional[List[Sequence[SequenceNumber]]] = None
    episode: Optional[List[Sequence[SequenceNumber]]] = None
    volume: Optional[List[Sequence[SequenceNumber]]] = None
    content_type: Optional[List[Sequence[SequenceIdentifierNumber]]] = None

    def to_dict(self) -> dict:
        data = {
            Descriptor.SERIES_TITLE.value: self.title,
            Descriptor.SERIES_TYPE.value: self.type,
            Descriptor.SERIES_YEAR.value: [seq.to_dict() for seq in self.year] if self.year else None,
            Descriptor.SEASON.value: [seq.to_dict() for seq in self.season] if self.season else None,
            Descriptor.EPISODE.value: [seq.to_dict() for seq in self.episode] if self.episode else None,
            Descriptor.VOLUME.value: [seq.to_dict() for seq in self.volume] if self.volume else None,
            Descriptor.CONTENT_TYPE.value: [seq.to_dict() for seq in
                                            self.content_type] if self.content_type else None,
        }
        data = {key: value for key, value in data.items() if value is not None}
        return data

    @staticmethod
    def from_dict(data: dict, custom_mapper: Optional[Dict[str, str]] = None) -> 'SeriesInfo':
        default_mapper = {
            Descriptor.SERIES_TITLE.value: "title",
            Descriptor.SERIES_TYPE.value: "type",
            Descriptor.SERIES_YEAR.value: "year",
            Descriptor.SEASON.value: "season",
            Descriptor.EPISODE.value: "episode",
            Descriptor.VOLUME.value: "volume",
            Descriptor.CONTENT_TYPE.value: "content_type",
        }

        if custom_mapper:
            default_mapper.update(custom_mapper)

        normalized_data = {default_mapper.get(k, k): v for k, v in data.items() if default_mapper.get(k, None)}

        for key, value in normalized_data.items():
            if key in ["year", "season", "episode", "volume", "content_type"]:
                if "start" in value and "end" in value:
                    sequences = []
                    for seq in value:
                        sequences.append(SequenceRange.from_dict(seq, custom_mapper))
                    normalized_data[key] = sequences
                elif "identifier" in value:
                    sequences = []
                    for seq in value:
                        sequences.append(SequenceIdentifierNumber.from_dict(seq, custom_mapper))
                    normalized_data[key] = sequences
                else:
                    sequences = []
                    for seq in value:
                        sequences.append(SequenceNumber.from_dict(seq, custom_mapper))
                    normalized_data[key] = sequences
            elif key == "content_type":
                sequences = []
                for seq in value:
                    sequences.append(SequenceIdentifierNumber.from_dict(seq, custom_mapper))
                normalized_data[key] = sequences

        return SeriesInfo(**normalized_data)


@dataclass
class Metadata:
    file_name: str
    audio_term: Optional[List[str]] = None
    device_compatibility: Optional[List[str]] = None
    file_extension: Optional[str] = None
    file_checksum: Optional[str] = None
    file_index: Optional[int] = None
    language: Optional[List[str]] = None
    video_resolution: Optional[List[VideoResolution]] = None  # dataclass
    release_version: Optional[List[str]] = None
    release_group: Optional[List[str]] = None
    release_information: Optional[List[str]] = None
    series: List[SeriesInfo] = None  # dataclass
    source: Optional[List[str]] = None
    subs_term: Optional[List[str]] = None
    video_term: Optional[List[str]] = None
    other: Optional[List[str]] = None
    unknown: Optional[List[str]] = None

    def to_dict(self):
        data = {
            Descriptor.FILE_NAME.value: self.file_name,
            Descriptor.AUDIO_TERM.value: self.audio_term,
            Descriptor.DEVICE_COMPATIBILITY.value: self.device_compatibility,
            Descriptor.FILE_EXTENSION.value: self.file_extension,
            Descriptor.FILE_CHECKSUM.value: self.file_checksum,
            Descriptor.FILE_INDEX.value: self.file_index,
            Descriptor.LANGUAGE.value: self.language,
            Descriptor.VIDEO_RESOLUTION.value: [vr.to_dict() for vr in
                                                self.video_resolution] if self.video_resolution else None,
            Descriptor.RELEASE_VERSION.value: self.release_version,
            Descriptor.RELEASE_GROUP.value: self.release_group,
            Descriptor.RELEASE_INFORMATION.value: self.release_information,
            Descriptor.SERIES.value: [s.to_dict() for s in self.series] if self.series else None,
            Descriptor.SOURCE.value: self.source,
            Descriptor.SUBS_TERM.value: self.subs_term,
            Descriptor.VIDEO_TERM.value: self.video_term,
            Descriptor.OTHER.value: self.other,
            Descriptor.UNKNOWN.value: self.unknown,
        }
        data = {key: value for key, value in data.items() if value}
        return data

    @staticmethod
    def from_dict(data: dict, custom_mapper: Optional[Dict[str, str]] = None) -> 'Metadata':
        default_mapper = {
            Descriptor.FILE_NAME.value: "file_name",
            Descriptor.AUDIO_TERM.value: "audio_term",
            Descriptor.DEVICE_COMPATIBILITY.value: "device_compatibility",
            Descriptor.FILE_EXTENSION.value: "file_extension",
            Descriptor.FILE_CHECKSUM.value: "file_checksum",
            Descriptor.FILE_INDEX.value: "file_index",
            Descriptor.LANGUAGE.value: "language",
            Descriptor.VIDEO_RESOLUTION.value: "video_resolution",
            Descriptor.RELEASE_VERSION.value: "release_version",
            Descriptor.RELEASE_GROUP.value: "release_group",
            Descriptor.RELEASE_INFORMATION.value: "release_information",
            Descriptor.SERIES.value: "series",
            Descriptor.SOURCE.value: "source",
            Descriptor.SUBS_TERM.value: "subs_term",
            Descriptor.VIDEO_TERM.value: "video_term",
            Descriptor.OTHER.value: "other",
            Descriptor.UNKNOWN.value: "unknown",
        }
        if custom_mapper:
            default_mapper.update(custom_mapper)

        normalized_data = {default_mapper.get(k, k): v for k, v in data.items() if default_mapper.get(k, None)}

        if normalized_data.get("series"):
            series = []
            for series_str in normalized_data["series"]:
                series.append(SeriesInfo.from_dict(series_str, default_mapper))
            normalized_data["series"] = series

        if normalized_data.get("video_resolution"):
            resolution = []
            for resolution_str in normalized_data["video_resolution"]:
                resolution.append(VideoResolution.from_dict(resolution_str, default_mapper))
            normalized_data["video_resolution"] = resolution

        return Metadata(**normalized_data)
