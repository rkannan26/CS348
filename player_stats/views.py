from django.shortcuts import render, redirect, get_object_or_404
from .models import Player, Team
from .forms import PlayerForm, GameStatsForm
from django.db import connection

# View to display all players
def player_list(request):
    players = Player.objects.all()
    return render(request, 'player_list.html', {'players': players})

def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)

            new_team_name = form.cleaned_data.get('new_team_name')
            if new_team_name:
                new_team_city = form.cleaned_data.get('new_team_city')
                new_team_arena = form.cleaned_data.get('new_team_arena')
                team, created = Team.objects.get_or_create(
                    name=new_team_name,
                    defaults={'city': new_team_city, 'arena': new_team_arena}
                )
                player.team = team
            elif not form.cleaned_data.get('team'):
                form.add_error('team', "Please either select an existing team or create a new one.")
                return render(request, 'add_player.html', {'form': form})

            player.save()
            return redirect('player_list')
    else:
        form = PlayerForm()
    return render(request, 'add_player.html', {'form': form})


def edit_player(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('player_list')
    else:
        form = PlayerForm(instance=player)
    return render(request, 'edit_player.html', {'form': form, 'player': player})

def delete_player(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if request.method == 'POST':
        player.delete()
        return redirect('player_list')
    return render(request, 'delete_player.html', {'player': player})


def report_view(request):
    teams = Team.objects.all()
    players = []

    if request.method == 'POST':
        if 'back_to_list' in request.POST:
            return redirect('player_list')

        selected_team = request.POST.get('team')

        with connection.cursor() as cursor:
            query = """
            SELECT p.name, t.name as team_name, p.age, p.position,
                   COALESCE(AVG(gs.points), 0) as avg_points,
                   COALESCE(AVG(gs.rebounds), 0) as avg_rebounds,
                   COALESCE(AVG(gs.assists), 0) as avg_assists,
                   COALESCE(AVG(gs.steals), 0) as avg_steals,
                   COALESCE(AVG(gs.blocks), 0) as avg_blocks,
                   COALESCE(AVG(gs.turnovers), 0) as avg_turnovers
            FROM player_stats_player p
            JOIN player_stats_team t ON p.team_id = t.id
            LEFT JOIN player_stats_gamestats gs ON p.id = gs.player_id
            """
            if selected_team:
                query += "WHERE p.team_id = %s "
                query += "GROUP BY p.id, p.name, t.name, p.age, p.position"
                cursor.execute(query, [selected_team])
            else:
                query += "GROUP BY p.id, p.name, t.name, p.age, p.position"
                cursor.execute(query)

            players = cursor.fetchall()

    return render(request, 'report.html', {'players': players, 'teams': teams})

def add_game_stats(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if request.method == 'POST':
        form = GameStatsForm(request.POST)
        if form.is_valid():
            stats = form.save(commit=False)
            stats.player = player
            stats.save()
            return redirect('player_list')
    else:
        form = GameStatsForm()
    return render(request, 'add_game_stats.html', {'form': form, 'player': player})