from django.db import models

class Films(models.Model):
    img_film = models.ImageField(upload_to='films/', blank=True, null=True)
    nom_film = models.CharField(max_length=50)
    realisateur = models.CharField(max_length=50)
    date_sortie = models.IntegerField()
    duree = models.IntegerField()
    position = models.PositiveIntegerField(default=0) 

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.nom_film

class Series(models.Model):
    img_serie = models.ImageField(upload_to='series/', blank=True, null=True)
    nom_serie = models.CharField(max_length=50)
    realisateur = models.CharField(max_length=50)
    date_premiere_diffusion = models.IntegerField(blank=True, null=True) 
    nb_saison = models.IntegerField(blank=True, null=True)  
    position = models.PositiveIntegerField(default=0) 

    class Meta:
        ordering = ['position']
    
    def __str__(self):
        return self.nom_serie

class Livres(models.Model):
    img_livre = models.ImageField(upload_to='livres/', blank=True, null=True)
    nom_livre = models.CharField(max_length=50)
    auteur = models.CharField(max_length=50)
    date_sortie = models.IntegerField()

    def __str__(self):
        return self.nom_livre
    
