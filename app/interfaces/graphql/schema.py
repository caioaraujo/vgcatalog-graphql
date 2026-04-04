import strawberry
from app.interfaces.graphql.resolvers import Query, Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)
