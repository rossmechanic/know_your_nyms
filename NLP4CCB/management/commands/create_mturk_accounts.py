from django.core.management.base import BaseCommand
import re
from passgen import passgen
from django.contrib.auth.models import User


class Command(BaseCommand):
	help = 'Adds n mturk accounts to the database and creates a csv of those usernames and passwords'

	def add_arguments(self, parser):
		parser.add_argument('num_turkers', nargs='+', type=int)

		parser.add_argument(
			'--filename',
			dest='filename',
			default='turkers.csv',
			help='Specify a file name to store usernames and password. Default=turkers.csv'
		)

	def handle(self, *args, **options):
		max_turk_num = 0
		for user in User.objects.filter(username__regex=r'^mturk(\d+)'):
			turk_num = int(re.search(r'^mturk(\d+)', str(user)).group(1))
			if turk_num > max_turk_num:
				max_turk_num = turk_num

		max_turk_num += 1

		output_csv_string = 'Username,Password\n'
		for i in range(max_turk_num, max_turk_num + options['num_turkers'][0]):
			username = 'mturk' + str(i)
			password = passgen(length=12, punctuation=False, digits=True, case='both')
			user = User.objects.create(username=username)
			user.set_password(password)
			user.save()
			output_csv_string += username + ',' + password + '\n'

		with open(options['filename'], 'a') as f:
			f.write(output_csv_string)
