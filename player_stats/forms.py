from django import forms
from .models import Player, Team, GameStats

class PlayerForm(forms.ModelForm):
    new_team_name = forms.CharField(max_length=100, required=False, label="New Team Name")
    new_team_city = forms.CharField(max_length=100, required=False, label="New Team City")
    new_team_arena = forms.CharField(max_length=100, required=False, label="New Team Arena")

    class Meta:
        model = Player
        fields = ['name', 'team', 'position', 'age']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team'].required = False
        self.fields['team'].label = "Existing Team"

class GameStatsForm(forms.ModelForm):
    class Meta:
        model = GameStats
        fields = ['player', 'date', 'points', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers']