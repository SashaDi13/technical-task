from pydantic import BaseModel, HttpUrl


class PropertySchema(BaseModel):
    title: str
    price: str
    description: str
    address: str
    url: HttpUrl
    image_url: HttpUrl
