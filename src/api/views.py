from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
# Create your views here.

class JeuViewset(viewsets.ModelViewSet):
    queryset = Jeu.objects.all()
    serializer_class = JeuSerializer


class EditeurViewset(viewsets.ModelViewSet):
    queryset = Editeur.objects.all()
    serializer_class = EditeurSerializer
    
class JoinedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JoinedSerializer
    queryset = Jeu.objects.select_related('id_editeur').all()  

