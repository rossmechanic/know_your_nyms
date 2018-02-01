from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
import unittest
from django.core.urlresolvers import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.auth.models import AnonymousUser, User
from .views import *
# Create your tests here.

class TestConcretenessPictures(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user('admin', 'foo@foo.com', 'admin')

	# test that the connection works
	def test_models_connection(self):
		response = self.client.post('/models/')
		self.assertEqual(response.status_code, 200)

	# test the page uses the right html page for meronym
	def test_meronyms_html(self):
		self.client.login(username='admin', password='admin')
		session = self.client.session
		session['relationships'] = ["meronyms"]
		session.save()
		response = self.client.get('/models/')
		self.assertTemplateUsed(response, "input_words.html")

	# test if we select concreteness game the app actually takes us to that page
	def test_concreteness_html(self):
		self.client.login(username='admin', password='admin')
		session = self.client.session
		session['relationships'] = ["concreteness"]
		session.save()
		response = self.client.get('/models/')
		self.assertTemplateUsed(response, "input_concreteness.html")

	# test if we select pictures game the app actually takes us to that page
	def test_pictures_html(self):
		self.client.login(username='admin', password='admin')
		session = self.client.session
		session['relationships'] = ["pictures"]
		session.save()
		response = self.client.get('/models/')
		self.assertTemplateUsed(response, "input_pictures.html")

	# test the meronym game page contains the right info
	def test_meronyms_contains(self):
		self.client.login(username='admin', password='admin')
		session = self.client.session
		session['relationships'] = ["meronyms"]
		session.save()
		response = self.client.get('/models/')
		self.assertContains(response, "parts")

	# tes the concreteness game page contains the right info
	def test_concreteness_contains(self):
		self.client.login(username='admin', password='admin')
		session = self.client.session
		session['relationships'] = ["concreteness"]
		session.save()
		response = self.client.get('/models/')
		self.assertContains(response, "concreteness")

	# test the pictures game page contains the right info
	def test_pictures_contains(self):
		self.client.login(username='admin', password='admin')
		session = self.client.session
		session['relationships'] = ["pictures"]
		session.save()
		response = self.client.get('/models/')
		self.assertContains(response, "picture")

	# test the scoring page for the meronym game exists
	def test_scoring_meronym_link(self):
		response = self.client.post('/models/scoring/', {"sem_rel": "meronyms", "base_word": "sphere", "word_index":2, "form-TOTAL_FORMS":2, "form-0-word":"circle", "form-1-word":"round"})
		self.assertEqual(response.status_code, 200)

	# test the scoring page for the meronym game loads the correct page
	def test_scoring_meronym_page(self):
		response = self.client.post('/models/scoring/', {"sem_rel": "meronyms", "base_word": "sphere", "word_index":2, "form-TOTAL_FORMS":2, "form-0-word":"circle", "form-1-word":"round"})
		self.assertTemplateUsed(response, "scoring.html")

	# test the scoring page for the concreteness game exists
	def test_scoring_concreteness_link(self):
		response = self.client.post('/models/concreteness_scoring/', {"sem_rel": "concreteness", "results": "[]", "results_index": "[]"})
		self.assertEqual(response.status_code, 200)

	# test the scoring page for the concreteness game loads the correct page
	def test_scoring_concreteness_page(self):
		response = self.client.post('/models/concreteness_scoring/', {"sem_rel": "concreteness", "results": "[]", "results_index": "[]"})
		self.assertTemplateUsed(response, "concreteness_scoring.html")

	# test the scoring page for the pictures game exists
	def test_scoring_pictures_link(self):
		response = self.client.post('/models/pictures_scoring/', {"sem_rel": "pictures", "results": "[]", "results_index": "[]"})
		self.assertEqual(response.status_code, 200)

	# test the scoring page for the pictures game loads the correct page
	def test_scoring_pictures_page(self):
		response = self.client.post('/models/pictures_scoring/', {"sem_rel": "pictures", "results": "[]", "results_index": "[]"})
		self.assertTemplateUsed(response, "pictures_scoring.html")
