from django.contrib import admin
from models import UserStat, Relation, UserInput, Challenge

# Register your models here.
class UserStatAdmin(admin.ModelAdmin):
    list_display = ['user', 'rounds_played', 'total_score', 'index']

class RelationAdmin(admin.ModelAdmin):
    list_display = ['type', 'base_word', 'input_word', 'in_word_net', 'challenge_accepted']

class UserInputAdmin(admin.ModelAdmin):
    list_display = ['user', 'round_number', 'relation', 'word_score']

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'relation', 'sentence', 'is_pending']

admin.site.register(UserStat, UserStatAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(UserInput, UserInputAdmin)
admin.site.register(Challenge, ChallengeAdmin)