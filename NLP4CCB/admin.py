from django.contrib import admin
from models import UserStat, Relation, UserInput, Challenge, Pass, CompletedStat, WordStat, ConfirmationStat, ConcretenessStat, PicturesStat


def accept_challenge(modeladmin, request, queryset):
	for challenge in queryset:
		rel_challenges = Challenge.objects.filter(relation=challenge.relation)
		rel_challenges.update(is_pending=False)

		challenge.relation.challenge_accepted = True
		challenge.relation.save()

accept_challenge.short_description = "Accept selected challenges"


def deny_challenge(modeladmin, request, queryset):
	for challenge in queryset:
		rel_challenges = Challenge.objects.filter(relation=challenge.relation)
		rel_challenges.update(is_pending=False)

		challenge.relation.challenge_accepted = False
		challenge.relation.save()

deny_challenge.short_description = "Deny selected challenges"


# Register your models here.
class UserStatAdmin(admin.ModelAdmin):
	list_display = ['user', 'rounds_played', 'total_score', 'synonyms_index', 'antonyms_index', 'hyponyms_index', 'meronyms_index', 'concreteness_index', 'pictures_index', 'last_login']

class WordStatAdmin(admin.ModelAdmin):
	list_display = ['word', 'index', 'sem_rel', 'avg_score', 'rounds_played', 'retired']

class CompletedStatAdmin(admin.ModelAdmin):
	list_display = ['user', 'sem_rel', 'index', 'base_word']

class RelationAdmin(admin.ModelAdmin):
	list_display = ['type', 'base_word', 'input_word', 'in_word_net', 'challenge_accepted']

class ConfirmationStatAdmin(admin.ModelAdmin):
	list_display = ['sem_rel', 'base_word', 'input_word', 'times_confirmed', 'times_rejected']

class ConcretenessStatAdmin(admin.ModelAdmin):
	list_display = ['word', 'index', 'sem_rel', 'avg_score', 'total_score', 'rounds_played']

class PicturesStatAdmin(admin.ModelAdmin):
	list_display = ['word', 'index', 'sem_rel', 'avg_score', 'total_score', 'rounds_played']

class UserInputAdmin(admin.ModelAdmin):
	list_display = ['user', 'round_number', 'relation', 'word_score']


class ChallengeAdmin(admin.ModelAdmin):
	list_display = ['user', 'relation', 'sentence', 'is_pending']
	actions = [accept_challenge, deny_challenge]


class PassAdmin(admin.ModelAdmin):
	list_display = ['user', 'base_word', 'type']

admin.site.register(CompletedStat, CompletedStatAdmin)
admin.site.register(WordStat, WordStatAdmin)
admin.site.register(UserStat, UserStatAdmin)
admin.site.register(ConfirmationStat, ConfirmationStatAdmin)
admin.site.register(ConcretenessStat, ConcretenessStatAdmin)
admin.site.register(PicturesStat, PicturesStatAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(UserInput, UserInputAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Pass, PassAdmin)
