from __future__ import annotations

import itertools
import logging
import pathlib
import sys
from collections.abc import Sequence

from packaging.version import InvalidVersion, parse

if sys.version_info < (3, 10):
    from importlib_metadata import EntryPoint, entry_points
else:
    from importlib.metadata import entry_points, EntryPoint

from comictalker.comictalker import ComicTalker, TalkerError

logger = logging.getLogger(__name__)

__all__ = [
    "ComicTalker",
    "TalkerError",
]


def get_talkers(
    version: str, cache: pathlib.Path, local_plugins: Sequence[EntryPoint] = tuple()
) -> dict[str, ComicTalker]:
    """Returns all comic talker instances"""
    talkers: dict[str, ComicTalker] = {}
    ct_version = parse(version)

    # A dict is used, last plugin wins
    for talker in itertools.chain(entry_points(group="comictagger.talker"), local_plugins):
        try:
            talker_cls = talker.load()
            obj = talker_cls(version, cache)
            if obj.id != talker.name:
                logger.error("Talker ID must be the same as the entry point name")
                continue
            try:
                if ct_version >= parse(obj.comictagger_min_ver):
                    talkers[talker.name] = obj
                else:
                    logger.error(
                        f"Minimum ComicTagger version required of {obj.comictagger_min_ver} for talker {talker.name} is not met, will NOT load talker"
                    )
            except InvalidVersion:
                logger.warning(
                    f"Invalid minimum required ComicTagger version number for talker: {talker.name} - version: {obj.comictagger_min_ver}, will load talker anyway"
                )
                # Attempt to use the talker anyway
                # TODO flag this problem for later display to the user
                talkers[talker.name] = obj

        except Exception:
            logger.exception("Failed to load talker: %s", talker.name)

    return talkers
