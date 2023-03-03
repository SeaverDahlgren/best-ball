from django.shortcuts import render, get_object_or_404
from .models import Player, Stat

def home(request):
    if request.method == 'POST':
        num_players = int(request.POST['num_players'])
        player_names = []
        for i in range(num_players):
            player_names.append(request.POST['player_name{}'.format(i)])
        players = []
        for name in player_names:
            player = Player(name=name)
            player.save()
            players.append(player)
        context = {'players': players}
        return render(request, 'select_player.html', context)
    players = Player.objects.all()
    context = {'players': players}
    return render(request, 'home.html', context)

def select_player(request):
    players = Player.objects.all()
    context = {'players': players}
    return render(request, 'select_player.html', context)

def player_stats(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    stats = Stat.objects.filter(player=player)
    context = {'player': player, 'stats': stats}
    return render(request, 'player_stats.html', context)


