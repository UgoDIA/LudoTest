from rest_framework import serializers
from .models import Editeur, Jeu

class JeuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jeu
        fields = '__all__'

class EditeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editeur
        fields = '__all__'