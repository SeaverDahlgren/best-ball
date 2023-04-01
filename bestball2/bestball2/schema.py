import graphene
from graphene_django import DjangoObjectType #used to change Django object into a format that is readable by GraphQL
from bestballapp.models import Player, Ball

class PlayerType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = Player
        field = ("id", "name", "putts")

class BallType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = Ball
        field = ("id", "color", "distanceFromHole", "currentPlayer")

class Query(graphene.ObjectType):
    #query ContactType to get list of contacts
    list_player=graphene.List(PlayerType)
    read_player=graphene.Field(PlayerType, id=graphene.Int())
    list_ball=graphene.List(BallType)

    def resolve_list_player(root, info):
        # We can easily optimize query count in the resolve method
        return Player.objects.all()
    
    def resolve_read_player(root, info, id):
        return Player.objects.get(id=id)
    
    def resolve_list_ball(root, info):
        return Ball.objects.all()

class CreatePlayer(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        putts = graphene.Int()

    ok = graphene.Boolean()
    player = graphene.Field(PlayerType)

    def mutate(self, info, name, putts):
        player = Player(name=name, putts=putts)
        player.save()
        return CreatePlayer(ok=True, player=player)
    
class Mutation(graphene.ObjectType):
    create_player = CreatePlayer.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)