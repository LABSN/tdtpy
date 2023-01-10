import pytest

from tdt.abstract_ring_buffer import span


def test_span():
    # Test that the number of samples span are properly calculated given the
    # cycle count and index.
    assert span(0, 0, 0, 1, 10) == 1
    assert span(0, 0, 0, 9, 10) == 9
    assert span(1, 0, 1, 1, 10) == 1
    assert span(1, 0, 1, 9, 10) == 9
    assert span(1, 5, 1, 9, 10) == 4
    assert span(1, 5, 2, 4, 10) == 9
    assert span(1, 5, 2, 5, 10) == 10

    with pytest.raises(ValueError, match='Number of slots exceeds buffer size'):
        span(0, 0, 1, 9, 10)
    with pytest.raises(ValueError, match='Number of slots exceeds buffer size'):
        span(1, 0, 2, 1, 10)
    with pytest.raises(ValueError, match='Start sample higher than end sample'):
        span(3, 0, 2, 1, 10)
