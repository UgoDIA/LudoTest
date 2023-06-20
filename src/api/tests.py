from django.test import TestCase
from datetime import date
from .models import *
from .serializers import JeuSerializer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

#Test des models
class ModelTests(TestCase):
    def setUp(self):
        self.editeur = Editeur.objects.create(nom_editeur='Test Editeur')

    #test création editeur
    def test_editeur_creation(self):
        self.assertEqual(Editeur.objects.count(), 1)


    #test longueur nom editeur
    def test_editeur_nom_length(self):
        editeur = Editeur(nom_editeur='a' * 51) # test avec nom de 51 charactere
        with self.assertRaises(Exception):
            editeur.full_clean()

    #test création jeu
    def test_jeu_creation(self):
        Jeu.objects.create(
            nom_jeu='Test Jeu',
            date_publication=date.today(),
            age_min=10,
            joueurs_min=2,
            joueurs_max=4,
            id_editeur=self.editeur
        )
        self.assertEqual(Jeu.objects.count(), 1)

    # test age min negatif
    def test_jeu_age_min_negatif(self):
        jeu = Jeu(
            nom_jeu='Test Jeu',
            date_publication=date.today(),
            age_min=-1,
            joueurs_min=2,
            joueurs_max=4,
            id_editeur=self.editeur
        )
        with self.assertRaises(Exception):
            jeu.full_clean()

    #test joueurs min plus grand que joueurs max
    def test_joueur_min_joueurs_max(self):
        jeu = Jeu(
            nom_jeu='Test Jeu',
            date_publication=date.today(),
            age_min=10,
            joueurs_min=5,
            joueurs_max=3,
            id_editeur=self.editeur
        )
        with self.assertRaises(ValidationError) as context:
            jeu.full_clean()

        self.assertEqual(str(context.exception), "{'__all__': ['Joueurs min inférieur à joueurs max.']}")

    #test joueurs min negatif
    def test_joueurs_min_negative(self):
        jeu = Jeu(
            nom_jeu='Test Game',
            date_publication=date.today(),
            age_min=10,
            joueurs_min=-1,
            joueurs_max=4,
            id_editeur=self.editeur
        )
        with self.assertRaises(ValidationError):
            jeu.full_clean()

    #test joueurs max negatif
    def test_joueurs_max_negative(self):
        jeu = Jeu(
            nom_jeu='Test Game',
            date_publication=date.today(),
            age_min=10,
            joueurs_min=2,
            joueurs_max=-1,
            id_editeur=self.editeur
        )
        with self.assertRaises(ValidationError):
            jeu.full_clean()

#Test des opérations CRUD
class JeuCrudTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('JeuViewset-list')
        self.editeur = Editeur.objects.create(nom_editeur='Test Editeur')
        
    #test post   
    def test_create_jeu(self):
        data = {
            'nom_jeu': 'Test Jeu',
            'date_publication': '2023-01-01',
            'age_min': 10,
            'joueurs_min': 2,
            'joueurs_max': 4,
            'id_editeur': self.editeur.id_editeur  # Assuming there is an Editeur instance with primary key 1
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Jeu.objects.count(), 1)
        jeu = Jeu.objects.get(pk=1)
        self.assertEqual(jeu.nom_jeu, 'Test Jeu')

    #test get
    def test_get_jeu(self):
        editeur = Editeur.objects.create(nom_editeur='Test Editeur')
        jeu = Jeu.objects.create(
            nom_jeu='Test Jeu',
            date_publication=date.today(),
            age_min=10,
            joueurs_min=2,
            joueurs_max=4,
            id_editeur=editeur
        )

        response = self.client.get(reverse('JeuViewset-detail', args=[jeu.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = JeuSerializer(jeu)
        self.assertEqual(response.data, serializer.data)

    #test update
    def test_update_jeu(self):
        jeu = Jeu.objects.create(
            nom_jeu='Original Jeu',
            date_publication=date.today(),
            age_min=10,
            joueurs_min=2,
            joueurs_max=4,
            id_editeur=self.editeur
        )

        data = {
            'nom_jeu': 'Updated Jeu',
            'date_publication': '2023-01-01',
            'age_min': 12,
            'joueurs_min': 3,
            'joueurs_max': 5,
            'id_editeur': self.editeur.id_editeur
        }
        response = self.client.put(reverse('JeuViewset-detail', args=[jeu.pk]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        jeu.refresh_from_db()

        self.assertEqual(jeu.nom_jeu, 'Updated Jeu')
        self.assertEqual(jeu.age_min, 12)
        self.assertEqual(jeu.joueurs_min, 3)
        self.assertEqual(jeu.joueurs_max, 5)

    #test du delete
    def test_delete_jeu(self):
        jeu = Jeu.objects.create(
            nom_jeu='Test Jeu',
            date_publication=date.today(),
            age_min=10,
            joueurs_min=2,
            joueurs_max=4,
            id_editeur=self.editeur
        )

        response = self.client.delete(reverse('JeuViewset-detail', args=[jeu.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Jeu.objects.count(), 0)
