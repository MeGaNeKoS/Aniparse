from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Optional, List, TypeVar, Generic, Union


def _to_dict(obj, skip_none=True) -> dict:
    """Auto-generate dict from dataclass, recursing into nested dataclasses/lists."""
    result = {}
    for f in fields(obj):
        value = getattr(obj, f.name)
        if skip_none and value is None:
            continue
        if isinstance(value, list):
            converted = [item.to_dict() if hasattr(item, 'to_dict') else item for item in value]
            if skip_none and not converted:
                continue
            result[f.name] = converted
        elif hasattr(value, 'to_dict'):
            result[f.name] = value.to_dict()
        else:
            result[f.name] = value
    return result


def _from_dict(cls, data: dict):
    """Auto-generate instance from dict, using field metadata for nested types."""
    kwargs = {}
    for f in fields(cls):
        if f.name not in data:
            continue
        deserializer = f.metadata.get("from_dict")
        if deserializer:
            kwargs[f.name] = deserializer(data[f.name])
        else:
            kwargs[f.name] = data[f.name]
    return cls(**kwargs)


@dataclass
class VideoResolution:
    video_height: Optional[int] = None
    video_width: Optional[int] = None
    scan_method: Optional[str] = None

    def to_dict(self) -> dict:
        return _to_dict(self)

    @staticmethod
    def from_dict(data: dict) -> VideoResolution:
        return _from_dict(VideoResolution, data)


@dataclass
class SequenceNumber:
    number: int | float
    total: Optional[int | float] = None
    release_version: Optional[str] = None
    title: Optional[str] = None
    part: Optional[str] = None
    alternative: Optional[List[SequenceNumber]] = field(
        default_factory=list,
        metadata={"from_dict": lambda v: [SequenceNumber.from_dict(alt) for alt in v]}
    )

    def to_dict(self) -> dict:
        return _to_dict(self)

    @staticmethod
    def from_dict(data: dict) -> SequenceNumber:
        return _from_dict(SequenceNumber, data)


@dataclass
class SequenceIdentifierNumber(SequenceNumber):
    identifier: Optional[str] = None
    number: Optional[int | float] = None
    alternative: Optional[List[SequenceIdentifierNumber]] = field(
        default_factory=list,
        metadata={"from_dict": lambda v: [SequenceIdentifierNumber.from_dict(alt) for alt in v]}
    )

    def to_dict(self) -> dict:
        return _to_dict(self)

    @staticmethod
    def from_dict(data: dict) -> SequenceIdentifierNumber:
        return _from_dict(SequenceIdentifierNumber, data)


T = TypeVar('T', SequenceNumber, SequenceIdentifierNumber)


def _deserialize_sequence(seq: dict) -> Sequence:
    """Dispatch a single sequence dict to SequenceRange, SequenceIdentifierNumber, or SequenceNumber."""
    if "start" in seq and "end" in seq:
        return SequenceRange.from_dict(seq)
    elif "identifier" in seq:
        return SequenceIdentifierNumber.from_dict(seq)
    else:
        return SequenceNumber.from_dict(seq)


def _deserialize_sequence_list(v: list) -> list:
    return [_deserialize_sequence(seq) for seq in v]


def _deserialize_identifier_sequence_list(v: list) -> list:
    """For content_type: default to SequenceIdentifierNumber."""
    result = []
    for seq in v:
        if "start" in seq and "end" in seq:
            result.append(SequenceRange.from_dict(seq))
        else:
            result.append(SequenceIdentifierNumber.from_dict(seq))
    return result


@dataclass
class SequenceRange(Generic[T]):
    start: T
    end: T
    alternative: Optional[List[SequenceRange[T]]] = field(default_factory=list)

    def __post_init__(self):
        if type(self.start) is not type(self.end):
            raise ValueError("Start and end must be of the same type")

    def to_dict(self) -> dict:
        return _to_dict(self)

    @staticmethod
    def from_dict(data: dict) -> SequenceRange[T]:
        start_data = data.get("start", {})
        end_data = data.get("end", {})

        if "identifier" in start_data:
            start = SequenceIdentifierNumber.from_dict(start_data)
        else:
            start = SequenceNumber.from_dict(start_data)

        if "identifier" in end_data:
            end = SequenceIdentifierNumber.from_dict(end_data)
        else:
            end = SequenceNumber.from_dict(end_data)

        return SequenceRange(start=start, end=end)


Sequence = Union[T, SequenceRange[T]]


@dataclass
class SeriesInfo:
    title: Optional[str] = None
    type: Optional[str] = None
    year: Optional[List[Sequence[SequenceNumber]]] = field(
        default=None,
        metadata={"from_dict": _deserialize_sequence_list}
    )
    season: Optional[List[Sequence[SequenceNumber]]] = field(
        default=None,
        metadata={"from_dict": _deserialize_sequence_list}
    )
    episode: Optional[List[Sequence[SequenceNumber]]] = field(
        default=None,
        metadata={"from_dict": _deserialize_sequence_list}
    )
    volume: Optional[List[Sequence[SequenceNumber]]] = field(
        default=None,
        metadata={"from_dict": _deserialize_sequence_list}
    )
    content_type: Optional[List[Sequence[SequenceIdentifierNumber]]] = field(
        default=None,
        metadata={"from_dict": _deserialize_identifier_sequence_list}
    )

    def to_dict(self) -> dict:
        return _to_dict(self)

    @staticmethod
    def from_dict(data: dict) -> SeriesInfo:
        return _from_dict(SeriesInfo, data)


@dataclass
class Metadata:
    file_name: str
    audio_term: Optional[List[str]] = None
    device_compatibility: Optional[List[str]] = None
    file_extension: Optional[str] = None
    file_checksum: Optional[str] = None
    file_index: Optional[int] = None
    language: Optional[List[str]] = None
    video_resolution: Optional[List[VideoResolution]] = field(
        default=None,
        metadata={"from_dict": lambda v: [VideoResolution.from_dict(vr) for vr in v]}
    )
    release_version: Optional[List[str]] = None
    release_group: Optional[List[str]] = None
    release_information: Optional[List[str]] = None
    series: List[SeriesInfo] = field(
        default=None,
        metadata={"from_dict": lambda v: [SeriesInfo.from_dict(s) for s in v]}
    )
    source: Optional[List[str]] = None
    subs_term: Optional[List[str]] = None
    video_term: Optional[List[str]] = None
    other: Optional[List[str]] = None
    unknown: Optional[List[str]] = None

    def to_dict(self) -> dict:
        return _to_dict(self)

    @staticmethod
    def from_dict(data: dict) -> Metadata:
        return _from_dict(Metadata, data)
