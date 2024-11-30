from django.urls import path
from . import views
from .views import edit_player, delete_player, report_view

urlpatterns = [
    path('', views.player_list, name='player_list'),
    path('add/', views.add_player, name='add_player'),
    path('edit/<int:player_id>/', edit_player, name='edit_player'),
    path('delete/<int:player_id>/', delete_player, name='delete_player'),
    path('report/', report_view, name='report_view'),
    path('add_stats/<int:player_id>/', views.add_game_stats, name='add_game_stats'),
]
