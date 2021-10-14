from django.shortcuts import render
from .forms import PokeForm
import requests


# Create your views here.
def index(request):
    form = PokeForm(request.POST)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            pokemon = form.cleaned_data['pokemon']
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}')
            if response.status_code == 200:
                poke_json = response.json()
                context = {
                    'sprite': poke_json['sprites']['other']['official-artwork']['front_default'],
                    'name': poke_json['name'],
                    'form': form,
                    'success': True
                }
            else:
                context['success'] = False
    else:
        form = PokeForm()
        context['form'] = form
        context['success'] = False
    return render(request, 'index.html', context)
