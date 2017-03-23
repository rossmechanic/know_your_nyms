from django.contrib import admin
from models import UserStat, Relation, UserInput

# Register your models here.
class UserStatAdmin(admin.ModelAdmin):
    list_display = ['user', 'rounds_played', 'total_score']

class RelationAdmin(admin.ModelAdmin):
    list_display = ['type', 'base_word', 'input_word', 'word_net_score', 'model_score']

class UserInputAdmin(admin.ModelAdmin):
    list_display = ['user', 'round_number', 'round_time', 'relation', 'word_score', 'challenge']

admin.site.register(UserStat, UserStatAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(UserInput, UserInputAdmin)