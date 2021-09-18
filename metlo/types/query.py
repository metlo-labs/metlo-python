from typing import Optional
from datetime import datetime
from pydantic import conlist
from pydantic.dataclasses import dataclass

from metlo.types.enums import FilterOp, TimeGranularity


@dataclass
class Filter:
    dimension: str
    values: list
    op: FilterOp = FilterOp.EQ


@dataclass
class TimeDimension:
    dimension: str
    granularity: TimeGranularity
    date_range: Optional[conlist(datetime, min_items=2, max_items=2)] = None
