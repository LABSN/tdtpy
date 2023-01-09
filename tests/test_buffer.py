import pytest

from tdt.abstract_ring_buffer import pending


def test_pending():
    # Test that the number of samples pending are properly calculated given the
    # cycle count and index.
    assert pending(0, 0, 0, 1, 10) == 1
    assert pending(0, 0, 0, 9, 10) == 9
    assert pending(1, 0, 1, 1, 10) == 1
    assert pending(1, 0, 1, 9, 10) == 9
    assert pending(1, 5, 1, 9, 10) == 4
    assert pending(1, 5, 2, 4, 10) == 9
    assert pending(1, 5, 2, 5, 10) == 10

    with pytest.raises(ValueError, match='Number of slots exceeds buffer size'):
        pending(0, 0, 1, 9, 10)
    with pytest.raises(ValueError, match='Number of slots exceeds buffer size'):
        pending(1, 0, 2, 1, 10)
    with pytest.raises(ValueError, match='Start sample higher than end sample'):
        pending(3, 0, 2, 1, 10)
