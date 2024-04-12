# from typing import Union, Annotated
# from django.contrib.auth import authenticate
# import strawberry
# from .types import LoginError, LoginSuccess
# from .models import User

# LoginResult = Annotated[
#     Union[LoginSuccess, LoginError], strawberry.union("LoginResult")
# ]

# @strawberry.type
# class Mutation:
#     @strawberry.field
#     def login(self, username: str, password: str) -> LoginResult:
#         user = authenticate(username=username, password=password)
#         if user is None:
#             return LoginError(message="Something went wrong")
#         return LoginSuccess(user=User(username=username))
    

import strawberry
from gqlauth.user.queries import UserQueries
from gqlauth.user import arg_mutations as mutations
from gqlauth.core.middlewares import JwtSchema
from django.contrib.auth import get_user_model
from users.types import UserType

# blog
from typing import List
from blog.models import BlogPost
from blog.types import BlogPostType


@strawberry.django.type(model=get_user_model())
class Query:
    me: UserType = UserQueries.me
    public: UserType = UserQueries.public_user

    @strawberry.field
    def get_blogposts(self, title:str=None) -> List[BlogPostType]:
        if title:
            post = BlogPost.objects.filter(title=title)
            return post
        return BlogPost.objects.all()
    
    @strawberry.field
    def get_blogposts_by_limit(self, limit:int=None) -> List[BlogPostType]:
        """ Return all posts up to limit provided """
        blogs = BlogPost.objects.all()[0:limit]
        return blogs
    

@strawberry.type
class Mutation:

    register = mutations.Register.field
    verify_account = mutations.VerifyAccount.field # login
    password_set = mutations.PasswordSet.field
    password_change = mutations.PasswordChange.field
    update_account = mutations.UpdateAccount.field
    delete_account = mutations.DeleteAccount.field
    token_auth = mutations.ObtainJSONWebToken.field
    refresh_token = mutations.RefreshToken.field
    verify_token = mutations.VerifyToken.field

    @strawberry.field
    def create_blogpost(self, title:str, author:str, message:str) -> BlogPostType:
        blog = BlogPost(
            title = title,
            author = author,
            message = message
        )
        blog.save()
        return blog
    
    @strawberry.field
    def update_blogpost(self, id:int, title:str, author:str, message:str) -> BlogPostType:
        blog = BlogPost.objects.get(id=id)
        blog.title = title
        blog.author = author
        blog.message = message
        blog.save()
        return blog
    
    @strawberry.field
    def delete_blogpost(self, id:int) -> bool:
        blog = BlogPost.objects.get(id=id)
        blog.delete()
        return True
 

# This is essentially the same as strawberries schema though it
# injects the user to `info.context["request"].user
schema = JwtSchema(query=Query, mutation= Mutation)
