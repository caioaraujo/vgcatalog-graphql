import strawberry
from app.api.graphql.resolvers import Query, Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)
