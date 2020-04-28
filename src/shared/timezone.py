import os

import pytz as pytz

TZ = pytz.timezone(os.getenv('TZ', 'Asia/Tokyo'))
