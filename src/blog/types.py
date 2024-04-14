from typing import Union, Annotated

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
    message: str    


@strawberry.type
class DeleteBlogPostResponse:
    success: bool = True

@strawberry.type
class DeleteNotPermittedError:
    message: str 

# Create a Union type to represent the 2 results from the mutation
UpdateResponse = Annotated[
    Union[UpdateBlogPostSuccess, UpdateNotPermittedError],
    strawberry.union("UpdateBlogPostResponse"),
]

DeleteResponse = Annotated[
    Union[DeleteBlogPostResponse, DeleteNotPermittedError],
    strawberry.union("DeleteBlogResponse"),
]