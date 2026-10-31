# Simulação: falha de conectividade em uma unidade

> **Exercício simulado.** O cenário, a organização, os horários e os números são fictícios e foram criados para demonstrar a aplicação do [processo](processo.md). Este documento não descreve um evento real nem apresenta resultados obtidos em uma organização.

## Contexto
Uma organização fictícia opera 24 horas e tem uma unidade que depende de um sistema central, acessado pela rede corporativa. A unidade possui dois links de internet, com failover automático previsto para o caso de queda do principal.

## Situação
Às 07:42, no início do turno, o monitoramento alerta que a unidade perdeu a comunicação. Pouco depois, usuários relatam que o sistema central não abre. O link principal caiu, e o link secundário está ativo, mas não assumiu o tráfego.

## Classificação
| Critério | Avaliação | Justificativa |
| --- | --- | --- |
| Impacto | Alto | Sistema crítico indisponível para toda a unidade |
| Urgência | Alta | O atendimento do turno é afetado de imediato e a fila cresce a cada minuto |
| **Prioridade** | **P1** | Metas: resposta em 15 min e restauração em 4 h |

## Linha do tempo
| Horário | Tempo decorrido | Ação |
| --- | --- | --- |
| 07:42 | 0 min | Alerta do monitoramento e abertura do incidente |
| 07:49 | 7 min | Responsável de plantão assume; incidente classificado como P1 |
| 07:55 | 13 min | Sala de crise aberta; áreas afetadas orientadas a iniciar o procedimento manual |
| 08:05 | 23 min | Diagnóstico: link principal fora do ar e failover automático sem atuar |
| 08:10 | 28 min | Chamado aberto na operadora do link principal |
| 08:25 | 43 min | Primeira atualização periódica às áreas afetadas |
| 08:55 | 73 min | Decisão: redirecionar o tráfego manualmente para o link secundário |
| 09:26 | 104 min | Tráfego no link secundário e sistema validado pelos usuários; serviço restaurado |

O link principal voltou mais tarde, e o retorno foi feito em uma janela combinada, para evitar nova interrupção durante o turno.

## Decisões de gestão
- **Restaurar antes de investigar:** usar o link disponível, sem aguardar a operadora nem explicar por completo a falha do failover.
- **Comunicar desde o início:** as áreas ativaram o procedimento manual antes de haver diagnóstico, reduzindo o impacto.
- **Planejar o retorno:** voltar ao link principal assim que ele subisse causaria outra interrupção em horário de pico.

## Análise pós-incidente
**Causa imediata:** interrupção no link principal, na operadora.

**Por que a unidade ficou fora do ar, mesmo com um segundo link?**
1. O failover não atuou.
2. A regra de roteamento havia sido alterada em uma manutenção e não previa mais o desvio.
3. A mudança não incluiu um teste de failover ao final.
4. Não existia teste periódico de contingência para os links.

**Causa raiz:** a contingência era presumida, não verificada. A falha da operadora iniciou o incidente, mas a duração da parada veio da falha do processo interno.

| Ação | Tipo | Responsável | Prazo |
| --- | --- | --- | --- |
| Corrigir a regra de roteamento e testar o failover | Corretiva | Infraestrutura | 2 dias |
| Incluir teste de failover nas mudanças de rede | Preventiva | Gestão de mudanças | 15 dias |
| Criar teste semestral de contingência dos links | Preventiva | Infraestrutura | 30 dias |
| Alertar quando o link secundário estiver sem capacidade de assumir | Detecção | Monitoramento | 30 dias |
| Revisar o SLA e o processo de acionamento da operadora | Fornecedor | Coordenação de TI | 45 dias |

## Painel do mês simulado
Calculado com [`calcular_indicadores.py`](calcular_indicadores.py) sobre os [12 incidentes fictícios](dados-simulados.csv) de um mês, entre eles este P1 (`SIM-006`).

| Prioridade | Incidentes | MTTA | MTTR | Resposta na meta | Restauração na meta |
| --- | --- | --- | --- | --- | --- |
| P1 | 1 | 0h07 | 1h44 | 1/1 | 1/1 |
| P2 | 3 | 0h22 | 4h52 | 2/3 | 3/3 |
| P3 | 5 | 1h13 | 15h40 | 4/5 | 4/5 |
| P4 | 3 | 2h40 | 28h10 | 3/3 | 3/3 |

| Indicador | Resultado | Meta de referência | Situação |
| --- | --- | --- | --- |
| Conformidade com o SLA | 9/12 (75,0%) | ≥ 90% | Abaixo |
| Taxa de reabertura | 1/12 (8,3%) | ≤ 5% | Acima |
| Disponibilidade do serviço crítico | 99,77% (104 min fora do ar) | ≥ 99,9% | Abaixo |

## Leitura gerencial
- **O P1 cumpriu o SLA, e mesmo assim a disponibilidade ficou abaixo da meta.** Estar dentro do prazo de restauração não significa que o resultado foi aceitável: a meta de 99,9% permite cerca de 45 minutos no mês, e uma única parada durou mais que o dobro disso. A prioridade é fazer o failover funcionar, não acelerar a equipe.
- **A falha de SLA em P2 foi na resposta, fora do horário comercial** (`SIM-008`, 37 min às 21:15). Vale avaliar o processo de acionamento do plantão antes de pedir mais pessoas.
- **Com apenas 12 incidentes, um caso muda o percentual em mais de 8 pontos.** A decisão deve considerar a tendência de vários meses, não um único fechamento.

## O que este exercício demonstra
Uso de critérios objetivos de priorização, coordenação da crise, comunicação às áreas, análise de causa raiz focada em processo e leitura de indicadores para orientar decisões.
