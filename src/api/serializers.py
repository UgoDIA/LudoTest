from rest_framework import serializers
from rest_framework import viewsets
from .models import Editeur, Jeu

class JeuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jeu
        fields = '__all__'

class EditeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editeur
        fields = '__all__'
        

class JoinedSerializer(serializers.ModelSerializer):
    nom_editeur = serializers.CharField(source='id_editeur.nom_editeur')

    class Meta:
        model = Jeu
        fields = '__all__'