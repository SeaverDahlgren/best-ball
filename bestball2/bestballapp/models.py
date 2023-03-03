from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Stat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField()
    putts = models.IntegerField()
    fairways_hit = models.IntegerField()
    greens_in_regulation = models.IntegerField()

    def __str__(self):
        return f"{self.player.name}'s Stats"


