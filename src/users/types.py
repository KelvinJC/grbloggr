import strawberry

@strawberry.type
class UserType:
    username: str
    email: str
    phone_number: str
    password: strawberry.Private[str]

@strawberry.type
class LoginSuccess:
    user: UserType

@strawberry.type
class LoginError:
    message: str

