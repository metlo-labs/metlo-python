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


class JoinType(str, Enum):
    INNER = 'inner'
    LEFT = 'left'
    RIGHT = 'right'
    OUTER = 'outer'


class MetricType(str, Enum):
    SQL = 'sql'
    SUM = 'sum'
    AVG = 'avg'
    MIN = 'min'
    MAX = 'max'
    COUNT = 'count'
    COUNT_DISTINCT = 'count_distinct'


class MetloSQLDataType(str, Enum):
    BOOLEAN = 'boolean'
    STRING = 'string'
    INT = 'int'
    FLOAT = 'float'
    DECIMAL = 'decimal'
    DATE = 'date'
    TIME_TZ = 'time_tz'
    TIME = 'time'
    TIMESTAMP_TZ = 'timestamp_tz'
    TIMESTAMP = 'timestamp'
    OTHER = 'other'
