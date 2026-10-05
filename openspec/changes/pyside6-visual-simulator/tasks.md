## 1. Presentation contract

- [x] 1.1 Criar o modelo tipado de frame de apresentação e verificar que ele contém turno, movimentos, posições e capacidades
- [x] 1.2 Adaptar a simulação para produzir frames sem alterar a saída oficial; verificar com a suíte headless existente

## 2. PySide6 scene

- [x] 2.1 Adicionar PySide6 como dependência opcional documentada e verificar instalação no ambiente virtual
- [x] 2.2 Implementar transformação de coordenadas e itens visuais de zonas/conexões; verificar com smoke test PySide6 em backend `offscreen`
- [x] 2.3 Implementar itens visuais de drones, trânsito restrito, cores e ocupação; verificar com smoke test PySide6 em backend `offscreen`

## 3. Interactive window

- [x] 3.1 Implementar janela principal com cena, painel de detalhes e contador de turnos; verificar com smoke test PySide6 em backend `offscreen`
- [x] 3.2 Implementar play, pause, próximo turno, reset e controle de velocidade com `QTimer`; verificar avanço e reset no smoke test PySide6
- [x] 3.3 Adicionar `--gui` e erro controlado quando PySide6 não estiver instalado; verificar que o CLI sem `--gui` permanece headless

## 4. Verification and documentation

- [x] 4.1 Criar testes headless para frames, transformação de coordenadas e formatação de detalhes
- [x] 4.2 Executar `make lint`, testes e os mapas Easy/Medium; verificar que a GUI não altera o resultado da simulação
- [x] 4.3 Atualizar README com instalação, comando `--gui`, controles e limitações conhecidas
