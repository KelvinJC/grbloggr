from typing import List
import strawberry
from . import models
from blog.types import BlogPostType


@strawberry.django.type(models.User)
class AppUserType:
    username: str
    email: str
    phone_number: str
    password: strawberry.Private[str]
    blogposts: List["BlogPostType"]

@strawberry.type
class LoginSuccess:
    user: AppUserType

@strawberry.type
class LoginError:
    message: str
