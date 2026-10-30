# -*- coding: utf-8 -*-
"""``triton estudo``: o subcomando de estudos em lote por JSON (``estudo.json``).

A lógica fica em :mod:`triton.core.estudo`; aqui só estão os argumentos, as mensagens e os códigos de saída.
Em ``cli.py`` o subcomando só é registrado (``registrar``) e despachado (``executar``).

Códigos de saída: 0 tudo certo; 1 algum caso do estudo falhou (as saídas dos demais foram gravadas);
2 estudo ou argumentos inválidos (como nos demais subcomandos).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Callable, List, Optional

from triton import cli_progresso as PR
from triton.cli_textos import t as _t
from triton.core import estudo as E
from triton.core import estudo_consolidar as C

#: As ações do subcomando, na ordem em que a ajuda as mostra.
ACOES = ("init", "validate", "run", "resumo", "lote", "consolidar", "texto", "esquema", "apelidos")


def _inteiro_positivo(bruto: str) -> int:
    try:
        v = int(bruto)
        if v > 0:
            return v
    except ValueError:
        pass
    raise argparse.ArgumentTypeError(_t("Informe um inteiro positivo."))


def _tipologia(bruto: str) -> str:
    canon = E.tipologia_canonica(bruto)
    if canon is None or canon == E.TIPOLOGIA_OUTRA:
        raise argparse.ArgumentTypeError(_t("tipologia desconhecida: {0}. Use: {1}").format(bruto, ", ".join(E.TIPOLOGIAS)))
    return canon


def registrar(subparsers: Any) -> None:
    """Acrescenta ``estudo`` (e suas ações) ao analisador principal da CLI."""
    estudo = subparsers.add_parser(
        "estudo", help="Estudos em lote por JSON: organiza, executa e relata vários edifícios (tabelas para artigos)",
        description="Estudos em lote por JSON. Um estudo.json reúne projeto base, casos, substituições de parâmetros, "
                    "análise e saídas; o programa executa todos os casos e escreve CSV, JSON, Markdown, LaTeX e XLSX.")
    acoes = estudo.add_subparsers(dest="estudo_acao", required=True, metavar="{" + ",".join(ACOES) + "}")

    def nova(nome: str, ajuda: str):
        return acoes.add_parser(nome, help=_t(ajuda), description=_t(ajuda))

    p = nova("init", "Cria a pasta do estudo com um estudo.json esqueleto (sem valores inventados)")
    p.add_argument("pasta", help="Pasta do estudo (criada se não existir)")
    p.add_argument("--tipologia", type=_tipologia, default="residencial-unifamiliar", metavar="TIPOLOGIA",
                   help="escolar, comercial, residencial-unifamiliar, residencial-multifamiliar, hospitalar ou aeroportuario")
    p.add_argument("--forcar", action="store_true", help="Sobrescreve um estudo.json existente")

    p = nova("validate", "Valida o estudo.json: esquema, apelidos, arquivos e projetos")
    p.add_argument("estudo", help="Arquivo estudo.json")
    p.add_argument("--esquema", action="store_true", help="Só a estrutura do JSON, sem abrir projetos nem séries de chuva")

    p = nova("run", "Executa todos os casos do estudo e escreve as tabelas")
    p.add_argument("estudo", help="Arquivo estudo.json")
    p.add_argument("--saida", required=True, help="Pasta de saída (resultados.csv, resultados.json, tabela.md, tabela.tex, resumo.md)")
    p.add_argument("--retomar", action="store_true", help="Ignora os casos já calculados e inalterados")
    p.add_argument("--sobrescrever", action="store_true", help="Refaz todos os casos numa pasta de saída que já tem resultados")
    p.add_argument("--paralelo", type=_inteiro_positivo, default=1, metavar="N", help="Casos em N processos (o resultado não muda)")
    p.add_argument("--quiet", action="store_true", help="Oculta o progresso")
    p.add_argument("--progresso", choices=PR.MODOS, default="auto",
                   help="Progresso na saída de erro: rich (extra cli), simples (uma linha por caso) ou auto (rich se houver e for terminal). Os resultados não mudam")

    p = nova("resumo", "Refaz as tabelas a partir da pasta de saída, sem recalcular")
    p.add_argument("pasta", help="Pasta de saída de «triton estudo run»")
    p.add_argument("--estudo", help="Outro estudo.json (por exemplo com outras métricas ou casas decimais) no lugar da cópia da pasta")
    p.add_argument("--idioma", choices=E.IDIOMAS, help="Idioma das tabelas (padrão: o do estudo)")

    p = nova("lote", "Executa vários estudo*.json de uma pasta e compara as tipologias")
    p.add_argument("pasta", help="Pasta com os arquivos estudo*.json")
    p.add_argument("--saida", required=True, help="Pasta de saída (uma subpasta por estudo, mais comparativo.*)")
    p.add_argument("--recursivo", action="store_true", help="Procura estudo*.json também nas subpastas")
    p.add_argument("--retomar", action="store_true", help="Ignora os casos já calculados e inalterados")
    p.add_argument("--sobrescrever", action="store_true", help="Refaz todos os casos numa pasta de saída que já tem resultados")
    p.add_argument("--paralelo", type=_inteiro_positivo, default=1, metavar="N", help="Casos em N processos (o resultado não muda)")
    p.add_argument("--idioma", choices=E.IDIOMAS, help="Idioma do comparativo (padrão: o do primeiro estudo)")
    p.add_argument("--quiet", action="store_true", help="Oculta o progresso")
    p.add_argument("--progresso", choices=PR.MODOS, default="auto",
                   help="Progresso na saída de erro: rich (extra cli), simples (uma linha por caso) ou auto (rich se houver e for terminal). Os resultados não mudam")

    p = nova("consolidar", "Consolida os resultados.csv de várias execuções numa só tabela (tipologia, caso, métrica)")
    p.add_argument("pastas", nargs="+", metavar="PASTA", help="Pastas de saída de «triton estudo run» ou «lote» (procura resultados.csv nas subpastas)")
    p.add_argument("--saida", required=True, help="Pasta de saída (consolidado.csv e consolidado.md)")
    p.add_argument("--idioma", choices=E.IDIOMAS, help="Idioma da tabela em Markdown (padrão: o da edição)")
    p.add_argument("--motor", choices=C.MOTORES, default="auto",
                   help="Leitura dos arquivos: duckdb (extra analise) ou csv (biblioteca padrão); auto usa o duckdb se estiver instalado. O resultado é o mesmo")

    p = nova("texto", "Preenche um modelo de texto (.md) com os números reais dos resultados")
    p.add_argument("pasta", help="Pasta de saída de «triton estudo run»")
    p.add_argument("--modelo", required=True, help="Arquivo .md com marcadores de chaves duplas: metrica:caso, metrica:@min, metrica:@max, metrica:@media, n_casos")
    p.add_argument("--saida-texto", dest="saida_texto", help="Arquivo de saída (padrão: texto.md na pasta de saída; «-» imprime)")
    p.add_argument("--estrito", action="store_true", help="Termina com código 1 se algum marcador ficar sem resultado (XX)")
    p.add_argument("--idioma", choices=E.IDIOMAS, help="Idioma dos números (padrão: o do estudo)")

    p = nova("esquema", "Imprime o esquema JSON (JSON Schema) do estudo.json")
    p.add_argument("--saida", help="Grava no arquivo em vez de imprimir")

    nova("apelidos", "Lista os apelidos de parâmetros e as métricas disponíveis")


def _avisar(msg: str) -> None:
    print(msg, file=sys.stderr)


def _escrever_arquivo(destino: Path, texto: str) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


def _init(args: argparse.Namespace) -> int:
    pasta = Path(args.pasta)
    alvo = pasta / "estudo.json"
    if alvo.exists() and not args.forcar:
        raise ValueError(_t("{0} já existe; use --forcar para sobrescrevê-lo").format(alvo.name))
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "casos").mkdir(exist_ok=True)
    _escrever_arquivo(alvo, E._json_texto(E.esqueleto(pasta, args.tipologia)))
    _escrever_arquivo(pasta / "casos" / "LEIA.md", _t(
        "# Projetos e séries de chuva do estudo\n\nColoque aqui os arquivos .triton (um por edifício ou um só, como projeto base) e as séries "
        "diárias de chuva (.csv). O estudo.json refere estes arquivos por caminho relativo a esta pasta, por exemplo casos/predio.triton.\n\n"
        "Nada neste esqueleto foi preenchido pelo programa: substitua os «XX» e os null pelos dados do seu estudo e indique a fonte de cada um.\n"))
    _escrever_arquivo(pasta / "modelo_texto.md", E.modelo_de_texto(args.tipologia))
    print(_t("Estudo criado em: {0}").format(alvo.resolve()))
    print(_t("Próximos passos: preencha o estudo.json, execute «triton estudo validate» e depois «triton estudo run»."))
    return 0


def _validate(args: argparse.Namespace) -> int:
    plano, avisos = E.carregar_plano(Path(args.estudo), verificar_arquivos=not args.esquema)
    erros: List[str] = []
    if not args.esquema:
        erros = E.verificar_casos(plano)
    for a in avisos:
        _avisar(f"{_t('Aviso:')} {a}")
    if erros:
        raise E.ErroDeEstudo(erros)
    print(_t("Estudo válido: {0} casos, tipologia {1}, análise {2}.").format(
        len(plano["casos"]), plano["estudo"]["tipologia"], plano["analise"]["tipo"]))
    return 0


def _resumo_da_execucao(ex: E.Execucao, saida: Path) -> None:
    print(_t("Estudo concluído: {0} calculados, {1} ignorados, {2} com erro.").format(
        len(ex.calculados), len(ex.pulados), len(ex.erros)))
    print(_t("Saídas em: {0}").format(saida.resolve()))
    for nome in ex.arquivos:
        print(f"- {nome}")


def _run(args: argparse.Namespace) -> int:
    log, progresso, fechar = PR.criar(args.progresso, args.quiet)
    saida = Path(args.saida)
    try:
        ex = E.rodar_estudo(Path(args.estudo), saida, args.retomar, args.sobrescrever, args.paralelo, log, progresso)
    finally:
        fechar()
    for a in ex.avisos:
        _avisar(f"{_t('Aviso:')} {a}")
    _resumo_da_execucao(ex, saida)
    if ex.erros:
        _avisar(_t("Casos com erro: {0}").format(", ".join(ex.erros)))
    return ex.codigo


def _resumo(args: argparse.Namespace) -> int:
    gravados = E.refazer_resumo(Path(args.pasta), Path(args.estudo) if args.estudo else None, args.idioma)
    print(_t("Tabelas refeitas em: {0}").format(Path(args.pasta).resolve()))
    for nome in gravados:
        print(f"- {nome}")
    return 0


def _lote(args: argparse.Namespace) -> int:
    log, progresso, fechar = PR.criar(args.progresso, args.quiet)
    saida = Path(args.saida)
    try:
        execucoes, comparativo = E.rodar_lote(Path(args.pasta), saida, args.recursivo, args.retomar, args.sobrescrever,
                                              args.paralelo, args.idioma, log, progresso)
    finally:
        fechar()
    calc = sum(len(e.calculados) for e in execucoes)
    pul = sum(len(e.pulados) for e in execucoes)
    err = sum(len(e.erros) for e in execucoes)
    print(_t("Lote concluído: {0} estudos, {1} casos calculados, {2} ignorados, {3} com erro.").format(len(execucoes), calc, pul, err))
    print(_t("Saídas em: {0}").format(saida.resolve()))
    for nome in comparativo:
        print(f"- {nome}")
    return 1 if err else 0


def _consolidar(args: argparse.Namespace) -> int:
    saida = Path(args.saida)
    arquivos, n_arquivos, n_linhas, motor = C.consolidar([Path(p) for p in args.pastas], saida, args.idioma, args.motor)
    print(_t("Consolidado: {0} arquivos resultados.csv, {1} linhas (tipologia, caso, métrica).").format(n_arquivos, n_linhas))
    print(_t("Leitura e agrupamento: {0}").format(motor))
    print(_t("Saídas em: {0}").format(saida.resolve()))
    for nome in arquivos:
        print(f"- {nome}")
    return 0


def _texto(args: argparse.Namespace) -> int:
    pasta = Path(args.pasta)
    modelo = Path(args.modelo)
    if not modelo.is_file():
        raise FileNotFoundError(_t("Modelo não encontrado: {0}").format(modelo.name))
    plano, resultados = E.carregar_saida(pasta)
    lingua = E.resolver_idioma(args.idioma if args.idioma else plano["saidas"]["idioma"])
    texto, faltas = E.substituir_marcadores(modelo.read_text(encoding="utf-8-sig"), plano, resultados, lingua)
    if args.saida_texto == "-":
        sys.stdout.write(texto)
    else:
        destino = Path(args.saida_texto) if args.saida_texto else pasta / "texto.md"
        _escrever_arquivo(destino, texto)
        print(_t("Texto gravado em: {0}").format(destino.resolve()))
    if faltas:
        _avisar(_t("{0} marcador(es) sem resultado, deixados como «XX»: {1}").format(len(faltas), ", ".join(faltas)))
        if args.estrito:
            return 1
    return 0


def _esquema(args: argparse.Namespace) -> int:
    texto = E._json_texto(E.esquema_json())
    if args.saida:
        _escrever_arquivo(Path(args.saida), texto)
        print(_t("Esquema gravado em: {0}").format(Path(args.saida).resolve()))
    else:
        sys.stdout.write(texto)
    return 0


def _apelidos(_args: argparse.Namespace) -> int:
    from triton.core.edition import is_int_edition
    sys.stdout.write(E.texto_do_catalogo(is_int_edition()))
    return 0


_DESPACHO = {"init": _init, "validate": _validate, "run": _run, "resumo": _resumo, "lote": _lote,
             "consolidar": _consolidar, "texto": _texto, "esquema": _esquema, "apelidos": _apelidos}


def executar(args: argparse.Namespace) -> int:
    """Executa a ação pedida e devolve o código de saída (os erros de uso sobem como ``ValueError``/``OSError``)."""
    return _DESPACHO[args.estudo_acao](args)
