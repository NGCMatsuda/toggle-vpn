import pytest

pytest.register_assert_rewrite("shared_test.response_helper")
pytest.register_assert_rewrite("shared_test.api_helper")
pytest.register_assert_rewrite("shared_test.mocker_helper")
