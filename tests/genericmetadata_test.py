from __future__ import annotations

import textwrap

import pytest

import comicapi.genericmetadata
from testing.comicdata import credits, metadata


def test_apply_default_page_list(tmp_path):
    md = comicapi.genericmetadata.GenericMetadata()
    md.overlay(comicapi.genericmetadata.md_test)
    md.pages = []
    md.apply_default_page_list(["testing"])

    assert isinstance(md.pages[0]["image_index"], int)


@pytest.mark.parametrize("replaced, expected", metadata)
def test_metadata_overlay(md: comicapi.genericmetadata.GenericMetadata, replaced, expected):
    md.overlay(replaced)

    assert md == expected


def test_add_credit():
    md = comicapi.genericmetadata.GenericMetadata()

    md.add_credit(person="test", role="writer", primary=False)
    assert md.credits == [comicapi.genericmetadata.Credit(person="test", role="writer", primary=False)]


def test_add_credit_primary():
    md = comicapi.genericmetadata.GenericMetadata()

    md.add_credit(person="test", role="writer", primary=False)
    md.add_credit(person="test", role="writer", primary=True)
    assert md.credits == [comicapi.genericmetadata.Credit(person="test", role="writer", primary=True)]


@pytest.mark.parametrize("md, role, expected", credits)
def test_get_primary_credit(md, role, expected):
    assert md.get_primary_credit(role) == expected


def test_str(md):
    expected = textwrap.dedent(
        """\
        series:           Cory Doctorow's Futuristic Tales of the Here and Now
        issue:            1
        issue_count:      6
        title:            Anda's Game
        publisher:        IDW Publishing
        year:             2007
        month:            10
        day:              1
        volume:           1
        genres:           Sci-Fi
        language:         en
        critical_rating:  3.0
        alternate_series: Tales
        alternate_number: 2
        alternate_count:  7
        imprint:          craphound.com
        web_links:        ['https://comicvine.gamespot.com/cory-doctorows-futuristic-tales-of-the-here-and-no/4000-140529/']
        format:           Series
        manga:            No
        maturity_rating:  Everyone 10+
        story_arcs:       ['Here and Now']
        series_groups:    ['Futuristic Tales']
        scan_info:        (CC BY-NC-SA 3.0)
        characters:       Anda
        teams:            Fahrenheit
        locations:        lonely  cottage
        description:      For 12-year-old Anda, getting paid real money to kill the characters of players who were cheating in her favorite online computer game was a win-win situation. Until she found out who was paying her, and what those characters meant to the livelihood of children around the world.
        notes:            Tagged with ComicTagger 1.3.2a5 using info from Comic Vine on 2022-04-16 15:52:26. [Issue ID 140529]
        credit:           Writer: Dara Naraghi
        credit:           Penciller: Esteve Polls
        credit:           Inker: Esteve Polls
        credit:           Letterer: Neil Uyetake
        credit:           Cover: Sam Kieth
        credit:           Editor: Ted Adams
    """
    )

    assert str(md) == expected
