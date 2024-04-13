from typing import List
import strawberry
from . import models


@strawberry.type
class BlogPostType:
    id: int
    title: str
    author: "UserType1" 
    message: str

@strawberry.django.type(models.User)
class UserType1:
    username: str
    email: str
    phone_number: str
    password: strawberry.Private[str]
    blogposts: List["BlogPostType"]

@strawberry.type
class LoginSuccess:
    user: UserType1

@strawberry.type
class LoginError:
    message: str
