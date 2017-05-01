from django.contrib import admin
from models import UserStat, Relation, UserInput, Challenge, Pass


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
	list_display = ['user', 'rounds_played', 'total_score', 'synonyms_index', 'antonyms_index', 'hyponyms_index', 'meronyms_index']


class RelationAdmin(admin.ModelAdmin):
	list_display = ['type', 'base_word', 'input_word', 'in_word_net', 'challenge_accepted']


class UserInputAdmin(admin.ModelAdmin):
	list_display = ['user', 'round_number', 'relation', 'word_score']


class ChallengeAdmin(admin.ModelAdmin):
	list_display = ['user', 'relation', 'sentence', 'is_pending']
	actions = [accept_challenge, deny_challenge]


class PassAdmin(admin.ModelAdmin):
	list_display = ['user', 'base_word', 'type']

admin.site.register(UserStat, UserStatAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(UserInput, UserInputAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Pass, PassAdmin)
