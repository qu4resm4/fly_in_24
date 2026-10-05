## Context

O simulador possui parser, grafo, planejador, motor de turnos e visualização terminal. Os mapas fornecem coordenadas inteiras, cores, tipos de zona e capacidades, enquanto o motor pode produzir uma sequência de turnos com movimentos e ocupações. A nova interface deve consumir esses dados, mas não executar decisões de roteamento.

## Goals / Non-Goals

**Goals:**

- Criar uma janela 2D clara para apresentar a simulação.
- Separar estado da simulação e widgets gráficos.
- Permitir controle manual e automático dos frames.
- Reutilizar as coordenadas e cores já presentes nos mapas.
- Manter execução headless para testes e avaliadores automáticos.

**Non-Goals:**

- Não usar a biblioteca gráfica para construir ou resolver o grafo.
- Não alterar o algoritmo de roteamento nesta mudança.
- Não adicionar servidor web ou interface remota.
- Não exigir que a GUI seja usada nos testes unitários do motor.

## Decisions

### PySide6 e Qt Graphics View

Será usado PySide6 com `QGraphicsScene` e `QGraphicsView`. A cena conterá itens próprios para zonas, conexões e drones, permitindo zoom e navegação. Pygame-ce foi considerado, mas exigiria implementar manualmente mais componentes de interface; Tkinter foi considerado mais simples, porém menos flexível para uma apresentação visual rica.

### Frames imutáveis de apresentação

O motor fornecerá uma sequência ou iterador de frames contendo turno, movimentos, posições e capacidades. A GUI consumirá esses frames e não modificará diretamente o estado interno do motor. Isso permite testar a GUI com frames artificiais e manter o modo terminal intacto.

### Timer controlado pela janela

Um `QTimer` aplicará frames em intervalos configuráveis. Play e pause controlam o timer; avanço manual aplica somente um frame; reset reconstrói o estado visual inicial. Nenhum `sleep` será usado na thread principal.

### Coordenação de coordenadas

As coordenadas do mapa serão convertidas para pixels por uma transformação com escala, margem e inversão opcional do eixo vertical. O cálculo ficará isolado no adaptador visual para não alterar as coordenadas do domínio.

### Dependência opcional

PySide6 será documentado como dependência da interface. Imports da GUI ficarão em módulos separados e o CLI só os carregará quando `--gui` for solicitado. Assim, parser, simulador e testes headless continuam funcionando sem Qt.

## Risks / Trade-offs

- [PySide6 aumenta o tamanho da instalação] → mantê-lo opcional e documentar instalação no ambiente virtual.
- [Diferenças de suporte gráfico entre sistemas] → testar primeiro macOS, manter fallback terminal e evitar recursos específicos de plataforma.
- [Muitos drones sobrepostos] → usar deslocamento visual determinístico ou agrupamento por zona.
- [GUI divergir do estado real] → atualizar exclusivamente a partir de frames produzidos pelo motor.
- [Animação interromper a responsividade] → usar `QTimer` e nunca bloquear o event loop.

## Migration Plan

1. Criar o modelo de frame e um adaptador que transforme a simulação em frames.
2. Adicionar itens gráficos para zonas, conexões e drones.
3. Adicionar janela, painel de informações e controles.
4. Adicionar a flag `--gui` e tratamento de dependência ausente.
5. Testar headless, smoke test da GUI e execução manual com mapas Easy e Medium.

Rollback consiste em executar o CLI sem `--gui` ou remover a dependência PySide6; o motor terminal permanece inalterado.

## Open Questions

Nenhuma.
