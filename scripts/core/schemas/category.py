from typing import Optional

import shortuuid
from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    title: str = Field(title="Name of the category")
    user_id: Optional[str] = Field(title="Category created by user", default="")
    description: str = Field(title="Description of the category")
    category_id: str = Field(default=shortuuid.ShortUUID().random(length=6))
