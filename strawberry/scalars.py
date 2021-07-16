from datetime import date, datetime, time
from decimal import Decimal
from typing import NewType, Type
from uuid import UUID


ID = NewType("ID", str)
SCALAR_TYPES = [int, str, float, bytes, bool, UUID, datetime, date, time, Decimal]


def is_scalar(annotation: Type) -> bool:
    type = getattr(annotation, "__supertype__", annotation)

    if type in SCALAR_TYPES:
        return True

    return hasattr(annotation, "_scalar_definition")
