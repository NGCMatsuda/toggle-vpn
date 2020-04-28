from typing import Any


def patch(mocker, function: Any, module=None, **kwargs):
    module_name = module.__name__ if module else function.__module__
    return mocker.patch(module_name + '.' + function.__name__, **kwargs)


def patch_class_method(mocker, method, **kwargs):
    return mocker.patch.object(method.__self__, method.__name__, **kwargs)
