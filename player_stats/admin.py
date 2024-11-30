from django.contrib import admin
from .models import Player, Team, GameStats

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(GameStats)
