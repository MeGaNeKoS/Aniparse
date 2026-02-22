# Aniparse

A probability-based anime filename parser for Python.

Aniparse parses anime video filenames into structured metadata. Unlike regex-based approaches, it uses a **scoring engine** where confidence accumulates from multiple signals — position, context, keywords, and patterns — so it handles the wild variety of fansub naming conventions gracefully.

Based on the C++ library [Anitomy](https://github.com/erengy/anitomy), redesigned from the ground up in v2.

## Installation

```
pip install aniparse
```

## Usage

```python
import aniparse

aniparse.parse('[TaigaSubs]_Toradora!_(2008)_-_01v2_-_Tiger_and_Dragon_[1280x720_H.264_FLAC][1234ABCD].mkv')
```

```python
{
    'file_name': '[TaigaSubs]_Toradora!_(2008)_-_01v2_-_Tiger_and_Dragon_[1280x720_H.264_FLAC][1234ABCD].mkv',
    'audio_term': ['FLAC'],
    'file_extension': 'mkv',
    'file_checksum': '1234ABCD',
    'video_resolution': [{'video_height': 720, 'video_width': 1280}],
    'release_version': ['2'],
    'release_group': ['TaigaSubs'],
    'series': [{
        'title': 'Toradora!',
        'year': [{'number': 2008}],
        'episode': [{'number': 1, 'release_version': '2', 'title': 'Tiger and Dragon'}],
    }],
    'video_term': ['H.264'],
}
```

The `parse` function returns a dict with all identified metadata, or `None` if the input is empty.

### Alternative titles

Pipe `|` is a first-class separator. Each segment after the first becomes an alternative series entry:

```python
aniparse.parse('[TROLLORANGE] Hell Girl Season 4 (CR WEB-DL 1080p x264 AAC) | Hell Girl: Fourth Twilight')
```

```python
{
    'file_name': '[TROLLORANGE] Hell Girl Season 4 (CR WEB-DL 1080p x264 AAC) | Hell Girl: Fourth Twilight',
    'audio_term': ['AAC'],
    'video_resolution': [{'video_height': 1080, 'scan_method': 'p'}],
    'release_group': ['TROLLORANGE'],
    'release_information': ['CR'],
    'series': [
        {'title': 'Hell Girl', 'season': [{'number': 4}]},
        {'title': 'Hell Girl: Fourth Twilight'},
    ],
    'source': ['WEB-DL'],
    'video_term': ['x264'],
}
```

### Path and folder context

```python
# Parse from a full path
aniparse.parse('', path='/anime/Toradora/[Group] Toradora! - 01.mkv')

# Or pass folder separately
aniparse.parse('[Group] Toradora! - 01.mkv', folder='/anime/Toradora')
```

```python
# aniparse.parse('[Group] Toradora! - 01.mkv', folder='/anime/Toradora')
{
    'file_name': '[Group] Toradora! - 01.mkv',
    'file_extension': 'mkv',
    'release_group': ['Group'],
    'series': [
        {'title': 'Toradora!', 'episode': [{'number': 1}]},
    ],
    'folder_name': '/anime/Toradora',
}

# aniparse.parse('01 - surge.mkv', path='series s1+s2+s3/season1/01 - surge.mkv')
{
    'file_name': '01 - surge.mkv',
    'file_extension': 'mkv',
    'series': [{
        'episode': [{'number': 1, 'title': 'surge'}],
        'title': 'series',
        'season': [{'number': 1}],
    }],
    'folder_name': 'series s1+s2+s3/season1',
}
```

### Custom instance

For repeated parsing with custom settings:

```python
from aniparse import Aniparse, ParserConfig

parser = Aniparse(config=ParserConfig(fuzzy=True))
result = parser.parse('[Group] Title - 01 [1080p].mkv')
```

### Custom keywords

Provide your own `WordListManager` to extend or replace the built-in keyword lists:

```python
from aniparse import Aniparse, WordListManager

parser = Aniparse(wordlist_provider=my_wordlist_manager)
result = parser.parse(filename)
```

### Debug mode

Pass `debug=True` to include the token scoring breakdown in the output:

```python
aniparse.parse(filename, debug=True)
```

## Output structure

The output is a flat dict with these top-level keys:

| Key | Type | Description |
|---|---|---|
| `file_name` | `str` | Original input filename |
| `file_extension` | `str` | File extension |
| `file_checksum` | `str` | CRC32 checksum (e.g. `1234ABCD`) |
| `file_index` | `int` | File index number |
| `series` | `list[SeriesInfo]` | Series metadata (title, episodes, seasons, etc.) |
| `audio_term` | `list[str]` | Audio codec terms (FLAC, AAC, etc.) |
| `video_term` | `list[str]` | Video codec terms (H.264, x265, etc.) |
| `video_resolution` | `list[VideoResolution]` | Resolution info (height, width, scan method) |
| `source` | `list[str]` | Source terms (Blu-ray, WEB-DL, etc.) |
| `release_group` | `list[str]` | Release group names |
| `release_information` | `list[str]` | Release info (BATCH, REMASTER, etc.) |
| `release_version` | `list[str]` | Version strings |
| `language` | `list[str]` | Language tags |
| `subs_term` | `list[str]` | Subtitle terms (Subbed, Hardsub, etc.) |
| `device_compatibility` | `list[str]` | Device compatibility tags |

Each `SeriesInfo` contains:

| Key | Type | Description |
|---|---|---|
| `title` | `str` | Series title |
| `type` | `str` | Series type (OVA, Movie, TV, Special, etc.) |
| `year` | `list[Sequence]` | Year(s) |
| `season` | `list[Sequence]` | Season number(s) |
| `episode` | `list[Sequence]` | Episode number(s), with optional `title`, `release_version`, `part` |
| `volume` | `list[Sequence]` | Volume number(s) |
| `content_type` | `list[Sequence]` | Content type (NCOP, NCED, PV, etc.) with optional `identifier` |

Episode/season/volume entries support ranges (`start`/`end`), totals (`number`, `total` for "X of Y"), and alternatives.

Only present keys are included — `None` values are omitted.

## Configuration

`ParserConfig` options:

| Attribute | Type | Default | Description |
|---|---|---|---|
| `year_min` | `int` | `1900` | Minimum valid year |
| `year_max` | `int` | `2099` | Maximum valid year |
| `range_total` | `set[str]` | `{"of"}` | Connectors for "X of Y" patterns |
| `range_separator` | `set[str]` | `{"-", "~", "&", "+"}` | Range delimiters |
| `fuzzy` | `bool` | `False` | Enable fuzzy keyword matching |
| `fuzzy_threshold` | `float` | `0.8` | Fuzzy match threshold |

## How does it work?

Aniparse processes filenames through a six-stage pipeline:

1. **Tokenize** — Split input into tokens, detecting brackets, delimiters, and text boundaries
2. **Identify** — Match tokens against keyword lists, assigning initial possibilities with base scores
3. **Expand** — Pattern-based rules add new possibilities (checksums, numbers, years, titles, etc.)
4. **Score** — Context-aware rules adjust confidence based on position, neighbors, brackets, and structural zones
5. **Resolve** — Pick the winning possibility per token based on highest score
6. **Compose** — Assemble tokens into the final metadata dict

This approach avoids hardcoded rules like "first bracket = release group". Instead, each token accumulates evidence from multiple signals, and the highest-confidence interpretation wins.

## Why use Aniparse?

Anime filenames are notoriously inconsistent:

- Element order varies between groups
- Brackets and parentheses may be metadata containers or part of the title
- Multiple delimiter styles coexist in a single filename
- Numbers are ambiguous (episode? season? year? resolution?)

Regex-based parsers can't cover the combinatorial explosion of conventions. Aniparse's scoring approach handles tens of thousands of filenames with high accuracy.

## Known limitations

- Single-letter "E" episode prefix can be too aggressive in brackets
- Number-dash-number in titles (e.g., `009-1`) may be parsed as episode ranges
- CJK language descriptors may be included in the title
- Parenthesized alternative series after metadata may not be detected

## License

*Aniparse* is licensed under [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/FAQ/).
