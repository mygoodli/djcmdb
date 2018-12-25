import datetime,json


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)

DateEncoder()