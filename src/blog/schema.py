# import strawberry
# from typing import List
# from .models import BlogPost
# from .types import BlogPostType

# # Query
# # equivalent to Read operation and GET method
# @strawberry.type
# class Query:
#     @strawberry.field
#     def get_blogposts(self, title:str=None) -> List[BlogPostType]:
#         if title:
#             post = BlogPost.objects.filter(title=title)
#             return post
#         return BlogPost.objects.all()
    
#     @strawberry.field
#     def get_blogposts_by_limit(self, limit:int=None) -> List[BlogPostType]:
#         """ Return all posts up to limit provided """
#         blogs = BlogPost.objects.all()[0:limit]
#         return blogs
    
# # Mutation
# # equivalent to `Create, Update, Delete` operations
# # and `POST, PUT, PATCH, DELETE` methods
# @strawberry.type
# class Mutation:
#     @strawberry.field
#     def create_blogpost(self, title:str, author:str, message:str) -> BlogPostType:
#         blog = BlogPost(
#             title = title,
#             author = author,
#             message = message
#         )
#         blog.save()
#         return blog
    
#     @strawberry.field
#     def update_blogpost(self, id:int, title:str, author:str, message:str) -> BlogPostType:
#         blog = BlogPost.objects.get(id=id)
#         blog.title = title
#         blog.author = author
#         blog.message = message
#         blog.save()
#         return blog
    
#     @strawberry.field
#     def delete_blogpost(self, id:int) -> bool:
#         blog = BlogPost.objects.get(id=id)
#         blog.delete()
#         return True
    
# # Define a schema
# schema = strawberry.schema.Schema(query=Query, mutation=Mutation)