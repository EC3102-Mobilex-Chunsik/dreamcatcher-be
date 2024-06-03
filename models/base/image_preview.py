from pydantic import BaseModel, Field
from pydantic_core import Url


class ImagePreviewModel(BaseModel):
    image_url: Url = Field(
        description='컷신',
    )
