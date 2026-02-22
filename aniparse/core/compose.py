"""Assemble resolved tokens into a Metadata output object."""
from __future__ import annotations

import os
import re
from typing import Optional

from aniparse.config import ParserConfig
from aniparse.core import constant
from aniparse.rule.possibilities.number_rule import get_number_from_ordinal
from aniparse.core.token import Tokens, Token
from aniparse.core.token_tags import Tag
from aniparse.core.rhythm import DelimiterProfile
from aniparse.output_schemas import (
    Metadata, SeriesInfo, VideoResolution, SequenceNumber,
    SequenceIdentifierNumber, SequenceRange,
)


def compose(tokens: Tokens, filename: str, delimiter_profile: DelimiterProfile = None, config: ParserConfig = None) -> Metadata:
    """Assemble resolved tokens into a Metadata object."""
    # --- Collect raw values into plain lists/vars ---
    title_tokens: list[Token] = []
    checksum_tokens: list[Token] = []
    season_numbers: list[dict] = []
    season_tokens: list[Token] = []
    episode_numbers: list[dict] = []
    episode_tokens: list[Token] = []
    volume_numbers: list[dict] = []
    volume_tokens: list[Token] = []
    content_type_entries: list[dict] = []
    series_type: Optional[str] = None
    episode_title_tokens: list[Token] = []
    unknown_tokens: list[str] = []
    release_information: list[str] = []
    release_version: list[str] = []
    subs_term: list[str] = []
    language: list[str] = []
    device_compatibility: list[str] = []
    other: list[str] = []
    sequence_prefix_context: Optional[Tag] = None
    last_content_type_identifier: Optional[str] = None
    last_number_target: Optional[Tag] = None
    file_index: Optional[int] = None
    alt_series_list: list[dict] = []

    token_list = list(tokens)
    in_bracket = False
    skip_next_prefix = False
    consumed_tokens: set[int] = set()

    for i, token in enumerate(token_list):
        if id(token) in consumed_tokens:
            continue
        label = token.category
        poss = token.possibilities.get(label)
        descriptor = poss.descriptor if poss else None

        if label == Tag.BRACKET:
            if token.content in constant.OPEN_BRACKETS:
                in_bracket = True
            elif token.content in constant.CLOSE_BRACKETS:
                in_bracket = False
            continue

        if label == Tag.TITLE:
            if descriptor == Tag.SEQUENCE_TITLE:
                episode_title_tokens.append(token)
            else:
                title_tokens.append(token)

        elif label == Tag.TYPE:
            type_val = _normalize_type(token)
            if in_bracket:
                # Bracketed TYPE (e.g., "(TV)") → series type qualifier
                if not series_type:
                    series_type = type_val
            else:
                # Freestanding TYPE (e.g., "OVA" after brackets) → could be content_type
                if series_type:
                    # Already have a series type — this is content type
                    sequence_prefix_context = Tag.CONTENT_TYPE
                    last_content_type_identifier = type_val
                else:
                    series_type = type_val

        elif label == Tag.SEQUENCE_PREFIX:
            if skip_next_prefix:
                skip_next_prefix = False
                continue
            if descriptor in (Tag.SEASON,):
                sequence_prefix_context = Tag.SEASON
            elif descriptor in (Tag.EPISODE,):
                sequence_prefix_context = Tag.EPISODE
            elif descriptor in (Tag.VOLUME,):
                sequence_prefix_context = Tag.VOLUME
            elif descriptor in (Tag.CONTENT_TYPE, Tag.CONTENT_IDENTIFIER):
                if sequence_prefix_context == Tag.CONTENT_TYPE and last_content_type_identifier:
                    last_content_type_identifier = last_content_type_identifier.strip() + constant.SPACE + token.content
                else:
                    sequence_prefix_context = Tag.CONTENT_TYPE
                    last_content_type_identifier = token.content
            else:
                sequence_prefix_context = Tag.EPISODE

        elif label == Tag.SEQUENCE_NUMBER:
            num = _try_int(token.content)
            # For ordinals (e.g. "2nd"), extract the number part via config
            if num is None and config:
                ordinal_val = get_number_from_ordinal(token.content, config)
                if ordinal_val.isdigit():
                    num = int(ordinal_val)
                # Look ahead for SEQUENCE_PREFIX to set context
                for j in range(i + 1, len(token_list)):
                    ft = token_list[j]
                    if ft.category == Tag.DELIMITER:
                        continue
                    if ft.category == Tag.SEQUENCE_PREFIX:
                        fp = ft.possibilities.get(ft.category)
                        fd = fp.descriptor if fp else None
                        if fd in (Tag.SEASON,):
                            sequence_prefix_context = Tag.SEASON
                        elif fd in (Tag.VOLUME,):
                            sequence_prefix_context = Tag.VOLUME
                        else:
                            sequence_prefix_context = Tag.EPISODE
                        skip_next_prefix = True
                    break
            entry: dict[str, object] = {"number": num if num is not None else token.content}

            # Token's own descriptor overrides prefix context (e.g. SxEE marks first number as SEASON)
            num_poss = token.possibilities.get(Tag.SEQUENCE_NUMBER)
            num_descriptor = num_poss.descriptor if num_poss else None
            if num_descriptor == Tag.SEASON or sequence_prefix_context == Tag.SEASON:
                season_numbers.append(entry)
                season_tokens.append(token)
                last_number_target = Tag.SEASON
            elif sequence_prefix_context == Tag.VOLUME:
                volume_numbers.append(entry)
                volume_tokens.append(token)
                last_number_target = Tag.VOLUME
            elif sequence_prefix_context == Tag.CONTENT_TYPE:
                ct_entry: dict[str, object] = {"number": num if num is not None else token.content}
                if last_content_type_identifier:
                    ct_entry["identifier"] = last_content_type_identifier
                content_type_entries.append(ct_entry)
                last_content_type_identifier = None
                last_number_target = Tag.CONTENT_TYPE
            else:
                # Check if this is an alternative episode (bracketed number when episode already exists
                # from OUTSIDE this bracket group)
                if in_bracket and episode_numbers and _has_episode_outside_bracket(token_list, i, episode_tokens):
                    # Check if bracket also has unknown text (= alternative series title)
                    alt_title = _get_bracket_unknown_text(token_list, i)
                    if alt_title:
                        # This is an alternative series, not just an alternative episode
                        alt_series_list.append({"title": alt_title, "episode": [entry]})
                        last_number_target = Tag.EPISODE
                        sequence_prefix_context = None
                        continue
                    if "alternative" not in episode_numbers[-1]:
                        episode_numbers[-1]["alternative"] = []
                    episode_numbers[-1]["alternative"].append(entry)
                    last_number_target = Tag.EPISODE
                    sequence_prefix_context = None
                    continue
                episode_numbers.append(entry)
                episode_tokens.append(token)
                last_number_target = Tag.EPISODE
            # Keep context if next token is a connector (&, +)
            next_meaningful = _next_non_delimiter(token_list, i)
            if next_meaningful and (next_meaningful.content in config.range_connectors
                                    or next_meaningful.category == Tag.SEQUENCE_RANGE):
                pass  # keep sequence_prefix_context for the next number
            else:
                sequence_prefix_context = None

        elif label == Tag.SEQUENCE_PART:
            if not (len(token.content) > 1 and token.content.isalpha()):
                # Direct part value (digit/letter from glued forms) — attach to most recent entry
                if last_number_target == Tag.CONTENT_TYPE and content_type_entries:
                    content_type_entries[-1]["part"] = token.content
                elif episode_numbers:
                    episode_numbers[-1]["part"] = token.content
            elif in_bracket and episode_numbers:
                # "Part" word followed by a number → attach to last episode/alternative
                next_tok = _next_non_delimiter(token_list, i)
                if next_tok and next_tok.content.isdigit():
                    last_ep = episode_numbers[-1]
                    alts = last_ep.get("alternative", [])
                    if alts:
                        alts[-1]["part"] = next_tok.content
                    else:
                        last_ep["part"] = next_tok.content
                    consumed_tokens.add(id(next_tok))

        elif label == Tag.RELEASE_VERSION:
            # Named version marker (e.g., "yorihime ver") — use preceding unknown as version value
            ver_value = token.content
            if not token.content[0].isdigit():
                prev_unknown = None
                for j in range(i - 1, -1, -1):
                    pt = token_list[j]
                    if pt.category in (Tag.DELIMITER, Tag.CONTEXT_DELIMITER):
                        continue
                    if pt.category == Tag.UNKNOWN and not pt.possibilities:
                        prev_unknown = pt
                    break
                if prev_unknown:
                    ver_value = prev_unknown.content
                    # Remove from unknown_tokens since it's now a version name
                    if prev_unknown.content in unknown_tokens:
                        unknown_tokens.remove(prev_unknown.content)
            release_version.append(ver_value)
            if last_number_target == Tag.CONTENT_TYPE and content_type_entries:
                content_type_entries[-1]["release_version"] = ver_value
            elif sequence_prefix_context == Tag.CONTENT_TYPE and last_content_type_identifier:
                # Pending content_type without number (e.g., "EDv2")
                content_type_entries.append({
                    "identifier": last_content_type_identifier,
                    "release_version": ver_value,
                })
                last_content_type_identifier = None
                sequence_prefix_context = None
            elif last_number_target == Tag.VOLUME and volume_numbers:
                volume_numbers[-1]["release_version"] = ver_value
            elif episode_numbers:
                episode_numbers[-1]["release_version"] = ver_value

        elif label == Tag.FILE_CHECKSUM:
            checksum_tokens.append(token)

        elif label == Tag.FILE_INDEX:
            idx = _try_int(token.content)
            file_index = idx if idx is not None else token.content

        elif label == Tag.RELEASE_INFORMATION:
            release_information.append(token.content)

        elif label == Tag.DEVICE_COMPATIBILITY:
            device_compatibility.append(token.content)

        elif label == Tag.EXTRA_INFO:
            other.append(token.content)

        elif label == Tag.UNKNOWN:
            if token.content.strip():
                unknown_tokens.append(token.content)

    if last_content_type_identifier and sequence_prefix_context == Tag.CONTENT_TYPE:
        content_type_entries.append({"identifier": last_content_type_identifier})

    episode_numbers = _merge_decimals(episode_numbers, token_list)
    episode_numbers = _detect_ranges(episode_numbers, token_list, episode_tokens, config)
    episode_numbers = _lift_alternatives_to_range(episode_numbers, token_list)
    episode_numbers = _dedup_episodes(episode_numbers)

    season_numbers = _dedup_episodes(season_numbers)  # reuse for season dedup
    season_numbers = _detect_ranges(season_numbers, token_list, season_tokens, config)

    volume_numbers = _detect_ranges(volume_numbers, token_list, volume_tokens, config)

    if release_version and episode_numbers:
        last_ep = episode_numbers[-1]
        if isinstance(last_ep, dict) and "start" not in last_ep:
            last_ep["release_version"] = release_version[0] if len(release_version) == 1 else (constant.COMMA + constant.SPACE).join(release_version)
        elif isinstance(last_ep, dict) and "end" in last_ep:
            last_ep["end"]["release_version"] = release_version[0] if len(release_version) == 1 else (constant.COMMA + constant.SPACE).join(release_version)

    # --- Grouped label merging ---
    audio_term: list[str] = []
    video_term: list[str] = []
    source: list[str] = []
    for label_key, target in [
        (Tag.AUDIO_TERM, audio_term),
        (Tag.VIDEO_TERM, video_term),
        (Tag.SOURCE, source),
        (Tag.SUBS_TERM, subs_term),
        (Tag.LANGUAGE, language),
    ]:
        groups = _group_adjacent_by_label(tokens, label_key)
        if groups:
            target.extend(_merge_adjacent_tokens(g, delimiter_profile) for g in groups)

    if audio_term:
        audio_term = _normalize_audio_terms(audio_term)

    if subs_term:
        subs_term = _normalize_subs_terms(subs_term)

    # Filter CJK-only language entries (redundant with English equivalents)
    if language:
        language = [l for l in language if re.search(r'[a-zA-Z]', l)]
        # Deduplicate (case-insensitive, preserve first occurrence)
        seen_lang = set()
        deduped = []
        for l in language:
            key = l.lower()
            if key not in seen_lang:
                seen_lang.add(key)
                deduped.append(l)
        language = deduped

    video_resolution_dicts = _build_video_resolutions(tokens)

    release_group: list[str] = []
    rg_groups = _group_adjacent_by_label(tokens, Tag.RELEASE_GROUP)
    if rg_groups:
        for g in rg_groups:
            # Split token group on & separators
            subgroups = _split_release_group_on_ampersand(g)
            keep_us = len(subgroups) > 1  # keep underscores when & split
            for sg in subgroups:
                merged = _merge_release_group_tokens(sg, keep_underscores=keep_us)
                if merged.strip():
                    release_group.append(merged.strip())

    file_checksum: Optional[str] = None
    if checksum_tokens:
        file_checksum = "".join(t.content for t in checksum_tokens)

    # --- Build SeriesInfo ---
    series_info_dict: dict = {}

    if title_tokens:
        merged_title = _merge_title_tokens(title_tokens, delimiter_profile=delimiter_profile).strip()
        # Append trailing period if glued to last title token and followed by
        # context delimiter (e.g., "yatte mita. - 01"), but not when period is
        # the primary delimiter (dot-separated filenames like "dragon.ball.kai.-.01")
        if not (delimiter_profile and delimiter_profile.primary == constant.DOT):
            last_tt = title_tokens[-1]
            trailing_idx = last_tt.index + len(last_tt.content)
            for t in token_list:
                if t.index == trailing_idx and t.content == constant.DOT and t.category == Tag.DELIMITER:
                    # Only if next non-space token is context delimiter or bracket
                    for t2 in token_list:
                        if t2.index <= t.index:
                            continue
                        if t2.category == Tag.DELIMITER and t2.content.strip() == "":
                            continue
                        if t2.category in (Tag.CONTEXT_DELIMITER, Tag.BRACKET):
                            merged_title += constant.DOT
                        break
                    break
        series_info_dict["title"] = merged_title

    if episode_numbers and title_tokens:
        episode_numbers, _ = _absorb_glued_episodes_into_title(
            title_tokens, episode_numbers, token_list, series_info_dict, delimiter_profile
        )

    if series_type:
        series_info_dict["type"] = series_type

    year_entries: list[dict] = []
    year_tokens: list[Token] = []
    for token in tokens:
        if token.category == Tag.YEAR:
            num = _try_int(token.content)
            if num is not None:
                year_entries.append({"number": num})
                year_tokens.append(token)
    year_entries = _detect_ranges(year_entries, token_list, year_tokens, config)
    if year_entries:
        series_info_dict["year"] = year_entries

    if season_numbers:
        series_info_dict["season"] = season_numbers
    if episode_numbers:
        series_info_dict["episode"] = episode_numbers
    if volume_numbers:
        series_info_dict["volume"] = volume_numbers
    if content_type_entries:
        series_info_dict["content_type"] = content_type_entries

    if episode_title_tokens:
        # Check if these tokens are between season and episode (→ season title)
        is_season_title = False
        if season_tokens and episode_tokens:
            last_season_idx = season_tokens[-1].index
            first_ep_idx = episode_tokens[0].index
            ep_title_indices = [t.index for t in episode_title_tokens
                                if Tag.DELIMITER not in t.possibilities
                                and Tag.CONTEXT_DELIMITER not in t.possibilities]
            if ep_title_indices and last_season_idx < ep_title_indices[0] < first_ep_idx:
                is_season_title = True
                # Exclude the episode number from title tokens
                episode_title_tokens = [t for t in episode_title_tokens
                                        if Tag.SEQUENCE_NUMBER not in t.possibilities]

        ep_title = _merge_title_tokens(episode_title_tokens, replace_dashes=True, delimiter_profile=delimiter_profile).strip()
        # Normalize doubled single-quotes to single quotes (e.g., ''word'' → 'word')
        ep_title = ep_title.replace(constant.APOSTROPHE * 2, constant.APOSTROPHE)
        # Append trailing period if glued to last episode title token
        if episode_title_tokens:
            last_ett = episode_title_tokens[-1]
            ett_trailing_idx = last_ett.index + len(last_ett.content)
            for t in token_list:
                if t.index == ett_trailing_idx and t.content == constant.DOT and t.category == Tag.DELIMITER:
                    for t2 in token_list:
                        if t2.index <= t.index:
                            continue
                        if t2.category == Tag.DELIMITER and t2.content.strip() == "":
                            continue
                        if t2.category in (Tag.CONTEXT_DELIMITER, Tag.BRACKET):
                            ep_title += constant.DOT
                        break
                    break
        if ep_title:
            if is_season_title:
                series_info_dict["season"][-1]["title"] = ep_title
            elif "episode" in series_info_dict and series_info_dict["episode"]:
                last_ep = series_info_dict["episode"][-1]
                if isinstance(last_ep, dict):
                    last_ep["title"] = ep_title
            elif "content_type" in series_info_dict and series_info_dict["content_type"]:
                series_info_dict["content_type"][-1]["title"] = ep_title
            elif "volume" in series_info_dict and series_info_dict["volume"]:
                series_info_dict["volume"][-1]["title"] = ep_title

    # --- Expand +separated bracket components into multiple series ---
    expanded = _expand_plus_separated_series(
        series_info_dict, season_numbers, token_list, tokens, config)
    if expanded:
        series_info_dict = expanded[0]  # base series (may be trimmed)
        extra_series = expanded[1:]
    else:
        extra_series = []

    # --- Convert intermediate dicts to dataclass instances ---
    series_list: list[SeriesInfo] = []
    if series_info_dict:
        series_list = [_dict_to_series_info(series_info_dict)]
    for es in extra_series:
        series_list.append(_dict_to_series_info(es))
    for alt in alt_series_list:
        series_list.append(_dict_to_series_info(alt))

    video_res_list: list[VideoResolution] = []
    if video_resolution_dicts:
        video_res_list = [VideoResolution(**d) for d in video_resolution_dicts]

    from aniparse.core.constant import FILE_EXTENSIONS
    name, ext = os.path.splitext(filename)
    ext_val = ext.lstrip(constant.DOT).lower() if ext else ""
    if ext_val not in FILE_EXTENSIONS:
        ext_val = ""

    # Filter file extension from release_group
    if ext_val and release_group:
        release_group = [rg for rg in release_group if rg.lower() != ext_val]
        if not release_group:
            release_group = []

    return Metadata(
        file_name=filename,
        file_extension=ext_val or None,
        file_checksum=file_checksum,
        file_index=file_index,
        audio_term=audio_term or None,
        device_compatibility=device_compatibility or None,
        language=language or None,
        video_resolution=video_res_list or None,
        release_version=release_version or None,
        release_group=release_group or None,
        release_information=release_information or None,
        series=series_list or None,
        source=source or None,
        subs_term=subs_term or None,
        video_term=video_term or None,
        other=other or None,
        unknown=_group_unknown_tokens(tokens, unknown_tokens, delimiter_profile) or None,
    )


def _expand_plus_separated_series(series_info, season_numbers, token_list, tokens, config: ParserConfig = None):
    """Expand bracket groups like (S01+S02+...+Movies+OVAs) into multiple series.

    Returns list of series dicts if expansion happened, else None.
    """
    if not series_info or not series_info.get("title"):
        return None

    # Find a bracket group containing + separated items mixing seasons and types
    bracket_groups = _find_plus_bracket_groups(token_list, config)
    if not bracket_groups:
        return None

    for components in bracket_groups:
        season_comps = [c for c in components if c["kind"] == Tag.SEASON]
        type_or_text = [c for c in components if c["kind"] in (Tag.TYPE, Tag.TITLE)]
        # Only expand when we have multiple individual seasons AND type/text entries
        # (batch pattern like S01+S02+S03+S04+Movies+OVAs)
        # Skip when there's a season range (Season 1-4 + OVA) — that's one series
        if len(season_comps) < 2 or not type_or_text:
            continue

        # Expand: each component becomes a separate series
        title = series_info.get("title", "")
        result = []
        for comp in components:
            entry = {"title": title}
            if comp["kind"] == Tag.SEASON:
                entry["season"] = [{"number": comp["number"]}]
            elif comp["kind"] == Tag.TYPE:
                entry["type"] = comp["value"]
            elif comp["kind"] == Tag.TITLE:
                entry["title"] = title + constant.SPACE + comp["value"]
            result.append(entry)

        return result

    return None


def _find_plus_bracket_groups(token_list, config: ParserConfig = None):
    """Find bracket groups containing +-separated items."""
    results = []
    i = 0
    while i < len(token_list):
        token = token_list[i]
        if token.category == Tag.BRACKET and token.content in constant.OPEN_BRACKETS:
            # Collect tokens inside bracket
            inside = []
            j = i + 1
            while j < len(token_list):
                t = token_list[j]
                if t.category == Tag.BRACKET and t.content in constant.CLOSE_BRACKETS:
                    break
                inside.append(t)
                j += 1

            # Check if this bracket has + separators
            connectors = config.range_connectors if config else ()
            plus_count = sum(1 for t in inside if t.content in connectors)
            if plus_count >= 2:
                # Split on connectors into components
                components = []
                current = []
                for t in inside:
                    if t.content in connectors:
                        comp = _classify_component(current)
                        if comp:
                            components.append(comp)
                        current = []
                    else:
                        current.append(t)
                comp = _classify_component(current)
                if comp:
                    components.append(comp)
                if len(components) >= 3:
                    results.append(components)
            i = j + 1
        else:
            i += 1
    return results


def _classify_component(tokens):
    """Classify a +-separated component as season, type, or text."""
    meaningful = [t for t in tokens
                  if t.category not in (Tag.DELIMITER, Tag.CONTEXT_DELIMITER)]
    if not meaningful:
        return None

    # Season: SEQUENCE_PREFIX(season) + SEQUENCE_NUMBER
    if (len(meaningful) >= 2
            and meaningful[0].category == Tag.SEQUENCE_PREFIX
            and meaningful[1].category == Tag.SEQUENCE_NUMBER):
        poss = meaningful[0].possibilities.get(Tag.SEQUENCE_PREFIX)
        if poss and poss.descriptor == Tag.SEASON:
            num = _try_int(meaningful[1].content)
            return {"kind": Tag.SEASON, "number": num if num is not None else meaningful[1].content}

    # Type: TYPE token (possibly followed by plural 's')
    if meaningful[0].category == Tag.TYPE:
        # Reconstruct the full type name (e.g., "OVA" + "s" → "OVAs")
        type_val = "".join(t.content for t in meaningful)
        return {"kind": Tag.TYPE, "value": type_val}

    # Text: unknown tokens (like "Alternative")
    text_parts = [t.content for t in meaningful if not t.possibilities or t.category == Tag.UNKNOWN]
    if text_parts:
        return {"kind": Tag.TITLE, "value": constant.SPACE.join(text_parts)}

    return None


def _dict_to_series_info(d: dict) -> SeriesInfo:
    """Convert an intermediate series info dict to a SeriesInfo dataclass."""
    return SeriesInfo(
        title=d.get("title"),
        type=d.get("type"),
        year=_convert_sequence_list(d.get("year")),
        season=_convert_sequence_list(d.get("season")),
        episode=_convert_sequence_list(d.get("episode")),
        volume=_convert_sequence_list(d.get("volume")),
        content_type=_convert_sequence_list(d.get("content_type"), identifier=True),
    )


def _convert_sequence_list(entries: list[dict] | None, identifier: bool = False):
    """Convert a list of intermediate dicts to SequenceNumber/Range instances."""
    if not entries:
        return None
    result = []
    for entry in entries:
        if "start" in entry and "end" in entry:
            alt_dicts = entry.get("alternative", [])
            alt_ranges = _convert_sequence_list(alt_dicts, identifier) if alt_dicts else []
            result.append(SequenceRange(
                start=_dict_to_sequence(entry["start"], identifier),
                end=_dict_to_sequence(entry["end"], identifier),
                alternative=alt_ranges,
            ))
        else:
            result.append(_dict_to_sequence(entry, identifier))
    return result


def _dict_to_sequence(d: dict, identifier: bool = False):
    """Convert a single intermediate dict to a SequenceNumber or SequenceIdentifierNumber."""
    if identifier or "identifier" in d:
        return SequenceIdentifierNumber(
            number=d.get("number"),
            identifier=d.get("identifier"),
            total=d.get("total"),
            release_version=d.get("release_version"),
            title=d.get("title"),
            part=d.get("part"),
        )
    alt = d.get("alternative")
    alt_list = [_dict_to_sequence(a, identifier) for a in alt] if alt else []
    return SequenceNumber(
        number=d["number"],
        total=d.get("total"),
        release_version=d.get("release_version"),
        title=d.get("title"),
        part=d.get("part"),
        alternative=alt_list,
    )

def _absorb_glued_episodes_into_title(title_tokens, episode_numbers, token_list, series_info,
                                      delimiter_profile=None):
    last_title = title_tokens[-1]
    last_title_end = last_title.index + len(last_title.content)

    seq_tokens = [t for t in token_list if t.category == Tag.SEQUENCE_NUMBER]
    if not seq_tokens:
        return episode_numbers, 0

    first_ep_token = seq_tokens[0]
    between_start = last_title_end
    between_end = first_ep_token.index

    if between_end - between_start != 1:
        return episode_numbers, 0

    glue_token = None
    for t in token_list:
        if t.index == between_start and Tag.DELIMITER in t.possibilities:
            glue_token = t
            break

    if not glue_token:
        return episode_numbers, 0

    # Don't absorb when the glue delimiter is also the primary delimiter (structural separator)
    if delimiter_profile and glue_token.content == delimiter_profile.primary:
        return episode_numbers, 0

    old_title = series_info.get("title", "")
    series_info["title"] = f"{old_title}{glue_token.content}{first_ep_token.content}"
    return episode_numbers[1:], 1


def _detect_ranges(entries: list, token_list: list, entry_tokens: list[Token] | None = None, config: ParserConfig = None) -> list:
    if len(entries) < 2:
        return entries

    if entry_tokens is None:
        # Fallback: assume seq_tokens are 1:1 with entries (legacy behavior)
        entry_tokens = [t for t in token_list if t.category == Tag.SEQUENCE_NUMBER]

    result = []
    skip_next = False
    for idx, entry in enumerate(entries):
        if skip_next:
            skip_next = False
            continue
        if idx + 1 < len(entries):
            if idx < len(entry_tokens) and idx + 1 < len(entry_tokens):
                t1 = entry_tokens[idx]
                t2 = entry_tokens[idx + 1]
                range_token = None
                t1_pos = token_list.index(t1)
                t2_pos = token_list.index(t2)
                for between_idx in range(t1_pos + 1, t2_pos):
                    bt = token_list[between_idx]
                    if bt.category == Tag.SEQUENCE_RANGE:
                        range_token = bt
                        break
                if range_token is not None:
                    start_num = entry.get("number")
                    end_num = entries[idx + 1].get("number")
                    if start_num is not None and end_num is not None and start_num <= end_num:
                        if range_token.content.lower() in config.range_total:
                            entry["total"] = end_num
                            result.append(entry)
                        elif range_token.content in config.range_connectors:
                            # + means separate entries, not a range
                            result.append(entry)
                            result.append(entries[idx + 1])
                        else:
                            result.append({
                                "start": entry,
                                "end": entries[idx + 1],
                            })
                        skip_next = True
                        continue
        result.append(entry)
    return result


def _merge_title_tokens(title_tokens: list[Token], replace_dashes: bool = False,
                        delimiter_profile: DelimiterProfile | None = None) -> str:
    if not title_tokens:
        return ""
    parts = []
    _glued_paren_depth = 0
    _stripped_open_bracket = None
    for i, token in enumerate(title_tokens):
        if i > 0:
            gap = token.index - (title_tokens[i - 1].index + len(title_tokens[i - 1].content))
            if gap > 0:
                parts.append(constant.SPACE)
            elif gap == 0:
                # Insert space between word and number when glued (e.g., "part1" → "part 1")
                prev_tok = title_tokens[i - 1]
                if (Tag.CONTENT_IDENTIFIER in prev_tok.possibilities and token.content[0:1].isdigit()):
                    parts.append(constant.SPACE)
        content = token.content
        resolved = token.category
        is_primary = delimiter_profile and content == delimiter_profile.primary

        has_delim_possibility = Tag.DELIMITER in token.possibilities
        # Brackets in title: square brackets kept as-is, parentheses removed
        # only when glued to non-delimiter text (e.g., "mezzo(dsa)" → "mezzo dsa")
        if Tag.BRACKET in token.possibilities and resolved == Tag.TITLE:
            if content in constant.OPEN_BRACKETS:
                # Check if glued to previous non-delimiter token → replace with space
                glued = False
                for k in range(i - 1, -1, -1):
                    pt = title_tokens[k]
                    if Tag.DELIMITER in pt.possibilities or Tag.CONTEXT_DELIMITER in pt.possibilities:
                        continue
                    if pt.index + len(pt.content) == token.index:
                        content = constant.SPACE
                        _glued_paren_depth += 1
                        glued = True
                    break
                if not glued and i == 0:
                    # Strip outer container bracket (first title token)
                    content = ""
                    _stripped_open_bracket = token.content
            elif content in constant.CLOSE_BRACKETS:
                if _glued_paren_depth > 0:
                    content = constant.SPACE
                    _glued_paren_depth -= 1
                elif (i == len(title_tokens) - 1
                      and _stripped_open_bracket
                      and constant.BRACKET_PAIRS.get(_stripped_open_bracket) == content):
                    # Strip matching outer close bracket
                    content = ""
        elif is_primary or content == constant.UNDERSCORE:
            content = constant.SPACE
        elif resolved == Tag.CONTEXT_DELIMITER and replace_dashes:
            content = constant.SPACE
        elif resolved == Tag.DELIMITER or (has_delim_possibility and resolved == Tag.TITLE):
            # Glued delimiters (e.g. "3.0") are kept as-is
            prev_glued = i > 0 and token.index == title_tokens[i - 1].index + len(title_tokens[i - 1].content)
            next_glued = i + 1 < len(title_tokens) and title_tokens[i + 1].index == token.index + 1
            if prev_glued and next_glued:
                pass
            else:
                content = constant.SPACE
        parts.append(content)
    result = constant.SPACE.join("".join(parts).split())
    return result

def _group_unknown_tokens(tokens: Tokens, raw_unknowns: list[str], delimiter_profile: DelimiterProfile = None) -> list[str]:
    """Group adjacent UNKNOWN tokens (across spaces/underscores only) into merged strings."""
    if not raw_unknowns:
        return []
    groups: list[list[Token]] = []
    current: list[Token] = []
    pending_delims: list[Token] = []
    for token in tokens:
        if token.category == Tag.UNKNOWN:
            if current:
                current.extend(pending_delims)
            current.append(token)
            pending_delims = []
        elif (token.category in (Tag.DELIMITER, Tag.CONTEXT_DELIMITER)
              and current and delimiter_profile and token.content == delimiter_profile.primary):
            pending_delims.append(token)
        else:
            pending_delims = []
            if current:
                groups.append(current)
                current = []
    if current:
        groups.append(current)
    result = []
    for g in groups:
        merged = _merge_adjacent_tokens(g, delimiter_profile).strip()
        if merged:
            result.append(merged)
    return result


def _group_adjacent_by_label(tokens: Tokens, label: Tag) -> list[list[Token]]:
    groups = []
    current = []
    saw_plain_delimiter = False
    for token in tokens:
        if token.category == label:
            if (saw_plain_delimiter or token.split_boundary) and current:
                groups.append(current)
                current = []
            current.append(token)
            saw_plain_delimiter = False
        elif token.category in (Tag.DELIMITER, Tag.CONTEXT_DELIMITER):
            # A delimiter that also has the target label is part of the keyword match
            if current and label not in token.possibilities:
                saw_plain_delimiter = True
        else:
            saw_plain_delimiter = False
            if current:
                groups.append(current)
                current = []
    if current:
        groups.append(current)
    return groups


def _merge_adjacent_tokens(tokens: list[Token], delimiter_profile: DelimiterProfile = None) -> str:
    if not tokens:
        return ""
    parts = []
    for i, token in enumerate(tokens):
        if i > 0:
            gap = token.index - (tokens[i - 1].index + len(tokens[i - 1].content))
            if gap > 0:
                parts.append(constant.SPACE)
        content = token.content
        if content == constant.UNDERSCORE:
            content = constant.SPACE
        parts.append(content)
    return "".join(parts)


def _split_release_group_on_ampersand(tokens: list[Token]) -> list[list[Token]]:
    """Split a release group token list on '&' separators (only when surrounded by delimiters)."""
    # Only split on & that has delimiter tokens on both sides (e.g., "_&_")
    split_indices = []
    for i, t in enumerate(tokens):
        if Tag.CONTEXT_DEPENDENT in t.possibilities:
            has_delim_before = i > 0 and Tag.DELIMITER in tokens[i - 1].possibilities
            has_delim_after = i + 1 < len(tokens) and Tag.DELIMITER in tokens[i + 1].possibilities
            if has_delim_before and has_delim_after:
                split_indices.append(i)

    if not split_indices:
        return [tokens]

    groups = []
    start = 0
    for si in split_indices:
        groups.append(tokens[start:si])
        start = si + 1
    groups.append(tokens[start:])

    # Trim leading/trailing delimiter tokens from each subgroup
    trimmed = []
    for g in groups:
        while g and Tag.DELIMITER in g[0].possibilities:
            g = g[1:]
        while g and Tag.DELIMITER in g[-1].possibilities:
            g = g[:-1]
        if g:
            trimmed.append(g)
    return trimmed if trimmed else [tokens]


def _merge_release_group_tokens(tokens: list[Token], keep_underscores: bool = False) -> str:
    if not tokens:
        return ""
    parts = []
    for i, token in enumerate(tokens):
        if i > 0:
            gap = token.index - (tokens[i - 1].index + len(tokens[i - 1].content))
            if gap > 0:
                parts.append(constant.SPACE)
        content = token.content
        if not keep_underscores:
            content = content.replace(constant.UNDERSCORE, constant.SPACE)
        parts.append(content)
    result = constant.SPACE.join("".join(parts).split())
    return result


def _merge_decimals(entries: list, token_list: list) -> list:
    if len(entries) < 2:
        return entries

    seq_tokens = [t for t in token_list if t.category == Tag.SEQUENCE_NUMBER]
    result = []
    skip_next = False
    for idx, entry in enumerate(entries):
        if skip_next:
            skip_next = False
            continue
        if idx + 1 < len(entries) and idx < len(seq_tokens) - 1:
            t1 = seq_tokens[idx]
            t2 = seq_tokens[idx + 1]
            t1_pos = token_list.index(t1)
            t2_pos = token_list.index(t2)
            if t2_pos - t1_pos == 2:
                between = token_list[t1_pos + 1]
                if between.content == constant.DOT and between.category == Tag.DELIMITER:
                    decimal_val = float(f"{t1.content}.{t2.content}")
                    result.append({"number": decimal_val})
                    skip_next = True
                    continue
        result.append(entry)
    return result


def _lift_alternatives_to_range(entries: list[dict], token_list: list) -> list[dict]:
    """Move alternatives from start/end sub-entries up to the range level,
    and detect ranges within alternatives."""
    for entry in entries:
        if "start" not in entry:
            continue
        # Collect alternatives from start and end
        alts = []
        for sub_key in ("start", "end"):
            sub = entry.get(sub_key)
            if sub and "alternative" in sub:
                alts.extend(sub.pop("alternative"))
        if alts:
            # Detect ranges within alternatives (pairs connected by range tokens)
            if len(alts) == 2:
                a, b = alts
                a_num = a.get("number")
                b_num = b.get("number")
                if (isinstance(a_num, int) and isinstance(b_num, int)
                        and a_num < b_num):
                    # Check if there's a range token between them in the original tokens
                    entry["alternative"] = [{"start": a, "end": b}]
                else:
                    entry["alternative"] = alts
            else:
                entry["alternative"] = alts
    return entries


def _dedup_episodes(entries: list[dict]) -> list[dict]:
    """Merge duplicate episode numbers, keeping the entry with most info."""
    if len(entries) <= 1:
        return entries
    seen: dict[object, int] = {}  # number -> index in result
    result = []
    for entry in entries:
        if "start" in entry:  # range — always keep
            result.append(entry)
            continue
        num = entry.get("number")
        if num in seen:
            # Merge: keep the one with more fields
            existing = result[seen[num]]
            for k, v in entry.items():
                if k not in existing or existing[k] is None:
                    existing[k] = v
        else:
            seen[num] = len(result)
            result.append(entry)
    return result


def _has_episode_outside_bracket(token_list: list, current_idx: int, episode_tokens: list) -> bool:
    """Check if any existing episode token is outside the current bracket group."""
    # Find the opening bracket of the current group
    bracket_start_idx = -1
    for j in range(current_idx - 1, -1, -1):
        t = token_list[j]
        if t.category == Tag.BRACKET and t.content in constant.OPEN_BRACKETS:
            bracket_start_idx = t.index
            break
    if bracket_start_idx < 0:
        return False
    # Check if any episode token has index before this bracket
    return any(et.index < bracket_start_idx for et in episode_tokens)


def _has_range_before_in_bracket(token_list: list, current_idx: int) -> bool:
    """Check if there's a range token (dash/SEQUENCE_RANGE) before this number in the same bracket group."""
    for j in range(current_idx - 1, -1, -1):
        t = token_list[j]
        cat = t.category
        if cat == Tag.BRACKET:
            return False  # hit the bracket opening without finding a range
        if cat == Tag.SEQUENCE_RANGE or cat == Tag.CONTEXT_DELIMITER:
            return True
    return False


def _is_alternative_episode(token_list: list, current_idx: int) -> bool:
    """Check if this bracketed SEQUENCE_NUMBER is an alternative episode.

    True when the bracket group containing this number is immediately preceded
    by another SEQUENCE_NUMBER (with only delimiters/brackets between).
    """
    # Walk backward from current position to find what precedes the bracket group
    for j in range(current_idx - 1, -1, -1):
        t = token_list[j]
        cat = t.category
        if cat == Tag.BRACKET:
            continue  # skip the opening bracket
        if cat == Tag.DELIMITER or t.content.strip() == '':
            continue
        if cat == Tag.SEQUENCE_PREFIX:
            continue  # skip "episode" prefix inside the bracket
        # The first meaningful token before the bracket group
        return cat == Tag.SEQUENCE_NUMBER
    return False


def _get_bracket_unknown_text(token_list, seq_num_idx):
    """Get unknown text from the same bracket group as a SEQUENCE_NUMBER.

    Walks backward from seq_num_idx to find the bracket open, collecting
    UNKNOWN tokens. Returns merged text if found, else None.
    """
    unknown_parts = []
    for j in range(seq_num_idx - 1, -1, -1):
        t = token_list[j]
        if t.category == Tag.BRACKET:
            break  # reached the opening bracket
        if t.category == Tag.CONTEXT_DELIMITER:
            continue  # skip the dash separator
        if t.category == Tag.DELIMITER:
            if unknown_parts:
                unknown_parts.append(t.content)
            continue
        if t.category == Tag.UNKNOWN:
            unknown_parts.append(t.content)
        else:
            break
    if not unknown_parts:
        return None
    # Count actual words (not delimiters/punctuation)
    word_count = sum(1 for p in unknown_parts if p.strip() and p.strip().isalpha())
    if word_count < 2:
        return None  # single word isn't a title
    # Reverse since we walked backward
    unknown_parts.reverse()
    text = ''.join(unknown_parts).strip()
    return text if text else None


def _next_non_delimiter(token_list, current_idx):
    """Find next non-delimiter token after current index."""
    for j in range(current_idx + 1, len(token_list)):
        t = token_list[j]
        if t.category in (Tag.DELIMITER, Tag.CONTEXT_DELIMITER):
            continue
        return t
    return None


def _normalize_type(token: Token) -> str:
    """Normalize type using canonical form from keyword entry, or content as-is."""
    poss = token.possibilities.get(Tag.TYPE) or token.possibilities.get(Tag.SERIES_TYPE)
    if poss and poss.element and poss.element.canonical:
        return poss.element.canonical.lower()
    return token.content.lower()


def _try_int(s: str):
    try:
        return int(s)
    except (ValueError, TypeError):
        return None


def _normalize_audio_terms(terms: list[str]) -> list[str]:
    result = []
    seen = set()
    for term in terms:
        for part in _split_audio_term(term):
            key = part.lower()
            if key not in seen:
                seen.add(key)
                result.append(part)
    return result


def _split_audio_term(term: str) -> list[str]:
    m = re.match(r'^([a-z][a-z\-]+?)x\d{1,2}$', term, re.IGNORECASE)
    if m:
        return [m.group(1)]
    m = re.match(r'^(truehd|dd|flac|aac|dts)(\d{1,2}(?:\.\d{1,2}){0,2}(?:ch)?)$', term, re.IGNORECASE)
    if m:
        return [m.group(1), m.group(2)]
    return [term]


def _normalize_subs_terms(terms: list[str]) -> list[str]:
    result = []
    seen = set()
    for term in terms:
        m = re.match(r'^([a-z]+?)x\d{1,2}$', term, re.IGNORECASE)
        normalized = m.group(1) if m else term
        key = normalized.lower()
        if key not in seen:
            seen.add(key)
            result.append(normalized)
    return result


def _build_video_resolutions(tokens: Tokens) -> list[dict]:
    groups = []
    current_group = []

    for token in tokens:
        if token.category == Tag.VIDEO_RESOLUTION:
            current_group.append(token)
        else:
            if current_group:
                groups.append(current_group)
                current_group = []
    if current_group:
        groups.append(current_group)

    if not groups:
        return []

    resolutions = []
    for group in groups:
        combined = "".join(t.content for t in group).lower()

        match = re.match(r'^(\d+)([pi])$', combined)
        if match:
            resolutions.append({
                "video_height": int(match.group(1)),
                "scan_method": match.group(2),
            })
            continue

        match = re.match(r'^(\d+)k$', combined)
        if match:
            resolutions.append({
                "video_width": int(match.group(1)) * 1000,
            })
            continue

        match = re.match(r'^(\d+)[x×](\d+)$', combined)
        if match:
            resolutions.append({
                "video_width": int(match.group(1)),
                "video_height": int(match.group(2)),
            })
            continue

        if combined.isdigit():
            num = int(combined)
            if num > 100:
                entry: dict[str, int | str] = {"video_height": num}
                # Default scan method to 'p' for common resolutions
                if num in constant.COMMON_RESOLUTIONS:
                    entry["scan_method"] = "p"
                resolutions.append(entry)

    return resolutions
