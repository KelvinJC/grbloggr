from typing import List
import strawberry
import strawberry.django
from . import models


@strawberry.django.type(models.BlogPost)
class PostType:
    id: int
    title: str
    author: str
    message: str
