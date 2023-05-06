from django.http import HttpResponse, JsonResponse
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
            if p1 == '' and p2 == '' and p3 == '':
                return render(request, 'newgame.html')
            newSession = Session.objects.create()
            # Clear the players in the session
            newSession.players.clear()
            players = [p1, p2, p3]
            playList = []
            for ball_id, player in enumerate(players, start=1):
                newPlay, _ = Player.objects.get_or_create(name=player)
                playList.append(newPlay)
                ball = get_object_or_404(Ball, pk=ball_id)
                ball.distanceFromHole = 0
                try:
                    oldPlayer = Player.objects.get(currentBall=ball)
                    oldPlayer.currentBall = None
                    oldPlayer.save()
                except:
                    pass
                newPlay.currentBall = ball
                newPlay.save()
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
        try:
            oldPlayer = Player.objects.get(currentBall=ball)
            oldPlayer.currentBall = None
            oldPlayer.save()
        except:
            pass
        player.currentBall = ball
        player.save()
        return HttpResponse("Ball assigned to player successfully!")
    else:
        return HttpResponse("Invalid Request!")


@csrf_exempt
def set_ball_distance(request):
    if request.method == 'POST':
        ball_id = request.POST.get('ball_id')
        new_dist = request.POST.get("new_dist")
        ball = get_object_or_404(Ball, pk=ball_id)
        ball.distanceFromHole = new_dist//10
        ball.save()
        return HttpResponse("Ball Distance Changed")
    else:
        return HttpResponse("Invalid Request!")

@csrf_exempt
def new_ball(request):
    if request.method == 'POST':
        color = request.POST.get('color')
        ball = Ball.objects.create(color=color)
        return HttpResponse("Created new Ball!")
    else:
        return HttpResponse("Invalid Request!")


@csrf_exempt
def add_stroke(request):
    if request.method == 'POST':
        ball_id = request.POST.get('ball_id')
        ball = get_object_or_404(Ball, pk=ball_id)
        ball.strokes += 1
        ball.save()
        return HttpResponse("Stroke Incremented!")
    else:
        return HttpResponse("Invalid Request!")

@csrf_exempt
def reset_stroke(request):
    if request.method == 'POST':
        ball_id = request.POST.get('ball_id')
        ball = get_object_or_404(Ball, pk=ball_id)
        ball.strokes = 0
        ball.save()
        return HttpResponse("Stroke Count Reset!")
    else:
        return HttpResponse("Invalid Request!")

@csrf_exempt
def set_hole(request):
    if request.method == 'POST':
        ball_id = request.POST.get('ball_id')
        in_hole = request.POST.get('in_hole')
        ball = get_object_or_404(Ball, pk=ball_id)
        ball.inHole = in_hole
        ball.save()
        return HttpResponse("In Hole Changed!")
    else:
        return HttpResponse("Invalid Request!")

@csrf_exempt
def set_spin(request):
    if request.method == 'POST':
        ball_id = request.POST.get('ball_id')
        spin_rate = request.POST.get('spin_rate')
        ball = get_object_or_404(Ball, pk=ball_id)
        ball.currentSpinRate = spin_rate
        ball.save()
        return HttpResponse("Set new Spin Rate!")
    else:
        return HttpResponse("Invalid Request!")

def get_players_data(request):
    players = Player.objects.all()  # Retrieve all player objects from the database

    # Prepare the data in a format suitable for JSON serialization
    data = []
    for player in players:
        if player.currentBall is not None:
            player_data = {
                'name': player.name,
                'currentBall': {
                    'strokes': player.currentBall.strokes,
                    'id': player.currentBall.id,
                    'strokes': player.currentBall.strokes,
                    'distanceFromHole': player.currentBall.distanceFromHole,
                    'currentSpinRate': player.currentBall.currentSpinRate,
                    'inHole': player.currentBall.inHole
                }
            }
            data.append(player_data)

    return JsonResponse({'data': data})

