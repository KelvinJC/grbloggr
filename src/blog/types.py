import strawberry
import strawberry.django
from users import models 


@strawberry.type
class BlogPostType:
    id: int
    title: str
    author: "LimitedAppUserType" 
    message: str

@strawberry.django.type(models.User)
class LimitedAppUserType:
    username: str
    email: str


@strawberry.type
class UpdateBlogPostSuccess:
    blog: BlogPostType

@strawberry.type
class UpdateNotPermittedError:
    error: bool = True
    message: str    