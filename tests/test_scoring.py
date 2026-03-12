from packages.scoring.core import compute_composite_score, normalize_rank


def test_composite_score_uses_required_weights():
    score = compute_composite_score(80, 70, 60, 50, 40)
    assert score == 63.5


def test_rank_normalization_clamps_to_expected_range():
    assert normalize_rank(1) > normalize_rank(10)
    assert normalize_rank(100) == 0.0

