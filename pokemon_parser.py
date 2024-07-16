import csv
from pathlib import Path

FORMAT_STR = '\n'.join([
    f'{"Index": <{15}}'': {Index}',
    f'{"Generation": <{15}}'': {Generation}',
    f'{"Name": <{15}}'': {Name}',
    f'{"Type 1": <{15}}'': {Type 1}',
    f'{"Type 2": <{15}}'': {Type 2}',
    f'{"Legendary": <{15}}'': {Legendary}',
    f'{"Total": <{15}}'': {Total}',
    f'{"HP": <{15}}'': {HP}',
    f'{"Attack": <{15}}'': {Attack}',
    f'{"Defense": <{15}}'': {Defense}',
    f'{"Sp. Atk": <{15}}'': {SpAtk}',
    f'{"Sp. Def": <{15}}'': {SpDef}',
    f'{"Speed": <{15}}'': {Speed}',
])
CURRENT_DIR = Path(__file__).parent

with open('Pokemon.csv') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=',')
    pokemons = [row for row in csvreader]


def create_directory_hierarchy():
    generations = set(pokemon['Generation'] for pokemon in pokemons)
    type_1 = set(pokemon['Type 1'] for pokemon in pokemons)
    type_2 = set(pokemon['Type 2'] for pokemon in pokemons)

    for gen in generations:
        for t_1 in type_1:
            for t_2 in type_2:
                Path(CURRENT_DIR / 'Pokedex' / f'Gen {gen}' / t_1 / t_2).mkdir(
                    parents=True,
                    exist_ok=True
                )


def create_pokemon_files():
    for pokemon in pokemons:
        gen = pokemon['Generation']
        t_1 = pokemon['Type 1']
        t_2 = pokemon['Type 2']
        index = pokemon['Index']
        filename = CURRENT_DIR / 'Pokedex' / f'Gen {gen}' / t_1 / t_2 / f'{index}.txt'
        with open(filename, 'w', newline='\n') as pokemon_file:
            pokemon_file.write(FORMAT_STR.format(**pokemon))


if __name__ == "__main__":
    create_directory_hierarchy()
    create_pokemon_files()
