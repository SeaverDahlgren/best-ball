from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('newgame/', views.newgame, name='newgame'),
    path('player_stats/<int:id>/', views.player_stats, name='player_stats'),
    path('pair_ball/', views.pair_ball, name='pair_ball'),
    path('change_dist/', views.set_ball_distance, name='change_dist'),
    path('admin/', admin.site.urls),
]
