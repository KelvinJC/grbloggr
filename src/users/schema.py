  
from typing import List
from django.contrib.auth import get_user_model

import strawberry
from gqlauth.user.queries import UserQueries
from gqlauth.user import arg_mutations as mutations
from gqlauth.core.middlewares import JwtSchema

from .types import UserType1, BlogPostType
from users.models import User
from blog.models import BlogPost


@strawberry.django.type(model=get_user_model())
class Query:
    me: UserType1 = UserQueries.me # With MeQuery you can retrieve data for the currently authenticated user
    public: UserType1 = UserQueries.public_user

    @strawberry.field
    def get_blogposts(self, info: strawberry.Info, title:str=None) -> List[BlogPostType]:
        print("INFO CONTEXT REQ", info.context.request.user)
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

    register = mutations.Register.field              # --> user registration with username and pwd
    verify_account = mutations.VerifyAccount.field   # --> email verification during user registration 
    password_set = mutations.PasswordSet.field       # --> set password after passwordless registration
    password_change = mutations.PasswordChange.field
    update_account = mutations.UpdateAccount.field
    delete_account = mutations.DeleteAccount.field
    login = mutations.ObtainJSONWebToken.field       # --> login
    refresh_token = mutations.RefreshToken.field
    verify_token = mutations.VerifyToken.field


    @strawberry.field
    def create_blogpost(self, title:str, author:str, message:str) -> BlogPostType:
        blog = BlogPost(
            title = title,
            author = User.objects.filter(username=author).first(),
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
 

# This is essentially the same as strawberries schema,
# though it injects the user to `info.context["request"].user
schema = JwtSchema(query=Query, mutation= Mutation)
