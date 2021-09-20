from dataclasses import field
from typing import Optional

from pydantic.dataclasses import dataclass
from pydantic import ValidationError, validator

from metlo.types.enums import FilterOp, JoinType, MetloSQLDataType, MetricType


NO_VALUE_FILTER_OPS = {FilterOp.NOT_NULL, FilterOp.IS_NULL}


@dataclass
class Filter:
    column: str
    op: FilterOp
    value: Optional[str] = None

    @validator('value')
    def filter_op_requires_value(cls, v, values):
        filter_op = values.get('op')
        fails = filter_op not in NO_VALUE_FILTER_OPS and not v
        if fails:
            raise ValidationError(
                f'You need to specify a value for the {filter_op} filter.'
            )
        return v

    def __hash__(self):
        return hash(f'{self.column} {self.op} {self.value}')

    def __eq__(self, other):
        self_sql = f'{self.column} {self.op} {self.value}'
        other_sql = f'{other.column} {other.op} {other.value}'
        return self_sql == other_sql


@dataclass
class Dimension:
    sql: str
    description: str = ''
    primary_key: bool = False
    data_type: MetloSQLDataType = MetloSQLDataType.OTHER


@dataclass
class Metric:
    name: str
    description: str
    type: MetricType = MetricType.SQL
    sql: Optional[str] = ''
    filters: list[Filter] = field(default_factory=list)


@dataclass
class Join:
    name: str
    table: str
    sql: str
    type: JoinType = JoinType.INNER


@dataclass
class Definition:
    id: str
    name: str
    owner: str
    description: str
    datasource: str
    table: str
    derived_table: bool = False
    joins: list[Join] = field(default_factory=list)
    metrics: list[Metric] = field(default_factory=list)
    dimensions: dict[str, Dimension] = field(default_factory=dict)
