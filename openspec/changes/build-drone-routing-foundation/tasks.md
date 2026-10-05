## 1. Project setup

- [x] 1.1 Criar `pyproject.toml`, `.gitignore`, `Makefile`, `README.md` e a estrutura `src/`/`tests/`; verificar que os comandos documentados são reconhecidos
- [x] 1.2 Configurar execução de `flake8` e `mypy` para Python 3.10+; verificar com `make lint` usando o ambiente virtual Python 3.12

## 2. Map input and domain

- [x] 2.1 Implementar os objetos de zona, conexão, drone e grafo com tipos e docstrings; verificar importação e testes unitários básicos
- [x] 2.2 Implementar o parser de mapas, comentários, metadados padrão e conexões bidirecionais; verificar com todos os mapas Easy
- [x] 2.3 Implementar validações de declarações ausentes, duplicatas, capacidades inválidas, tipos desconhecidos e referências inexistentes; verificar mensagens com linha e causa

## 3. Routing and simulation

- [x] 3.1 Implementar busca de rotas ponderadas, excluindo zonas bloqueadas e priorizando zonas priority; verificar caminhos lineares, bifurcações, loops e becos sem saída
- [x] 3.2 Implementar planejamento de múltiplos drones com distribuição de rotas e espera; verificar que nenhum mapa produz conflito de capacidade
- [x] 3.3 Implementar o motor de simulação por turnos com atualização em duas fases e encerramento após a última entrega; verificar os mapas Easy e Medium
- [x] 3.4 Implementar travessias de dois turnos para zonas restricted; verificar chegada obrigatória e saída que representa a conexão durante o trânsito
- [x] 3.5 Executar os mapas Hard e medir quantidade de turnos; registrar limitações de desempenho sem alterar a validade dos movimentos

## 4. Output and visualization

- [x] 4.1 Implementar o formato oficial de saída por turnos, omitindo drones parados; verificar a saída contra os exemplos do enunciado
- [x] 4.2 Implementar `--visual` com cores, mapa legível e posições dos drones; verificar funcionamento com cores conhecidas e desconhecidas
- [x] 4.3 Implementar `--capacity-info` com ocupação atual e capacidade máxima de zonas e conexões; verificar demonstração em um mapa com gargalo

## 5. Verification and documentation

- [x] 5.1 Criar testes de parser, grafo, rotas, capacidades, movimentos restritos, saída e casos desconectados; verificar execução completa da suíte
- [x] 5.2 Executar `make lint`, testes e todos os mapas fornecidos; corrigir erros de tipagem, estilo e simulação
- [x] 5.3 Completar o README com descrição, instruções, algoritmo, visualização, estrutura e exemplo de entrada/saída; verificar leitura por um usuário novo
