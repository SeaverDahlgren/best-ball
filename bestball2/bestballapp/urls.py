from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('newgame/', views.newgame, name='newgame'),
    path('player_stats/<int:id>/', views.player_stats, name='player_stats'),
    path('pair_ball/', views.pair_ball, name='pair_ball'),
    path('change_dist/', views.set_ball_distance, name='change_dist'),
    path('add_stroke/', views.add_stroke, name='add_stroke'),
    path('set_hole/', views.set_hole, name='set_hole'),
    path('api/players/', views.get_players_data, name='get_players_data'),
    path('admin/', admin.site.urls),
]
