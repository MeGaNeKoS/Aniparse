"""Shared test helpers for fixture comparison."""
from dataclasses import dataclass, field
from typing import Optional, List

import pytest
import aniparse
from aniparse.output_schemas import Metadata
from aniparse.abstraction.keyword_base import ElementEntry
from aniparse.wordlist import InMemoryWordListProvider, WordListManager
from aniparse.core.constant import DEFAULT_PROVIDER_NAME


@dataclass
class Fixture:
    """Test fixture: a Metadata expected result + optional custom keywords for DB tests."""
    metadata: Metadata
    custom_keywords: Optional[List[ElementEntry]] = field(default=None)
    path: Optional[str] = field(default=None)

    @property
    def file_name(self):
        return self.metadata.file_name

    def to_dict(self):
        return self.metadata.to_dict()


def _normalize(value):
    """Lowercase strings for comparison."""
    if isinstance(value, str):
        return value.lower().strip()
    if isinstance(value, list):
        return [_normalize(v) for v in value]
    if isinstance(value, dict):
        return {k: _normalize(v) for k, v in value.items()}
    return value


def compare_dicts(expected, actual, path=""):
    """Compare expected fixture dict against actual parse output.
    Only checks keys present in expected (fixture is ground truth).
    Returns list of (path, expected, actual) mismatches.
    """
    mismatches = []
    for key, exp_val in expected.items():
        act_val = actual.get(key)
        full_path = f"{path}.{key}" if path else key

        if exp_val is None:
            continue

        if act_val is None:
            mismatches.append((full_path, exp_val, None))
            continue

        exp_norm = _normalize(exp_val)
        act_norm = _normalize(act_val)

        if isinstance(exp_norm, list) and isinstance(act_norm, list):
            for i, (e, a) in enumerate(zip(exp_norm, act_norm)):
                if isinstance(e, dict) and isinstance(a, dict):
                    mismatches.extend(compare_dicts(e, a, f"{full_path}[{i}]"))
                elif e != a:
                    mismatches.append((f"{full_path}[{i}]", e, a))
            if len(exp_norm) != len(act_norm):
                mismatches.append((f"{full_path}.length", len(exp_norm), len(act_norm)))
        elif isinstance(exp_norm, dict) and isinstance(act_norm, dict):
            mismatches.extend(compare_dicts(exp_norm, act_norm, full_path))
        elif exp_norm != act_norm:
            mismatches.append((full_path, exp_norm, act_norm))

    return mismatches


def run_fixture(fixture):
    """Run a single fixture through aniparse.parse() and assert correctness.

    Accepts either a Metadata (no custom keywords) or a Fixture (with custom keywords).
    """
    if isinstance(fixture, Fixture):
        custom_keywords = fixture.custom_keywords
        path = fixture.path
        expected = fixture.to_dict()
    else:
        custom_keywords = None
        path = None
        expected = fixture.to_dict()

    file_name = expected["file_name"]

    wlm = None
    if custom_keywords:
        wlm = WordListManager()
        provider = InMemoryWordListProvider()
        from aniparse import keyword
        for word in keyword.DEFAULT_KEYWORD:
            provider.add_word(word)
        for kw in custom_keywords:
            provider.add_word(kw)
        wlm.add_provider(DEFAULT_PROVIDER_NAME, provider)

    parse_kwargs = {"wordlist_provider": wlm}
    if path:
        parse_kwargs["path"] = path

    actual = aniparse.parse(file_name, **parse_kwargs)

    assert actual is not None, f"parse() returned None for: {file_name}"

    mismatches = compare_dicts(expected, actual)
    if mismatches:
        msg_lines = [f"Mismatches for: {file_name}"]
        for path, exp, act in mismatches:
            msg_lines.append(f"  {path}: expected={exp!r}, got={act!r}")
        pytest.fail("\n".join(msg_lines))
