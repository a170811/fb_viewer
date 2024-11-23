from pydantic import BaseModel, Field


class Post(BaseModel):
    source: str = Field(..., description="訊息來源")
    content: str = Field(..., description="訊息內容")

    def __str__(self):
        return f"source: {self.source}\n" f"content: {self.content}\n"
