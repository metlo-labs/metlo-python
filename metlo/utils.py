from datetime import datetime, date
import json


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)
