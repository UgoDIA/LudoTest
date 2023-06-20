from django.test import TestCase
from datetime import date
from .models import *


class EditeurModelTests(TestCase):
    def test_editeur_creation(self):
        # Test model creation
        Editeur.objects.create(nom_editeur='Test Editeur')
        self.assertEqual(Editeur.objects.count(), 1)

    def test_editeur_nom_length(self):
        # Test maximum length constraint
        editeur = Editeur(nom_editeur='a' * 51)  # Trying to exceed the maximum length of 50 characters
        with self.assertRaises(Exception):
            editeur.full_clean()

class JeuModelTests(TestCase):
    def test_jeu_creation(self):
        # Test model creation
        editeur = Editeur.objects.create(nom_editeur='Test Editeur')
        Jeu.objects.create(
            nom_jeu='Test Jeu',
            date_publication=date.today(),
            age_min=10,
            joueurs_min=2,
            joueurs_max=4,
            id_editeur=editeur
        )
        self.assertEqual(Jeu.objects.count(), 1)

    def test_jeu_age_min_negative(self):
        # Test minimum age constraint
        editeur = Editeur.objects.create(nom_editeur='Test Editeur')
        jeu = Jeu(
            nom_jeu='Test Jeu',
            date_publication=date.today(),
            age_min=-1,  # Trying to set a negative age
            joueurs_min=2,
            joueurs_max=4,
            id_editeur=editeur
        )
        with self.assertRaises(Exception):
            jeu.full_clean()
            
    def test_joueur_min_greater_than_joueurs_max(self):
        editeur = Editeur.objects.create(nom_editeur='Test Editeur')
        jeu = Jeu(
            nom_jeu='Test Game',
            date_publication='2023-01-01',
            age_min=10,
            joueurs_min=5,
            joueurs_max=3,
            id_editeur=editeur
        )

        with self.assertRaises(ValidationError) as context:
            jeu.full_clean()

        self.assertEqual(
            "{'joueurs_min': ['Minimum number of players cannot be greater than the maximum number of players.']}",
            str(context.exception)
        )
