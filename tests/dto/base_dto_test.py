from shared.dto.base_dto import BaseDTO, ignored


def test_left_side_is_ignored_in_eq():
    assert BaseDTO(id=ignored) == BaseDTO(id=1)


def test_right_side_is_ignored_in_eq():
    assert BaseDTO(id=1) == BaseDTO(id=ignored)


def test_either_sides_are_not_ignored_in_eq():
    assert BaseDTO(id=1) == BaseDTO(id=1)
    assert BaseDTO(id=1) != BaseDTO(id=2)

