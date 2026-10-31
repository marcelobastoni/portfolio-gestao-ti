"""Calcula os indicadores de incidentes a partir de um CSV no formato de templates/registro-incidentes.csv.

Uso: python calcular_indicadores.py dados-simulados.csv [dias_do_periodo]
"""
import csv
import sys
from datetime import datetime

# Metas em minutos, iguais às de processo.md: (primeira resposta, restauração).
METAS = {"P1": (15, 240), "P2": (30, 480), "P3": (120, 1440), "P4": (480, 4320)}


def minutos(inicio, fim):
    return (datetime.fromisoformat(fim) - datetime.fromisoformat(inicio)).total_seconds() / 60


def formatar(valor):
    horas, resto = divmod(round(valor), 60)
    return f"{horas}h{resto:02d}"


def main(caminho, dias):
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        incidentes = list(csv.DictReader(arquivo))

    print("| Prioridade | Incidentes | MTTA | MTTR | Resposta na meta | Restauração na meta |")
    print("| --- | --- | --- | --- | --- | --- |")
    no_prazo = 0
    for prioridade, (meta_resposta, meta_restauracao) in METAS.items():
        grupo = [i for i in incidentes if i["prioridade"] == prioridade]
        if not grupo:
            continue
        respostas = [minutos(i["abertura"], i["primeira_resposta"]) for i in grupo]
        restauracoes = [minutos(i["abertura"], i["restauracao"]) for i in grupo]
        resposta_ok = sum(valor <= meta_resposta for valor in respostas)
        restauracao_ok = sum(valor <= meta_restauracao for valor in restauracoes)
        no_prazo += sum(
            r <= meta_resposta and t <= meta_restauracao for r, t in zip(respostas, restauracoes)
        )
        print(
            f"| {prioridade} | {len(grupo)} | {formatar(sum(respostas) / len(grupo))} "
            f"| {formatar(sum(restauracoes) / len(grupo))} | {resposta_ok}/{len(grupo)} "
            f"| {restauracao_ok}/{len(grupo)} |"
        )

    total = len(incidentes)
    reabertos = sum(i["reaberto"] == "sim" for i in incidentes)
    indisponibilidade = sum(int(i["indisponibilidade_min"]) for i in incidentes)
    print()
    print(f"- Incidentes no período: {total}")
    print(f"- Conformidade com o SLA (resposta e restauração): {no_prazo}/{total} ({no_prazo / total:.1%})")
    print(f"- Taxa de reabertura: {reabertos}/{total} ({reabertos / total:.1%})")
    print(f"- Disponibilidade do serviço crítico: {1 - indisponibilidade / (dias * 1440):.2%} ({indisponibilidade} min fora do ar)")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 31)
