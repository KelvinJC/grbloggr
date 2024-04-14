from typing import List

from django.contrib.auth import get_user_model
import strawberry

from .types import (
    BlogPostType, DeleteBlogPostResponse, UpdateResponse, DeleteResponse,
    DeleteNotPermittedError, UpdateBlogPostSuccess, UpdateNotPermittedError,
)
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
    def delete_blogpost(self, info: strawberry.Info, id:int) -> DeleteResponse:
        blog = BlogPost.objects.get(id=id)
        if blog.author == info.context.request.user:
            blog.delete()
            return DeleteBlogPostResponse
        return DeleteNotPermittedError(message="ERROR: Delete failed. Delete operation restricted to author.")
 

