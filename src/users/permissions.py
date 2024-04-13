import typing
import strawberry
from strawberry.permission import BasePermission
from django.contrib.auth.models import AnonymousUser 


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"
 
    # This method can also be async!
    def has_permission(self, source: typing.Any, info: strawberry.Info, **kwargs) -> bool:
        print("PATH", info.path.key)
        if isinstance(info.context.request.user,  AnonymousUser):
            return False
        return True


# NOTE: 
# Couldn't figure out how to pass the blog instance into 
# the has_permission method of a permission class
# to enable a comparsion of its author with the info.context.request.user.
# Decided to return an UpdateError type if a different user attempts an update

# DRF example:
# class IsBlogPostAuthorOrReadOnly(BasePermission):
#     ''' Restrict update, partial update and delete requests to blog post author.'''
    
#     # def has_object_permission(self, request, view, obj):
#     def has_permission(self, source: typing.Any, info: strawberry.Info, **kwargs):

#         # allow GET, HEAD, and OPTIONS requests (read-only)
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         # check if the requesting user is the owner of the blog post
#         return obj.author == request.user