# Pokemons Evolution Data Collector

Este projeto é uma aplicação Python para coletar dados de evolução de Pokémons usando a [PokeAPI](https://pokeapi.co/). Ele faz requisições assíncronas para obter informações sobre Pokémons, suas espécies e detalhes da cadeia de evolução, salvando os dados em um arquivo Excel.

## Estrutura do Código

- `Pokemons` - Classe principal para lidar com a coleta de dados.
- `evolucao` - Método assíncrono que faz as requisições para obter os dados de evolução de um Pokémon específico.
- `main` - Método assíncrono que executa as requisições para todos os Pokémons na lista fornecida.
- `save_to_dataframe` - Método que salva os dados coletados em um DataFrame e em um arquivo Excel.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/pokemon-evolution-collector.git
   cd pokemon-evolution-collector
   ```
2. Crie um ambiente virtual e ative-o:
   ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
