type SequenceBase = {
    total?: number;
    release_version?: string;
    title?: string;
    part?: string;
}
type SequenceNumber = SequenceBase & {
    number: number;
}

// Extended of Sequence number for `extras` file. `NCED`, `PV`, etc.
type SequenceIdentifierNumber = SequenceBase & {
    identifier: string;
    number?: number;
}

// Defines a range of episodes or volumes, from a start to an end point. E.g 1-25
type SequenceRange<T> = {
    start: T;
    end: T;
}

type SequenceAlternative<T> = T & {
    alternative?: T[]
}

type Sequence<T> = SequenceAlternative<T> | SequenceAlternative<SequenceRange<T>>

// Comprehensive information about a series, including titles, types, and various sequences. E.g:
type SeriesInfo = {
    title?: string;
    type?: string;
    year?: Sequence<SequenceNumber>[];
    season?: Sequence<SequenceNumber>[];
    episode?: Sequence<SequenceNumber>[];
    volume?: Sequence<SequenceNumber>[];
    content_type?: Sequence<SequenceIdentifierNumber>[];
}

type VideoResolution = {
    video_height?: number;
    video_width?: number;
    scan_method?: "p" | "i" | "P" | "I";
}

export type Metadata = {
    audio_term?: string[];
    device_compatibility?: string[];
    file_name: string;
    file_extension?: string;
    file_checksum?: string;
    file_index?: number;
    language?: string[];
    video_resolution?: VideoResolution[];
    release_version?: string[];
    release_group?: string[];
    release_information?: string[];
    series: SeriesInfo[];
    source?: string[];
    subs_term?: string[];
    video_term?: string[];
    other?: string[];
    unknown?: string[];
}