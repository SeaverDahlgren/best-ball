from django.db import models

# Create your models here.
class Ball(models.Model):
    color = models.CharField(max_length=50)
    # Set Default ball distance from hole to 100 arbitrarily
    distanceFromHole = models.DecimalField(max_digits=8, decimal_places=3, default=100)
    lastSpin = models.DecimalField(max_digits=8, decimal_places=3, null=True)

    def __str__(self):
        return f"{self.color} Ball"

class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)
    putts = models.IntegerField(default=0)
    currentBall = models.OneToOneField(Ball, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Session(models.Model):
    players = models.ManyToManyField(Player, related_name='games')

    def __str__(self):
        return f"Session {self.id}"

class Stat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField()
    putts = models.IntegerField()
    fairways_hit = models.IntegerField()
    greens_in_regulation = models.IntegerField()

    def __str__(self):
        return f"{self.player.name}'s Stats"


