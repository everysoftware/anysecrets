from __future__ import annotations

import datetime
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from pydantic import ConfigDict, Field, computed_field
from sqlalchemy import Select

from backend.base.models import Entity
from backend.base.schemas import BaseModel
from backend.base.types import UUID

T = TypeVar("T")


class Specification(BaseModel, ABC):
    @abstractmethod
    def to_expression(self, stmt: Select[T], model_type: type[Entity]) -> Select[T]: ...  # type: ignore[type-var]


class Filter(Specification):
    id: UUID | None = None
    created_at_gt: datetime.datetime | None = None
    created_at_lt: datetime.datetime | None = None
    updated_at_gt: datetime.datetime | None = None
    updated_at_lt: datetime.datetime | None = None

    def to_expression(self, stmt: Select[T], model_type: type[Entity]) -> Select[T]:  # type: ignore[type-var]
        for criteria_name in self.model_fields_set:
            criteria_value = getattr(self, criteria_name)
            if criteria_value is None:
                continue
            field, operator = split_criteria_name(criteria_name)
            stmt = process_operator(stmt, model_type, field, operator, criteria_value)
        return stmt


class Sort(Specification):
    sort: str = "updated_at:desc"

    def to_expression(self, stmt: Select[T], model_type: type[Entity]) -> Select[T]:  # type: ignore[type-var]
        for entry in self.sort.split(","):
            field, order = split_sort_entry(entry)
            attr = getattr(model_type, field)
            if attr is None:
                raise ValueError(f"Invalid field: `{field}`")
            stmt = stmt.order_by(attr.asc() if order == "asc" else attr.desc())
        return stmt


class BasicPagination(Specification):
    limit: int = Field(100, ge=0)
    offset: int = Field(0, ge=0)

    def to_expression(self, stmt: Select[T], model_type: type[Entity]) -> Select[T]:  # type: ignore[type-var]
        return stmt.limit(self.limit).offset(self.offset)


class Page(BaseModel, Generic[T]):
    items: Sequence[T]

    @computed_field  # type: ignore
    @property
    def total(self) -> int:
        return len(self.items)

    def __bool__(self) -> bool:
        return bool(self.items)

    model_config = ConfigDict(arbitrary_types_allowed=True)


def split_criteria_name(criteria_name: str) -> tuple[str, str]:
    parts = criteria_name.split("_")
    if len(parts) == 1:
        return parts[0], "eq"
    return "_".join(parts[:-1]), parts[-1]


def process_operator(stmt: Select[T], model_type: type[Entity], field: str, op: str, value: Any) -> Select[T]:  # type: ignore[type-var]
    model_field = getattr(model_type, field)
    if model_field is None:
        raise ValueError(f"Invalid field: `{field}`")
    if op == "eq":
        return stmt.where(model_field == value)
    elif op == "ne":
        return stmt.where(model_field != value)
    elif op == "gt":
        return stmt.where(model_field > value)
    elif op == "lt":
        return stmt.where(model_field < value)
    elif op == "in":
        return stmt.where(model_field.in_(value))
    elif op == "like":
        return stmt.where(model_field.like(value))
    elif op == "ilike":
        return stmt.where(model_field.ilike(value))
    elif op == "contains":
        return stmt.where(model_field.contains(value))
    else:
        raise ValueError(f"Invalid operator: `{op}`")


def split_sort_entry(entry: str) -> tuple[str, str]:
    values = entry.lower().split(":")
    if not values or len(values) > 2:
        raise ValueError(f"Invalid sort entry: `{entry}`")
    if len(values) == 1:
        values.append("asc")
    field, order = values
    if order not in ["asc", "desc"]:
        raise ValueError(f"Invalid sort order: `{order}`")
    return field, order
