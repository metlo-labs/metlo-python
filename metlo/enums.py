from enum import Enum


class TimeGranularity(str, Enum):
    SECOND = 'second'
    MINUTE = 'minute'
    HOUR = 'hour'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'


class FilterOp(str, Enum):
    EQ = 'eq'
    LT = 'lt'
    GT = 'gt'
    LTE = 'lte'
    GTE = 'gte'
    IN = 'IN'
    LIKE = 'LIKE'
    NOT_NULL = 'not_null'
    IS_NULL = 'is_null'
