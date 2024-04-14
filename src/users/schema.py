import strawberry
from django.contrib.auth import get_user_model
from gqlauth.user.queries import UserQueries
from gqlauth.user import arg_mutations as mutations

from .types import AppUserType


@strawberry.django.type(model=get_user_model())
class Query:
    me: AppUserType = UserQueries.me # retrieve data for the currently authenticated user
    public: AppUserType = UserQueries.public_user
    

@strawberry.type
class Mutation:

    register = mutations.Register.field              # --> user registration with username and pwd
    verify_account = mutations.VerifyAccount.field   # --> email verification during user registration 
    login = mutations.ObtainJSONWebToken.field       # --> login
    password_set = mutations.PasswordSet.field       # --> set password after passwordless registration
    password_change = mutations.PasswordChange.field
    update_account = mutations.UpdateAccount.field
    delete_account = mutations.DeleteAccount.field
    refresh_token = mutations.RefreshToken.field
    verify_token = mutations.VerifyToken.field


 

