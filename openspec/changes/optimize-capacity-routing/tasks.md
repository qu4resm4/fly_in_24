## 1. Planning and baseline

- [x] 1.1 Registrar os turnos atuais dos mapas fornecidos e verificar que a suíte existente continua passando

## 2. Capacity-aware planner

- [x] 2.1 Modelar métricas de custo, capacidade mínima e gargalos de uma rota sem alterar o domínio público
- [x] 2.2 Implementar atribuição incremental baseada em tempo estimado de conclusão e uso previsto
- [x] 2.3 Garantir fallback para a estratégia de menor custo quando não houver candidatos alternativos

## 3. Verification

- [x] 3.1 Adicionar testes de distribuição em bifurcações e gargalos
- [x] 3.2 Executar todos os mapas e comparar turnos com o baseline
- [x] 3.3 Executar `make lint`, testes e `openspec validate --strict`
