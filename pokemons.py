"""---"""
from dataclasses import dataclass
from functools import partial
from os import path, mkdir
from asyncio import run

from aiometer import run_all
from httpx import AsyncClient, Response
from rich import print
from pandas import DataFrame

from utils.pokes import list_pokes


@dataclass
class Pokemons:
    """_summary_

    Returns:
        _type_: _description_
    """

    _base_url = 'https://pokeapi.co/api/v2'
    _path_here = path.dirname(__file__)

    def __init__(self, pokes: list[str]) -> None:
        """Inicializa a classe Pokemons com uma lista de nomes de Pokémon.

        Args:
            pokes (list[str]): Lista de nomes de Pokémon.
        """
        self._pokes: list[str] = pokes
        self._data: list[dict] = [] # Lista para armazenar os dados coletados

    async def evolucao(self, _poke: str) -> None:
        """Faz requisições assíncronas à API para coletar dados de evolução de um Pokémon específico.

        Args:
            _poke (str): Nome do Pokémon.
        """
        async with AsyncClient(base_url=self._base_url) as client:

            print(f'\n[b][red]-> Primeira requisicao, POKEMON [/]{_poke.upper()}')
            response: Response = await client.get(f'/pokemon/{_poke}')
            data = response.json()
            id_ = data.get('id')

            # Segunda requisição para obter dados da espécie do Pokémon
            print(f'[b][green]-> Segunda resuisicao, ESPECIE DO POKEMON [/]{_poke.upper()}')
            response = await client.get(f'/pokemon-species/{id_}')
            species_data = response.json()
            evolution_chain = species_data.get('evolution_chain').get('url')

            # Terceira requisição para obter detalhes da cadeia de evolução
            print(f'[b][blue]-> Terceira requisicao, DETALHES DA ESPECIE [/]{_poke.upper()}')
            response: Response = await client.get(evolution_chain)
            evolution_data = response.json()

            # Armazenar os dados coletados
            self._data.append({
                'pokemon': _poke,
                'id': id_,
                'species_url': f'/pokemon-species/{id_}',
                'evolution_chain_url': evolution_chain,
                'evolution_details': evolution_data
            })

    async def main(self):
        """Executa as requisições assíncronas para todos os Pokémon na lista.
        """
        result = run_all(
            [partial(self.evolucao, poke) for poke in self._pokes],
            max_at_once=5,
            max_per_second=10
        )
        await result

    def save_to_dataframe(self):
        """Salva os dados coletados em um DataFrame e em um arquivo XLSX.

        Returns:
            _type_: DataFrame contendo os dados coletados.
        """
        _df = DataFrame(self._data)
        if not path.exists(path.join(self._path_here, 'out')):
            mkdir(path.join(self._path_here, 'out'))
        _df.to_excel(path.join(self._path_here, 'out', 'pokemon_data.xlsx'), index=False)
        return _df


if __name__ == '__main__':

    # Uso da classe Pokemons
    pokemons = Pokemons(pokes=list_pokes)
    # Executar as requisições assíncronas
    run(pokemons.main())
    # Salvar os dados em um DataFrame e em um arquivo XLSX
    df = pokemons.save_to_dataframe()
    print(df)
