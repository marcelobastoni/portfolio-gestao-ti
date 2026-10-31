# Indicadores de desempenho

Um indicador só tem valor se levar a uma decisão. Por isso, cada um abaixo vem com o que observar e com o risco de interpretá-lo isoladamente.

| Indicador | Fórmula | Meta de referência | O que revela | Cuidado na leitura |
| --- | --- | --- | --- | --- |
| **MTTA**: tempo médio de primeira resposta | Soma de (primeira resposta − abertura) ÷ nº de incidentes | Conforme o SLA de cada prioridade | Capacidade de triagem e de plantão | Resposta automática não conta como atendimento |
| **MTTR**: tempo médio de restauração | Soma de (restauração − abertura) ÷ nº de incidentes | Conforme o SLA de cada prioridade | Eficácia da restauração | Sempre separar por prioridade: a média geral esconde os casos críticos |
| **Conformidade com o SLA** | Incidentes dentro das metas de resposta e de restauração ÷ total | ≥ 90% | Cumprimento do que foi acordado | Pode ser inflada por reclassificação; auditar mudanças de prioridade |
| **Taxa de reabertura** | Incidentes reabertos ÷ total | ≤ 5% | Qualidade da solução | Alta pressão por encerrar costuma elevar este número |
| **Disponibilidade do serviço crítico** | 1 − (minutos fora do ar ÷ minutos do período) | ≥ 99,9% | Experiência real da operação | Acompanhar por serviço e, se possível, pelo monitoramento, não só por chamados |
| **Backlog por idade** | Incidentes abertos por faixa de tempo | Tendência estável ou de queda | Capacidade da equipe frente à demanda | Um pico pode indicar um problema único, não falta de capacidade |
| **Recorrência** | Incidentes com a mesma causa ÷ total | Tendência de queda | Eficácia da gestão de problemas | Exige categorização consistente |
| **Ações pós-incidente no prazo** | Ações concluídas no prazo ÷ ações com prazo vencido no período | ≥ 85% | Se a melhoria realmente acontece | Priorizar ações que eliminam causas, não só as fáceis |

As metas são pontos de partida e devem ser ajustadas ao risco do negócio. Comparar com o histórico da própria operação costuma dizer mais do que um número genérico.

## Rotina de acompanhamento
| Frequência | Fórum | Foco |
| --- | --- | --- |
| Diária | Equipe de operação | Incidentes abertos, riscos de vencimento e P1/P2 do dia anterior |
| Mensal | Coordenação e áreas de negócio | Tendências, SLA, recorrências e plano de ação |
| Trimestral | Diretoria | Disponibilidade, riscos, resultados de testes de contingência e investimentos |

## Como calcular
O [script](calcular_indicadores.py) usa apenas a biblioteca padrão do Python e lê um CSV no formato do [modelo de registro](../templates/registro-incidentes.csv):

```bash
python calcular_indicadores.py dados-simulados.csv 31
```

O segundo argumento é o número de dias do período. O resultado com os dados de exemplo está na [simulação](simulacao-falha-conectividade.md#painel-do-mês-simulado).
