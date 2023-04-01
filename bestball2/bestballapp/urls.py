from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView #View for the user interface
from bestball2.schema import schema #Schema we want to query

urlpatterns = [
    path('admin/', admin.site.urls),
    # This URL will provide a user interface that is used to query the database
    # and interact with the GraphQL API.
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]

# from django.contrib import admin
# from django.urls import include, path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('newgame/', views.newgame, name='newgame'),
#     path('player_stats/<int:id>/', views.player_stats, name='player_stats'),
#     path('admin/', admin.site.urls),
# ]
