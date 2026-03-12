from packages.providers.matching import match_host_alias


def test_match_host_alias_returns_best_match():
    alias_map = {
        "host-a": ["Host A", "Alice Example"],
        "host-b": ["Host B"],
    }

    match = match_host_alias("Alice Example joins the roundtable", alias_map)

    assert match is not None
    assert match.host_slug == "host-a"
    assert match.confidence > 0.55

