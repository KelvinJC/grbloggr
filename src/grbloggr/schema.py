import strawberry
from gqlauth.core.middlewares import JwtSchema

from users import schema as user_schema
from blog import schema as blog_schema


@strawberry.type
class Query(user_schema.Query, blog_schema.Query):
    pass
    

@strawberry.type
class Mutation(user_schema.Mutation, blog_schema.Mutation):
    pass
    

# This is essentially the same as strawberries schema,
# though it injects the user to `info.context["request"].user
schema = JwtSchema(query=Query, mutation= Mutation)
