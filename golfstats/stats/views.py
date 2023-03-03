from django.shortcuts import render
from .models import Player

def input_players(request):
    if request.method == 'POST':
        player_names = request.POST.getlist('player_name')
        for name in player_names:
            Player.objects.create(name=name)
    return render(request, 'input_players.html')

def display_stats(request):
    players = Player.objects.all()
    return render(request, 'display_stats.html', {'players': players})


# Create your views here.
