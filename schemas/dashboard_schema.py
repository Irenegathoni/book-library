from pydantic import BaseModel
from typing import Optional
class DashboardResponse(BaseModel):
    books_read_count: int
    currently_reading: Optional[str] = None  # book title
    current_book_genre: Optional[str] = None
    current_book_image: Optional[str] = None
    model_config={"from_attributes":True}