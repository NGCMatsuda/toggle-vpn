import logging
import traceback


def mark_as_temporary(tag):
    return TemporaryFunctionality(tag)


class TemporaryFunctionality:
    def __init__(self, tag):
        self.tag = tag

    def __enter__(self):
        trace_frame = traceback.extract_stack()[-2]
        logging.warning(
            f'Temporary function warning {self.tag}: file://{trace_frame.filename}:{trace_frame.lineno + 1}')

    def __exit__(self, *_):
        pass
