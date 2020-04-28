from marshmallow_enum import EnumField


class Enum(EnumField):
    def __init__(self, enum, *args, **kwargs):
        super().__init__(enum, *args, **kwargs)
        self.metadata['enum'] = [e.value for e in enum]
        self.metadata['type'] = 'string'
