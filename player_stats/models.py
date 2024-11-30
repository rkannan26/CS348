from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    arena = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self):
        return self.name

class GameStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField()
    points = models.IntegerField()
    rebounds = models.IntegerField()
    assists = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()

    def __str__(self):
        return f"Stats for {self.player.name} on {self.date}"
