from shared_test.response_helper import _equal, ignored


def test_empty_array_is_only_equal_to_empty_array():
    assert not _equal([], dict())
    assert not _equal([], dict(a=1))
    assert not _equal([], [1])
    assert not _equal([], 'string')

    assert not _equal(dict(), [])
    assert not _equal(dict(a=1), [])
    assert not _equal([1], [])
    assert not _equal('string', [])

    assert _equal([], [])


def test_empty_dict_is_only_equal_to_empty_dict():
    assert not _equal(dict(), dict(a=1))
    assert not _equal(dict(), [])
    assert not _equal(dict(), [1])
    assert not _equal(dict(), 'string')

    assert not _equal(dict(a=1), dict())
    assert not _equal([], dict())
    assert not _equal([1], dict())
    assert not _equal('string', dict())

    assert _equal(dict(), dict())


def test_equal_dicts():
    value = dict(a=dict(b=['b', 1, 2.0, [1, 2, 3, 4]]))

    assert _equal(value, value)


def test_equal_arrays():
    value = [1, 2, 3, dict(a=dict(b=['b', 1, 2.0, [1, 2, 3, 4]]))]

    assert _equal(value, value)


def assert_equal_strings():
    assert _equal('abc', 'abc')


def assert_equal_integers():
    assert _equal(1, 1)


def test_equal_with_ignored_values():
    expected = dict(
        id=ignored,
        array=ignored,
        dict=ignored,
        a=dict(
            b=[ignored, 1, ]
        )
    )

    actual = dict(
        id=1,
        array=[6, 7],
        dict=dict(o=0),
        a=dict(
            b=['string', 1, ]
        )
    )

    assert _equal(actual, expected)
