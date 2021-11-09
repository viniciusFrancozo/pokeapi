from django.shortcuts import render
from .forms import PokeForm
import requests


# Create your views here.
def index(request):
    form = PokeForm(request.POST)
    context = {'form': form, 'sprites': {}, 'names': {}, 'origin': {}, 'stats': {}, 'statcolours': {
        '#F57155': '#F3937F',
        '#F79040': '#F5B17C',
        '#EEE83F': '#F1ED72',
        '#349FEE': '#6CB7EF',
        '#7FF03A': '#A4F075',
        '#FF5DE7': '#FE93EE'
    }, 'success': False}
    poketwo = ''
    pokethree = ''
    if request.method == 'POST':
        if form.is_valid():
            pokemon_name = form.cleaned_data['pokemon']
            response_poke1 = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}')
            if response_poke1.status_code == 200:
                context['success'] = True
                poke1_json = response_poke1.json()
                context['origin']['sprite'] = poke1_json['sprites']['other']['official-artwork']['front_default']
                context['origin']['name'] = poke1_json['name']
                for i in poke1_json['stats']:
                    context['stats'][i['stat']['name'].replace('special-', 'SP ').upper()] = i['base_stat']
                context['names']['name1'] = poke1_json['name']
                response_species = requests.get(poke1_json['species']['url'])
                evo_chain = requests.get(response_species.json()['evolution_chain']['url'])
                poke_root = evo_chain.json()['chain']['species']['name']
                try:
                    if evo_chain.json()['chain']['evolves_to'][0]:
                        poketwo = evo_chain.json()['chain']['evolves_to'][0]['species']['name']
                        context['names']['name2'] = poketwo
                    if evo_chain.json()['chain']['evolves_to'][0]['evolves_to']:
                        pokethree = evo_chain.json()['chain']['evolves_to'][0]['evolves_to'][0]['species']['name']
                        context['names']['name3'] = pokethree
                except IndexError:
                    pass

                context['form'] = form
                context['sprites']['sprite1'] = poke1_json['sprites']['other']['official-artwork']['front_default']

                if poke_root != poke1_json['name']:
                    response_pokeroot = requests.get(f'https://pokeapi.co/api/v2/pokemon/{poke_root.lower()}')
                    pokeroot_json = response_pokeroot.json()
                    context['names']['name1'] = pokeroot_json['name']
                    context['sprites']['sprite1'] = pokeroot_json['sprites']['other']['official-artwork']['front_default']
                if poketwo:
                    response_poke2 = requests.get(f'https://pokeapi.co/api/v2/pokemon/{poketwo.lower()}')
                    poke2_json = response_poke2.json()
                    context['sprites']['sprite2'] = poke2_json['sprites']['other']['official-artwork']['front_default']
                if pokethree:
                    response_poke3 = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokethree.lower()}')
                    poke3_json = response_poke3.json()
                    context['sprites']['sprite3'] = poke3_json['sprites']['other']['official-artwork']['front_default']

            else:
                context['success'] = False
    else:
        form = PokeForm()
        context['form'] = form
        context['success'] = False
    return render(request, 'index.html', context)
