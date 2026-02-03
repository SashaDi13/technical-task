from pydantic import BaseModel, HttpUrl


class PropertySchema(BaseModel):
    title: str
    price: int
    description: str
    address: str
    object_id: int
    url: HttpUrl
    image_url: HttpUrl
