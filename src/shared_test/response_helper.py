class IgnoredValue:
    def __repr__(self) -> str:
        return "#ignored#"


ignored = IgnoredValue()


def _equal(actual, expected):
    if actual == expected:
        return True
    elif isinstance(expected, ignored.__class__):
        return True
    elif actual.__class__ == expected.__class__:
        if isinstance(actual, dict):
            return actual.keys() == expected.keys() and \
                   all([_equal(actual[key], expected[key]) for key in actual.keys()])
        if isinstance(actual, [].__class__):
            return len(actual) == len(expected) and \
                   all([_equal(actual[index], expected[index]) for index, _ in enumerate(actual)])

    return False


def assert_response_equals(actual, expected):
    if not _equal(actual, expected):
        assert actual == expected
