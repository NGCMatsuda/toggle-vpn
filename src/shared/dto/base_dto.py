
class IgnoredAttribute:
    def __repr__(self) -> str:
        return '#ignored#'


ignored = IgnoredAttribute()


class BaseDTO:
    def __init__(self, **kwargs):
        self.attribute_names = list(kwargs.keys())
        self.attribute_names.sort()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        if not self.attribute_names == other.attribute_names:
            return False

        for key in self.attribute_names:
            if ((getattr(other, key) is not ignored and getattr(self, key) is not ignored) and
                    getattr(self, key) != getattr(other, key)):
                return False

        return True

    def __repr__(self):
        lines = [self.__class__.__name__ + ': {']
        for key in self.attribute_names:
            lines += '{}: {},'.format(key, str(getattr(self, key))).split('\n')
        lines += '}'
        return '\n    '.join(lines)
