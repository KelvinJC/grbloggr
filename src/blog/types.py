import strawberry
import strawberry.django
from users import models 


@strawberry.type
class BlogPostType:
    id: int
    title: str
    author: "LimitedUserType1" 
    message: str

@strawberry.django.type(models.User)
class LimitedUserType1:
    username: str
    email: str


@strawberry.type
class UpdateBlogPostSuccess:
    blog: BlogPostType

@strawberry.type
class UpdateNotPermittedError:
    error: bool = True
    message: str    