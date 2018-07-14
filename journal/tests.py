from django.test import TestCase
from django.utils import timezone
from datetime import datetime
# Create your tests here.
from journal.models import Kid, Journal


class JournalModelTest(TestCase):

    def test_changes_kid_state(self):
        kid = Kid(photo='nfjngsdlkfngds', name='vasya', birthday=datetime(2010, 1, 1).date(), grade=1)
        kid.save()
        journal = Journal(kid=kid, timestamp=timezone.now(), direction='IN', relative='M')
        journal.save()

        assert kid.is_studying


class KidViewTest(TestCase):

    def test_can_add_and_update(self):
        data = dict(photo='nfjngsdlkfngds', name='vasya', birthday=datetime(2010, 1, 1).date(), grade=1)
        response = self.client.post('/kids/', data=data)

        self.assertRedirects(response, '/kids/1/')

        response = self.client.post('/kids/1/', data={'grade': 2})
        kid = Kid.objects.get(id=1)
        assert kid.grade == 2


class JournalViewTest(TestCase):

    def test_can_add_entries(self):
        kid1 = Kid(photo='nfjngsdlkfngds', name='vasya', birthday=datetime(2010, 1, 1).date(), grade=1)
        kid2 = Kid(photo='nfjngsdlkfngds', name='petya', birthday=datetime(2010, 1, 1).date(), grade=1)

        kid1.save()
        kid2.save()
        response = self.client.post('/journal/1/', data={'relative': 'M'})
        self.assertRedirects(response, '/journal/1/')
        response = self.client.get('/journal/1/')
        assert len(response.json()['data']['items']) == 1

    def test_shows_studying(self):
        kid1 = Kid(photo='nfjngsdlkfngds', name='vasya', birthday=datetime(2010, 1, 1).date(), grade=1)
        kid2 = Kid(photo='nfjngsdlkfngds', name='petya', birthday=datetime(2010, 1, 1).date(), grade=1)

        kid1.save()
        kid2.save()

        self.client.post('/journal/1/', data={'relative': 'M'})
        self.client.post('/journal/2/', data={'relative': 'F'})

        response = self.client.get('/journal/')

        assert len(response.json()['data']['items']) == 2

        self.client.post('/journal/2/', data={'relative': 'F'})
        response = self.client.get('/journal/')

        assert len(response.json()['data']['items']) == 1
