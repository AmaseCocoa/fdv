from typing import Literal, Optional

from pydantic import BaseModel, Field


class BadgeParams(BaseModel):
    account: str = Field()


class JSONBadge(BaseModel):
    schemaVersion: Literal[1] = Field(default=1)
    label: str = Field(default="")
    message: str = Field()
    color: str = Field(default="FA007C")
    labelColor: str = Field(default="gray")
    isError: bool = Field(default=False)
    namedLogo: Optional[str] = Field(default=None)
    logoColor: str = Field(default="white")
    style: Literal[
        "flat", "flat-square", "plastic", "for-the-badge", "social"
    ] = Field(default="flat")
