from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime, mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
]
updated_at = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True
    ),
]
