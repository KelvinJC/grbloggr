from typing import List, Union, Annotated

from django.contrib.auth import get_user_model
import strawberry

from .types import BlogPostType, UpdateBlogPostSuccess, UpdateNotPermittedError
from .models import BlogPost
from users.permissions import IsAuthenticated


@strawberry.django.type(model=get_user_model())
class Query:

    @strawberry.field(permission_classes=[IsAuthenticated])
    def get_blogposts(self, info: strawberry.Info, title:str=None) -> List[BlogPostType]:
        if title:
            post = BlogPost.objects.filter(title=title)
            return post
        return BlogPost.objects.all()
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    def get_blogposts_by_limit(self, limit:int=None) -> List[BlogPostType]:
        """ Return all posts up to limit provided """
        blogs = BlogPost.objects.all()[0:limit]
        return blogs
    

# Create a Union type to represent the 2 results from the mutation
UpdateResponse = Annotated[
    Union[UpdateBlogPostSuccess, UpdateNotPermittedError],
    strawberry.union("UpdateBlogPostResponse"),
]

@strawberry.type
class Mutation:

    @strawberry.field(permission_classes=[IsAuthenticated])
    def create_blogpost(self, info: strawberry.Info, title:str, message:str) -> BlogPostType:
        blog = BlogPost(
            title = title,
            author = info.context.request.user, # User.objects.filter(username=user).first(),
            message = message
        )
        blog.save()
        return blog
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    def update_blogpost(self, info: strawberry.Info, id:int, title:str, message:str) -> UpdateResponse:
        blog = BlogPost.objects.get(id=id)
        if blog.author == info.context.request.user:
            blog.title = title
            blog.message = message
            blog.save()
            return UpdateBlogPostSuccess(blog=blog)
        return UpdateNotPermittedError(message="ERROR: Update failed. Blog post update restricted to author.")

    @strawberry.field(permission_classes=[IsAuthenticated])
    def delete_blogpost(self, info: strawberry.Info, id:int) -> bool:
        blog = BlogPost.objects.get(id=id)
        if blog.author == info.context.request.user:
            blog.delete()
            return True
        return False
 

