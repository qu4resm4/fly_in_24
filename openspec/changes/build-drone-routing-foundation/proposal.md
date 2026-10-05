## Why

O repositório contém o enunciado e os mapas, mas ainda não possui uma implementação capaz de interpretar uma rede, planejar rotas ou simular os drones. Esta mudança cria uma primeira fundação verificável, alinhada aos critérios de avaliação, para que a implementação possa evoluir com segurança para os mapas mais complexos.

## What Changes

- Criar um parser para mapas Fly-in, incluindo metadados, comentários e mensagens de erro com linha e causa.
- Criar o modelo orientado a objetos de zonas, conexões, drones e grafo customizado.
- Implementar busca de rotas considerando tipos de zona, zonas bloqueadas e capacidades.
- Implementar simulação discreta por turnos com movimentos simultâneos, espera e movimentação restrita de dois turnos.
- Implementar saída oficial por turnos e visualização opcional colorida no terminal.
- Adicionar a opção `--capacity-info` para exibir ocupação de zonas e conexões.
- Adicionar testes, `README.md`, `Makefile`, `.gitignore` e configuração de tipagem e lint.

## Capabilities

### New Capabilities

- `map-input`: leitura e validação dos arquivos de mapas Fly-in.
- `drone-routing`: planejamento de rotas e simulação de drones sob restrições de capacidade e tempo.
- `terminal-visualization`: saída oficial, visualização colorida e relatório de capacidades.

### Modified Capabilities

Nenhuma.

## Impact

- Novos módulos Python sob `src/` e testes sob `tests/`.
- Novos comandos de execução e validação no `Makefile`.
- Nenhuma dependência de biblioteca de grafos; a representação do grafo será própria.
- O modo padrão deverá permanecer compatível com o formato de saída exigido pelo avaliador.
