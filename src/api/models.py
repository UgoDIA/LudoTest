from django.db import models

# Create your models here.

class Editeur(models.Model):
    id_editeur = models.AutoField(primary_key=True)
    nom_editeur = models.CharField(max_length=50)

    class Meta:
        db_table = 'editeur'


class Jeu(models.Model):
    id_jeu = models.AutoField(primary_key=True)
    nom_jeu = models.CharField(max_length=50)
    date_publication = models.DateField()
    age_min = models.IntegerField()
    joueurs_min = models.IntegerField()
    joueurs_max = models.IntegerField()
    id_editeur = models.ForeignKey(Editeur, models.DO_NOTHING, db_column='id_editeur')

    class Meta:

        db_table = 'jeu'
