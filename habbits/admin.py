from django.contrib import admin

from habbits.models import Habit, Prize


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('habit_user', 'habit_name', 'habit_is_public', 'habit_owner',)
    list_filter = ('habit_name',)
    search_fields = ('habit_name',)


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ('prize_name',)
    list_filter = ('prize_name',)
    search_fields = ('prize_name',)
