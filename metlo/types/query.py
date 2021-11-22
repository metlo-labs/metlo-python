from typing import Optional
from datetime import datetime
from pydantic import conlist, root_validator, validator
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
    granularity: Optional[TimeGranularity] = None
    calculate_rel_change: bool = False
    date_range: Optional[conlist(datetime, min_items=2, max_items=2)] = None
    lookback: Optional[str] = None

    @root_validator
    def check_lookback(cls, values):
        if values.get("lookback") and values.get("date_range"):
            raise ValueError(
                "Cannot specify lookback and date range in the same time dimension"
            )
        return values

    @root_validator
    def check_granularity(cls, values):
        if not values.get("granularity") and not (values.get("date_range") or values.get("lookback")):
            raise ValueError(
                "Must specify a time granularity if there is no date_range or lookback"
            )
        return values

    @validator("calculate_rel_change")
    def check_calculate_rel_change(cls, v, values):
        if v and not (values.get("granularity")):
            raise ValueError("Must specify a time granularity to calculate rel change")
        return v
