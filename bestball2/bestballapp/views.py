from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Ball, Player, Session, Stat
from .forms import getPlayerInfo

def home(request):
    return render(request, 'home.html')

def newgame(request):
    if request.method == 'POST':
        form = getPlayerInfo(request.POST)
        if form.is_valid():
            p1 = form.cleaned_data["player1"]
            p2 = form.cleaned_data["player2"]
            p3 = form.cleaned_data["player3"]
            print("You entered P1:" + p1)
            if p1 == '' and p2 == '' and p3 == '':
                return render(request, 'newgame.html')
            newSession = Session.objects.create()
            # Clear the players in the session
            newSession.players.clear()
            players = [p1, p2, p3]
            playList = []
            for player in players:
                newPlay, _ = Player.objects.get_or_create(name=player)
                playList.append(newPlay)
                # newSession.players.add(newPlay)
            newSession.players.set(playList)
            return redirect(reverse('player_stats', args=(newSession.id,)))
    form = getPlayerInfo()
    context = {'form': form}
    return render(request, 'newgame.html', context)

def select_player(request):
    players = Player.objects.all()
    context = {'players': players}
    return render(request, 'select_player.html', context)

def player_stats(request, id):
    # player = get_object_or_404(Player, pk=player_id)
    # stats = Stat.objects.filter(player=player)
    # context = {'player': player, 'stats': stats}
    session = get_object_or_404(Session, id=id)
    players = session.players.all()
    context = {'session': session, 'players': players}
    return render(request, 'player_stats.html', context)

@csrf_exempt
def pair_ball(request):
    if request.method == 'POST':
        player_name = request.POST.get('player_name')
        ball_id = request.POST.get('ball_id')
        player = get_object_or_404(Player, name=player_name)
        ball = get_object_or_404(Ball, pk=ball_id)
        player.currentBall = ball
        player.save()
        return HttpResponse("Ball assigned to player successfully!")
    else:
        return HttpResponse("Invalid Request!")
