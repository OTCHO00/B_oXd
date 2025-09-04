from django import forms

class add_film(forms.Form):
    img_film = forms.ImageField(
    required=False,
    label="Affiche du film",
    widget=forms.ClearableFileInput(attrs={
        'style': 'display:none;',
        'id': 'id_img_film',
        })
    )
    nom_film = forms.CharField(label="Nom du film", max_length=60)
    realisateur = forms.CharField(label="Nom du réalisateur", max_length=60)
    date_sortie = forms.IntegerField()
    duree = forms.IntegerField()

class add_serie(forms.Form):
    img_serie = forms.ImageField(
        required=False,
        label="",
        widget=forms.ClearableFileInput(attrs={
            'style': 'display:none;',
            'id': 'id_img_serie',
        })
    )
    nom_serie = forms.CharField(label="Nom de la série", max_length=50)
    realisateur = forms.CharField(label="Créateur/Réalisateur", max_length=50)
    date_premiere_diffusion = forms.IntegerField(label="Année de première diffusion", required=False)
    nb_saison = forms.IntegerField(label="Nombre de saisons", required=False)

class add_livre(forms.Form):
    img_livre = forms.ImageField(required=False, label="Couverture du livre")
    nom_livre = forms.CharField(label="Nom du livre", max_length=60)
    auteur = forms.CharField(label="Nom du l'auteur", max_length=60)
    date_sortie = forms.IntegerField() 

