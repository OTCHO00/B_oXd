import json
import requests
from django.http import Http404
from django.db.models import Max
from django.shortcuts import render
from django.http import JsonResponse
from .models import Films, Series, Livres
from django.views.generic.edit import FormView
from .forms import add_film, add_serie, add_livre
from django.views.decorators.csrf import csrf_exempt

#FILM

def home(request):
    #recupere tout les films et leur position
    films = Films.objects.all().order_by('position')

    return render(request, 'ratings/home.html', {'films' : films})

@csrf_exempt
def update_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for index, film_id in enumerate(data.get('order', [])):
                Films.objects.filter(id=film_id).update(position=index)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def search_movies(request):
    query = request.GET.get('q', '')
    if len(query) < 3:  
        return JsonResponse({'results': []})
    
    api_key = "f0e8080821e4eb717740c09e73b82b2b"
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
    
    response = requests.get(url)
    data = response.json()
    
    return JsonResponse(data)

def get_movie_details(request, movie_id):
    api_key = "f0e8080821e4eb717740c09e73b82b2b"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits"
    
    response = requests.get(url)
    data = response.json()
    
    # Extraire les infos qu'on veut
    director = None
    for crew_member in data.get('credits', {}).get('crew', []):
        if crew_member.get('job') == 'Director':
            director = crew_member.get('name')
            break
    
    release_year = None
    if data.get('release_date'):
        release_year = data['release_date'][:4] 
    
    result = {
        'director': director,
        'release_year': release_year,
        'runtime': data.get('runtime')
    }
    
    return JsonResponse(result)


def detail(request, id):
    try:
        film = Films.objects.get(id=id)
        return render(request, 'ratings/detail.html', {'film': film})
    except Films.DoesNotExist:
        try:
            serie = Series.objects.get(id=id)
            return render(request, 'ratings/detail.html', {'serie': serie})
        except Series.DoesNotExist:
            raise Http404("Film ou série introuvable")
        

class film_form_view(FormView):
    template_name = "ratings/add.html"
    form_class = add_film
    success_url = "/"

    def form_valid(self, form):

        last_position = Films.objects.aggregate(Max('position'))['position__max']
        if last_position is None:
            last_position = 0

        obj = Films(**form.cleaned_data)
        obj.position = last_position + 1
        obj.save()

        return super().form_valid(form)
    
#SERIE

def serie(request):
    #recupere toutes les séries
    series = Series.objects.all().order_by('position')

    return render(request, "ratings/serie.html", {'series' : series})

@csrf_exempt
def update_order_serie(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for index, serie_id in enumerate(data.get('order', [])):
                Series.objects.filter(id=serie_id).update(position=index)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        

def search_series(request):
    query = request.GET.get('q', '')
    if len(query) < 3:  
        return JsonResponse({'results': []})
    
    api_key = "f0e8080821e4eb717740c09e73b82b2b"
    url = f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={query}"
    
    response = requests.get(url)
    data = response.json()
    
    return JsonResponse(data)

def get_serie_details(request, serie_id):
    api_key = "f0e8080821e4eb717740c09e73b82b2b"
    url = f"https://api.themoviedb.org/3/tv/{serie_id}?api_key={api_key}&append_to_response=credits"

    response = requests.get(url)
    data = response.json()

    # Récupérer le créateur principal
    director = None
    creators = data.get("created_by", [])
    if creators:
        director = creators[0].get("name")
    
    # Récupérer l'année de première diffusion
    first_air_year = None
    if data.get('first_air_date'):
        first_air_year = int(data['first_air_date'][:4])  

    return JsonResponse({
        "director": director,
        "first_air_year": first_air_year,
        "number_of_seasons": data.get('number_of_seasons')
    })

class serie_form_view(FormView):
    template_name = "ratings/add_serie.html"
    form_class = add_serie
    success_url = "/series/"

    def form_valid(self, form):
        obj = Series(**form.cleaned_data)
        obj.save()
        return super().form_valid(form)
    

#LIVRE

def search_books(request):
    query = request.GET.get('q', '')
    if len(query) < 3:  
        return JsonResponse({'results': []})
    
    api_key = "AIzaSyDcChs_c0JPJptZEFaUncy1hAs2D8w74nc"
    url = f"https://www.googleapis.com/books?api_key={api_key}&query={query}"
    
    response = requests.get(url)
    data = response.json()
    
    return JsonResponse(data)

def get_books_details(request, book_id):
    api_key = "AIzaSyDcChs_c0JPJptZEFaUncy1hAs2D8w74nc"
    url = f"https://api.themoviedb.org/3/tv/{book_id}?api_key={api_key}&append_to_response=credits"

    response = requests.get(url)
    data = response.json()

    # Récupérer le créateur principal
    auteur = None
    creators = data.get("Auteur")
    if creators:
        auteur = creators[0].get("name")
    
    # Récupérer l'année de sortie
    release_year = None
    if data.get('release_date'):
        release_year = data['release_date'][:4]  

    return JsonResponse({
        "auteur": auteur,
        "release_year": release_year,
    })

class livre_form_view(FormView):
    template_name = "ratings/add_livre.html"
    form_class = add_livre
    success_url = "/livres/"

    def form_valid(self, form):
        obj = Livres(**form.cleaned_data)
        obj.save()
        return super().form_valid(form)
    
#MANGA

def search_books(request):
    query = request.GET.get('q', '')
    if len(query) < 3:  
        return JsonResponse({'results': []})
    
    api_key = "AIzaSyDcChs_c0JPJptZEFaUncy1hAs2D8w74nc"
    url = f"https://www.googleapis.com/books?api_key={api_key}&query={query}"
    
    response = requests.get(url)
    data = response.json()
    
    return JsonResponse(data)

def get_books_details(request, book_id):
    api_key = "AIzaSyDcChs_c0JPJptZEFaUncy1hAs2D8w74nc"
    url = f"https://api.themoviedb.org/3/tv/{book_id}?api_key={api_key}&append_to_response=credits"

    response = requests.get(url)
    data = response.json()

    # Récupérer le créateur principal
    auteur = None
    creators = data.get("Auteur")
    if creators:
        auteur = creators[0].get("name")
    
    # Récupérer l'année de sortie
    release_year = None
    if data.get('release_date'):
        release_year = data['release_date'][:4]  

    return JsonResponse({
        "auteur": auteur,
        "release_year": release_year,
    })

class livre_form_view(FormView):
    template_name = "ratings/add_livre.html"
    form_class = add_livre
    success_url = "/livres/"

    def form_valid(self, form):
        obj = Livres(**form.cleaned_data)
        obj.save()
        return super().form_valid(form)