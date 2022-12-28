import os

from aniparse import KeywordManager, ElementCategory
from aniparse.keyword import KeywordOption
from aniparse.parser import Parser
from tests.fixtures.table import table

default_options = {
    'allowed_delimiters': ' _.&+,|',
    'check_title_enclosed': True,
    'eps_lower_than_alt': True,
    'ignored_dash': True,
    'ignored_strings': [],
    'keep_delimiters': False,
    'max_extension_length': 4,
    'title_before_episode': True,
    'valid_video_formats': ['3GP', 'AVI', 'DIVX', 'FLV', 'M2TS', 'MKV', 'MOV',
                            'MP4', 'MPG', 'OGM', 'RM', 'RMVB', 'TS', 'WEBM',
                            'WMV']

}

keyword_manager = KeywordManager(default_options['allowed_delimiters'])
keyword_option_default = KeywordOption()
keyword_manager.add(ElementCategory.EPISODE_PREFIX, keyword_option_default, [
    "#", "e",
    'EP', 'EP.', 'EPS', 'EPS.', 'EPISODE', 'EPISODE.', 'EPISODES',
    'CAPITULO', 'EPISODIO', 'FOLGE'
])
keyword_manager.add(ElementCategory.ANIME_SEASON_PREFIX, keyword_option_default, [
    'SAISON', 'SEASON', "s"])
keyword_manager.add(ElementCategory.ANIME_TYPE, keyword_option_default, [
    "ova", "oav", "oad", "ona", "specials", "tv", "sp", "special", "movie", "Gekijouban"
])
keyword_manager.add(ElementCategory.BONUS_TYPE, keyword_option_default, [
    'ED', 'ENDING', 'NCED', "CLEAN ENDING",
    'NCOP', 'OP', 'OPENING', "CLEAN OPENING",
    'PREVIEW', 'PV'
])

keyword_manager.add(ElementCategory.AUDIO_TERM, keyword_option_default, [
    # Audio channels
    '2.0CH', '2CH', '5.1', '5.1CH', 'DTS', 'DTS-ES', 'DTS5.1',
    'TRUEHD5.1',
    # Audio codec
    'AAC', 'AACX2', 'AACX3', 'AACX4', 'AC3', 'EAC3', 'E-AC-3',
    'FLAC', 'FLACX2', 'FLACX3', 'FLACX4', 'LOSSLESS', 'MP3', 'OGG',
    'VORBIS',
    # Audio language
    'DUALAUDIO', 'DUAL AUDIO', 'DUAL-AUDIO',
    'MULTIAUDIO', 'MULTI AUDIO', 'MULTI-AUDIO'
])

keyword_manager.add(ElementCategory.DEVICE_COMPATIBILITY, keyword_option_default, [
    'IPAD3', 'IPHONE5', 'IPOD', 'PS3', 'XBOX', 'XBOX360'])

keyword_manager.add(ElementCategory.LANGUAGE, keyword_option_default, [
    'ENG', 'ENGLISH', 'ESPANOL', 'JAP', 'PT-BR', 'SPANISH', 'VOSTFR', "ESP", "ITA"
])

keyword_manager.add(ElementCategory.OTHER, keyword_option_default, [
    'REMASTER', 'REMASTERED', 'UNCENSORED', 'UNCUT',
    'TS', 'VFR', 'WIDESCREEN', 'WS'
])
keyword_manager.add(ElementCategory.RELEASE_INFORMATION, keyword_option_default, [
    'BATCH', 'COMPLETE', 'PATCH', 'REMUX', 'END', 'FINAL'
])
keyword_manager.add(ElementCategory.SOURCE, keyword_option_default, [
    'BD', 'BDRIP', 'BLURAY', 'BLU-RAY',
    'DVD', 'DVD5', 'DVD9', 'DVD-R2J', 'DVDRIP', 'DVD-RIP',
    'R2DVD', 'R2J', 'R2JDVD', 'R2JDVDRIP',
    'HDTV', 'HDTVRIP', 'TVRIP', 'TV-RIP',
    'WEBCAST', 'WEBRIP'
])
keyword_manager.add(ElementCategory.VOLUME_PREFIX, keyword_option_default, [
    "Vol", "vol.", "VOLUME"])
keyword_manager.add(ElementCategory.SUBTITLES, keyword_option_default, [
    'ASS', 'BIG5', 'DUB', 'DUBBED', 'HARDSUB', 'HARDSUBS', 'RAW',
    'SOFTSUB', 'SOFTSUBS', 'SUB', 'SUBBED', 'SUBTITLED',
    'MULTI SUBS', 'MULTI-SUBS', 'MULTISUB', 'MULTISUBS'
])

keyword_manager.add(ElementCategory.VIDEO_TERM, keyword_option_default, [
    # Frame rate
    '23.976FPS', '24FPS', '29.97FPS', '30FPS', '60FPS', '120FPS',
    # Video codec
    '8BIT', '8-BIT', '10BIT', '10BITS', '10-BIT', '10-BITS',
    'HI10', 'HI10P', 'HI444', 'HI444P', 'HI444PP',
    'H264', 'H265', 'H.264', 'H.265', 'X264', 'X265', 'X.264',
    'AVC', 'HEVC', 'HEVC2', 'DIVX', 'DIVX5', 'DIVX6', 'XVID',
    # Video format
    'AVI', 'RMVB', 'WMV', 'WMV3', 'WMV9',
    # Video quality
    'HQ', 'LQ',
    # Video resolution
    'HD', 'SD'
])
for idx, item in enumerate(table):
    filename = item["file_name"].strip(".mkv").strip(".mp4").strip(".avi").strip("7z")
    if filename in ["Aim_For_The_Top!_Gunbuster-ep1.BD(H264.FLAC.10bit)[KAA][69ECCDCF]",
                    "Toradora! asdwd-03-Your-Song",
                    "Toradora-E03-Your-Song",
                    "Toradora! S01E03-Your Song",
                    "[ANE] Yosuga no Sora - Ep01 Preview (Yorihime ver) [BDRip 1080p x264 FLAC]",
                    "[B-G_&_m.3.3.w]_Myself_Yourself_12.DVD(H.264_DD2.0)_[CB2B37F1]",
                    "[BakaWolf-m.3.3.w] Special A 01 (H.264) [C83164B9]",
                    "[E-HARO Raws] Kore wa Zombie desu ka - 03 (TV 1280x720 h264 AAC) [888E4991]",
                    "[EMBER] Natsu no Arashi! - S01E01-Playback Part 2 [BD00F464]",
                    "Cyborg 009 (1968) [TSHS] [30C15D62]",
                    "[FB] Crayon Shin-Chan Movie 2 The Secret of Buri Buri Kingdom [DivX5 AC3] 1994 [852X480] V2",
                    "[FFF] Love Live! The School Idol Movie - PV [D1A15D2C]",
                    "[Judas] Card Captor Sakura - The Movie 2 - The Sealed Card",
                    "[BM&T] Toradora! - 07v2 - Pool Opening [720p Hi10 ] [BD] [8F59F2BA]",
                    "[Triad]_Today_in_Class_5-2_-_04",
                    "[Yoroshiku]_009-1_-_02_(H264)_[36D2444D]",
                    "[zza] Nanatsu no Taizai - S03 - Kamigami no Gekirin - 21 [1080p.x265]",
                    "[a4e]R.O.D_the_TV_01[divx5.2.1]"]:
        print("Skipped", filename)
        continue
    print(f"Parsing {idx}/{len(table)}", filename)
    if filename in ["Evangelion The New Movie Q (BD 1280x720 AVC AACx2 [5.1+2.0])"]:
        print("Found", filename)
    x = Parser(filename, default_options, keyword_manager)
    x.parse()
    categories = {}

    convert_to_float = [ElementCategory.EPISODE_NUMBER,
                        ElementCategory.EPISODE_TOTAL,
                        ElementCategory.ANIME_SEASON,
                        ElementCategory.RELEASE_VERSION,
                        ElementCategory.VOLUME_NUMBER,
                        ElementCategory.ANIME_YEAR,
                        ElementCategory.BONUS_NUMBER]

    compare_categories = [
        ElementCategory.ANIME_SEASON,
        ElementCategory.ANIME_SEASON_PREFIX,
        # ElementCategory.ANIME_TITLE,
        # ElementCategory.ANIME_TITLE_ALT,
        ElementCategory.ANIME_TYPE,
        ElementCategory.ANIME_YEAR,
        ElementCategory.AUDIO_TERM,
        ElementCategory.BONUS_TYPE,
        ElementCategory.BONUS_NUMBER,
        ElementCategory.BONUS_PART,
        ElementCategory.DEVICE_COMPATIBILITY,
        # ElementCategory.BRACKET,
        # ElementCategory.DELIMITER,
        ElementCategory.EPISODE_NUMBER,
        ElementCategory.EPISODE_PART,
        ElementCategory.EPISODE_NUMBER_ALT,
        ElementCategory.EPISODE_PREFIX,
        # ElementCategory.EPISODE_TITLE,
        ElementCategory.EPISODE_TOTAL,
        ElementCategory.FILE_CHECKSUM,
        # ElementCategory.FILE_EXTENSION,
        # ElementCategory.FILE_NAME,
        ElementCategory.LANGUAGE,
        # ElementCategory.OTHER,
        # ElementCategory.RANGE_SEPARATOR,
        # ElementCategory.RELEASE_GROUP,
        ElementCategory.RELEASE_INFORMATION,
        ElementCategory.RELEASE_VERSION,
        # ElementCategory.UNKNOWN,
        # ElementCategory.RELEASE_VERSION_PREFIX,
        ElementCategory.SOURCE,
        ElementCategory.SUBTITLES,
        ElementCategory.VIDEO_RESOLUTION,
        ElementCategory.VIDEO_TERM,
        ElementCategory.VOLUME_NUMBER,
        ElementCategory.VOLUME_PREFIX,
    ]

    for token in x.tokens.loop_forward():
        if token.category not in categories:
            categories[token.category] = []
        if token.category in convert_to_float:
            token.content = float(token.content)
        if token.content in categories[token.category]:
            continue
        categories[token.category].append(token.content)
        categories[token.category].sort()

    expected_categories = {}
    for category, content in item.items():
        cat = ElementCategory(category)
        if cat == ElementCategory.EPISODE_NUMBER_ALT:
            cat = ElementCategory.EPISODE_NUMBER
        if cat not in expected_categories:
            expected_categories[cat] = []

        if cat in convert_to_float:
            if isinstance(content, list):
                new_content = []
                for number in content:
                    if number in expected_categories[cat] + new_content:
                        continue
                    new_content.append(float(number))
                content = new_content
            else:
                if content in expected_categories[cat]:
                    continue
                content = float(content)
        if isinstance(content, list):
            expected_categories[cat].extend(content)
        else:
            expected_categories[cat].append(content)
        expected_categories[cat].sort()

    for verified in compare_categories:
        if categories.get(verified) != expected_categories.get(verified):
            list_of_tokens = []
            for token in x.tokens.loop_forward():
                list_of_tokens.append(token.content)
                # list_of_tokens.append((token.category, token.content))
            print(list_of_tokens)
            print(f"Error: {filename}")
            print(
                f"The {verified.value} should be {expected_categories.get(verified)} but is {categories.get(verified)}")
            break
    else:
        continue
    break
