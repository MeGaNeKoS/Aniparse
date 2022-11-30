# Aniparse

Aniparse is a Python library for parsing anime video filenames. It's simple to use, and it's based on the C++
library [Anitomy](https://github.com/erengy/anitomy) with a lot of improvement.

## Example

The following filename

```
[TaigaSubs]_Toradora!_(2008)_-_01v2_-_Tiger_and_Dragon_[1280x720_H.264_FLAC][1234ABCD].mkv
Toradora! S01E03-Your Song.mkv
```

can be parsed using the following code:

```python
import aniparse

aniparse.parse('[TaigaSubs]_Toradora!_(2008)_-_01v2_-_Tiger_and_Dragon_[1280x720_H.264_FLAC][1234ABCD].mkv')
{
    'anime_title': 'Toradora!',
    'anime_year': 2008,
    'audio_term': 'FLAC',
    'episode_number': 1,
    'episode_title': 'Tiger and Dragon',
    'file_checksum': '1234ABCD',
    'file_extension': 'mkv',
    'file_name': '[TaigaSubs]_Toradora!_(2008)_-_01v2_-_Tiger_and_Dragon_[1280x720_H.264_FLAC][1234ABCD].mkv',
    'release_group': 'TaigaSubs',
    'release_version': 2,
    'video_resolution': '1280x720',
    'video_term': 'H.264'
}

aniparse.parse("Toradora! S01E03-Your Song.mkv")
{
    'anime_season': 1,
    'anime_season_prefix': 'S',
    'anime_title': 'Toradora!',
    'episode_number': 3,
    'episode_prefix': 'E',
    'episode_title': 'Your Song',
    'file_extension': 'mkv',
    'file_name': 'Toradora! S01E03-Your Song.mkv'
}
```

The `parse` function receives a string and returns a dictionary containing all found elements.
It can also receive parsing `options` and `keyword_manager`, this will be explained below.

# How does it work?

Suppose that we're working on the following filename:

```text
"Aim_For_The_Top!_Gunbuster-ep1.BD(H264.FLAC.10bit)[KAA][69ECCDCF].mkv"
```

The filename is first stripped off of its extension and split into groups. Groups are determined by the position of
brackets:

```text
"Aim_For_The_Top!_Gunbuster-ep1.BD", "H264.FLAC.10bit", "KAA", "69ECCDCF"
```

Each group is then split into tokens. In our current example, the delimiter for the enclosed group is `.`, while the
words in other groups are separated by `_`:

```text
"Aim", "For", "The", "Top!", "Gunbuster-ep1", "BD", "H264", "FLAC", "10bit", "KAA", "69ECCDCF"
```

Note: the brackets and delimiter are stored as token with category `Delimiter` and `Bracket`. And each token remembers
if it enclosed or not.

Once the tokenizer is done, the parser comes into effect.
First, all tokens are compared against a set of known keywords. In this case,
the tokens `BD`, `H264`, `FLAC`, `10bit`, and `69ECCDCF` are recognized as keywords,
and are assigned the category `Source`, `VideoTerm`, `AudioTerm`, `VideoResolution`, and `FileChecksum` respectively.

```text
"Aim", "For", "The", "Top!", "Gunbuster-ep1", "KAA"
```

The next step is to look for the episode number. Each token that contains a number is analyzed. Here.
`Gunbuster-ep1` contains number, but it doesn't match the episode number pattern. In this case,
the token checked againts buggy dash pattern. So, `Gunbuster-ep1` will be split into `Gunbuster` and `ep1`.
After that, it will check and `ep1` is recognized as an episode number.
The category `EpisodeNumber` is assigned to it and the changes is saved.

```text
"Aim", "For", "The", "Top!", "Gunbuster", "KAA"
```

The next step is to look for the anime title. The parser will try to find unknown token before the episode number and
not inside a bracket.
In this case, `Aim`, `For`, `The`, `Top!`, and `Gunbuster` are unknown tokens, they are not inside a bracket, so it
assigned to the `AnimeTitle` category.

```text
"KAA"
```

the next step is to look for the release group. The parser will try to find unknown token after the episode number and
inside a bracket.
In this case, `KAA` is unknown token, and it inside a bracket, so it assigned to the `ReleaseGroup` category.

```text
```

the next step is to look for the episode title. The parser will try to find unknown token after the episode number and
not inside a bracket.
In this case, no more unknown token left, so it leave it empty

```text
```

lastly, the parser will try to find any unknown token and assign it to each category or to `Others` if it is not
recognized.

# Why should I use it?

Anime video files are commonly named in a format where the anime title is followed by the episode number,
and all the technical details are enclosed within brackets.
However, fansub groups tend to use their own naming conventions,
and the problem is more complicated than it first appears:

    Element order is not always the same.
    Technical information is not guaranteed to be enclosed.
    Brackets and parentheses may be grouping symbols or a part of the anime/episode title.
    Space and underscore are not the only delimiters in use.
    A single filename may contain multiple delimiters.

There are so many cases to cover that it's simply not possible to parse all filenames solely with
regular expressions. Aniparse tries a different approach, and it succeeds:
It's able to parse tens of thousands of filenames, with great accuracy.

# Are there any exceptions?

Yes, unfortunately. Aniparse fails to identify the anime title and episode number on rare occasions,
mostly due to bad naming conventions. See the examples below.

    Arigatou.Shuffle!.Ep08.[x264.AAC][D6E43829].mkv

Here, Aniparse would report that this file is the 8th episode of `Arigatou Shuffle!`, where `Arigatou` is actually the
name of the fansub group.

    Spice and Wolf 2

Is this the 2nd episode of `Spice and Wolf`, or a batch release of `Spice and Wolf 2`? with a text after number, there's
no way to know. It's up to you consider both cases. For current version, it treats as part of title if it's not leading zero,
and as episode number if it's leading zero.

## Suggestions to fansub groups

Please consider abiding by these simple rules before deciding on your naming convention:

- Don't enclose anime title, episode number and episode title within brackets. Enclose everything else, including the
  name of your group.
- Don't use parentheses to enclose release information; use square brackets instead. Parentheses should only be used if
  they are a part of the anime/episode title.
- Don't use multiple delimiters in a single filename. If possible, stick with either space or underscore.
- Use a separator (e.g. a dash) between anime title and episode number. There are anime titles that end with a number,
  which creates ambiguity.
- Indicate the episode interval in batch releases.

## Installation

To install Aniparse, simply use pip:

```commandline
pip install aniparse
```

Or download the source code and inside the source code's folder run:

```commandline
python setup.py install
```

Options
-------

The `parse` function can receive the `options` parameter. E.g.:

```python

import aniparse

aniparse_options = {'allowed_delimiters': ' '}
aniparse.parse('DRAMAtical Murder Episode 1 - Data_01_Login', options=aniparse_options)
{
    'anime_title': 'DRAMAtical Murder',
    'episode_prefix': 'Episode',
    'episode_number': '1',
    'episode_title': 'Data_01_Login',
    'file_name': 'DRAMAtical Murder Episode 1 - Data_01_Login'
}
```

If the default options had been used, the parser would have considered `_` as a delimiter and replaced it with space in
the episode title.

The options contain the following attributes:

| **Attribute name**   | **Type**        | **Description**                                                 | **Default value** |
|----------------------|-----------------|-----------------------------------------------------------------|-------------------|
| allowed_delimiters   | string          | The list of character to be considered as delimiters.           | ' _.&+,&#124;'    |
| check_title_enclosed | boolean         | Check the anime title in enclosed if no title found             | True              |
| eps_lower_than_alt   | boolean         | Set episode number to the lowest and the alt to be the highest  | True              |
| ignored_dash         | boolean         | If the dash in anime/episode title should be ignored or not.    | True              |
| ignored_strings      | list of strings | A list of strings to be removed from the filename during parse. | []                |
| keep_delimiters      | boolean         | If the delimiters should be kept or not in anime/episode title. | False             |
| max_extension_length | integer         | Maximum extension length.                                       | 4                 |
| title_before_episode | boolean         | If the anime title should be before the episode number or not.  | True              |

## License
*Aniparse* is licensed under [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/FAQ/).