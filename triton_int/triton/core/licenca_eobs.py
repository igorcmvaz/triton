# -*- coding: utf-8 -*-
"""Licença da E-OBS na edição IBE: o aviso do primeiro arranque, a escolha de uso e o rodapé do laudo.

A chuva da edição vem da E-OBS (ECA&D/Copernicus), de uso estritamente não comercial em pesquisa e
educação. A licença não trata da redistribuição de produtos derivados (``LICENCAS_DOS_DADOS.md``);
o aviso diz ao utilizador o que a licença pede, e o laudo repete a restrição e a citação. Nada aqui é
parecer jurídico: o texto precisa de revisão da UFSC antes da primeira distribuição (D5).

Decisão do titular (25/10/2026): a E-OBS fica disponível, mas todo relatório que a usa traz, bem grande e em
vermelho, que ela «não pode ser usada comercialmente» (``aviso_vermelho``), e quem declara uso comercial neste
computador a tem desligada (``BLOQUEAR_E_OBS_EM_USO_COMERCIAL``; o caminho é a série própria, ``custom_file``).
Quem usa assume o uso não comercial; o titular do programa não responde por uso comercial.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

# decisão do usuário (D1, 25/10/2026): ligado
#: Bloquear a E-OBS quando o utilizador declara uso comercial? True (padrão): a E-OBS fica indisponível e o programa pede a série
#: própria (``climate_source_mode = "custom_file"``). False: só avisa, regista a declaração no laudo e segue.
BLOQUEAR_E_OBS_EM_USO_COMERCIAL = True

USO_PESQUISA = "pesquisa"
USO_COMERCIAL = "comercial"
USOS = (USO_PESQUISA, USO_COMERCIAL)

#: As duas respostas do aviso, tal como aparecem nos botões.
RESPOSTAS = {
    USO_PESQUISA: "Uso de pesquisa ou educação",
    USO_COMERCIAL: "Uso comercial",
}

TITULO_DO_AVISO = "Dados de chuva: licença da E-OBS"

TEXTO_DO_AVISO = (
    "Os dados de chuva desta edição vêm da E-OBS, de uso estritamente não comercial em pesquisa e educação. "
    "A E-OBS é um produto do projeto ECA&D e do serviço Copernicus (versão {versao}). "
    "Se o seu projeto é profissional ou pago, carregue a sua própria série de chuva ou obtenha autorização "
    "dos titulares dos dados. O programa não verifica o uso: quem o utiliza assume o uso não comercial, e o titular do programa não responde por uso comercial. "
    "Este aviso não é parecer jurídico. Escolha o uso que se aplica a este computador."
)

#: O que o ecrã diz depois de «Uso comercial», conforme a constante.
TEXTO_COMERCIAL_BLOQUEADO = (
    "A base E-OBS foi desligada neste computador. Carregue a série diária de chuva do seu projeto "
    "(ficheiro próprio) ou obtenha autorização dos titulares dos dados."
)
TEXTO_COMERCIAL_SO_AVISA = (
    "A E-OBS só pode ser usada em pesquisa e educação não comerciais. O programa mantém a base disponível, "
    "mas a sua declaração de uso comercial fica registada nos laudos. Para uso comercial, carregue a sua "
    "própria série de chuva ou obtenha autorização dos titulares dos dados."
)

CITACAO = ("Cornes, R. C., van der Schrier, G., van den Besselaar, E. J. M., Jones, P. D. (2018). An Ensemble Version "
           "of the E-OBS Temperature and Precipitation Data Sets. J. Geophys. Res. Atmos., 123(17), 9391-9409. "
           "doi:10.1029/2017JD028200")
RECONHECIMENTO = ("We acknowledge the E-OBS dataset from the EU-FP6 project UERRA (https://www.uerra.eu) and the "
                  "Copernicus Climate Change Service, and the data providers in the ECA&D project (https://www.ecad.eu)")

_CHAVE = "licenca_eobs/uso"
_memoria: Dict[str, str] = {}


class LicencaEObsBloqueada(RuntimeError):
    """A E-OBS está desligada neste computador (uso comercial declarado e bloqueio ligado)."""


# ── Escolha de uso, lembrada na configuração do utilizador ──────────────────────────────────

def _armazem():
    """A configuração do utilizador (QSettings da edição); None sem PySide6."""
    try:
        # o mesmo par organização/aplicação das preferências da edição (triton/ui/translation.py)
        from triton.core.edition import abrir_preferencias
        return abrir_preferencias()
    except Exception:
        return None


def ler_escolha(armazem: Optional[Any] = None) -> Optional[str]:
    """O uso que o utilizador declarou neste computador: 'pesquisa', 'comercial' ou None (nunca escolheu)."""
    arm = armazem if armazem is not None else _armazem()
    valor = _memoria.get(_CHAVE) if arm is None else arm.value(_CHAVE, "")
    valor = str(valor or "")
    return valor if valor in USOS else None


def gravar_escolha(uso: str, armazem: Optional[Any] = None) -> None:
    if uso not in USOS:
        raise ValueError(f"Uso inválido: {uso!r}; use um de {USOS}.")
    arm = armazem if armazem is not None else _armazem()
    if arm is None:
        _memoria[_CHAVE] = uso
        return
    arm.setValue(_CHAVE, uso)
    arm.sync()


def precisa_perguntar(armazem: Optional[Any] = None) -> bool:
    """Só a edição com a base E-OBS pergunta, e só uma vez por instalação (até haver escolha gravada)."""
    from triton.core.edition import usa_dados_de_portugal
    return usa_dados_de_portugal() and ler_escolha(armazem) is None


def e_obs_bloqueada(armazem: Optional[Any] = None) -> bool:
    """A E-OBS está desligada? Só com a constante ligada e a declaração de uso comercial."""
    return bool(BLOQUEAR_E_OBS_EM_USO_COMERCIAL) and ler_escolha(armazem) == USO_COMERCIAL


def texto_do_aviso() -> str:
    from triton.core import base_climatica_portugal as _pt
    versao = "v33.0e"
    try:
        if _pt.disponivel():
            versao = _pt.pacote().get("versao_eobs") or versao
    except Exception:
        pass
    return TEXTO_DO_AVISO.format(versao=versao)


def texto_depois_da_escolha(uso: str) -> str:
    """O que o utilizador lê depois de responder; vazio para o uso de pesquisa ou educação."""
    if uso != USO_COMERCIAL:
        return ""
    return TEXTO_COMERCIAL_BLOQUEADO if BLOQUEAR_E_OBS_EM_USO_COMERCIAL else TEXTO_COMERCIAL_SO_AVISA


# ── Rodapé do laudo ──────────────────────────────────────────────────────────────────────────

def credito_da_serie_de_exemplo(auditoria: Optional[Dict[str, Any]] = None, ingles: bool = False) -> str:
    """Crédito CC BY 4.0 das séries de exemplo da reanálise ERA5 obtidas pelo Open-Meteo; vazio para as demais.

    Vale pelo modelo climático gravado no projeto («ERA5 (Open-Meteo)»), nas edições sem a base do Brasil.
    """
    modelo = str((auditoria or {}).get("climate_model") or "").upper()
    if "ERA5" not in modelo and "OPEN-METEO" not in modelo:
        return ""
    if ingles:
        return ("Rainfall: weather data from Open-Meteo.com (CC BY 4.0), based on the ERA5 reanalysis of the Copernicus "
                "Climate Change Service (Hersbach et al., 2020).")
    return ("Chuva: dados meteorológicos de Open-Meteo.com (CC BY 4.0), a partir da reanálise ERA5 do Copernicus "
            "Climate Change Service (Hersbach et al., 2020).")


AVISO_VERMELHO_PT = "ATENÇÃO: a série de chuva deste relatório (E-OBS) NÃO PODE SER USADA COMERCIALMENTE."
AVISO_VERMELHO_EN = "WARNING: the rainfall series in this report (E-OBS) MUST NOT BE USED COMMERCIALLY."
AVISO_VERMELHO_NOTA_PT = ("Uso restrito a pesquisa e educação não comerciais (licença da E-OBS). Quem utiliza este relatório assume o uso "
                          "não comercial; o titular do programa não responde por uso comercial.")
AVISO_VERMELHO_NOTA_EN = ("Use restricted to non-commercial research and education (E-OBS licence). Whoever uses this report assumes "
                          "non-commercial use; the owner of the programme is not liable for commercial use.")


def chuva_e_iberica(auditoria: Optional[Dict[str, Any]]) -> bool:
    """A chuva do laudo é do Iberia01 ou das ilhas ERA5 (ODbL e CC BY: uso comercial permitido, com atribuição)?"""
    from triton.core.base_climatica_iberica import CENARIO_IBERIA01
    return str((auditoria or {}).get("climate_scenario") or "") == CENARIO_IBERIA01


def aviso_vermelho(auditoria: Optional[Dict[str, Any]] = None, ingles: bool = False) -> str:
    """O aviso grande e vermelho dos relatórios que usam a E-OBS (vazio fora da IBE e com série própria do utilizador).

    Leva a marca d'água diagonal «NÃO COMERCIAL» (aplicada só no PDF gerado pelo Chromium, que honra ``position: fixed``).
    """
    from html import escape
    from triton.core.edition import usa_dados_de_portugal
    if not usa_dados_de_portugal() or (auditoria or {}).get("chuva_serie_propria") or chuva_e_iberica(auditoria):
        return ""
    titulo, nota = (AVISO_VERMELHO_EN, AVISO_VERMELHO_NOTA_EN) if ingles else (AVISO_VERMELHO_PT, AVISO_VERMELHO_NOTA_PT)
    marca = "NON-COMMERCIAL" if ingles else "NÃO COMERCIAL"
    return (f"<div class='aviso-eobs' data-marca='{marca}' style='border:3px solid #b91c1c;background:#fef2f2;color:#b91c1c;"
            f"padding:10px 14px;margin:0 0 10px 0;text-align:center;'>"
            f"<div style='font-size:17pt;font-weight:800;line-height:1.2;'>{escape(titulo)}</div>"
            f"<div style='font-size:9pt;font-weight:600;margin-top:4px;'>{escape(nota)}</div></div>")


def inserir_aviso_vermelho(html: str, auditoria: Optional[Dict[str, Any]] = None, ingles: bool = False) -> str:
    """O mesmo HTML com o aviso vermelho logo depois de ``<body>`` (ou no começo, se não houver)."""
    import re
    aviso = aviso_vermelho(auditoria, ingles)
    if not aviso or "class='aviso-eobs'" in html:
        return html
    achado = re.search(r"<body[^>]*>", html, re.IGNORECASE)
    if achado:
        return html[:achado.end()] + aviso + html[achado.end():]
    return aviso + html


def marca_dagua_html(html: str) -> str:
    """Acrescenta a marca d'água diagonal, discreta, se o HTML traz o aviso vermelho (para o PDF do Chromium)."""
    import re
    achado = re.search(r"class='aviso-eobs' data-marca='([^']+)'", html)
    if not achado or "class='marca-eobs'" in html:
        return html
    marca = (f"<div class='marca-eobs' style='position:fixed;top:42%;left:0;width:100%;text-align:center;"
             f"transform:rotate(-28deg);font-size:72pt;font-weight:800;color:rgba(185,28,28,0.07);z-index:-1;'>{achado.group(1)}</div>")
    corpo = re.search(r"<body[^>]*>", html, re.IGNORECASE)
    return html[:corpo.end()] + marca + html[corpo.end():] if corpo else marca + html


def rodape_do_laudo(auditoria: Optional[Dict[str, Any]] = None, ingles: bool = False) -> str:
    """As linhas de texto que fecham todo laudo da edição IBE; vazio nas outras edições.

    ``auditoria`` é o ``audit_context`` do laudo: ``chuva_serie_propria`` (a série não é da E-OBS),
    ``climate_city_name`` (o concelho) e ``chuva_procedencia`` (a procedência gravada no projeto).
    Devolve HTML simples, já escapado, uma linha por ``<br/>``.
    """
    from html import escape
    from triton.core.edition import usa_dados_de_portugal, usa_dados_do_brasil
    aud = auditoria or {}
    credito = credito_da_serie_de_exemplo(aud, ingles)
    if not usa_dados_de_portugal():
        return escape(credito) if credito and not usa_dados_do_brasil() else ""
    from triton.core import qualidade_chuva as _q
    proc = aud.get("chuva_procedencia") or {}
    linhas = []
    if chuva_e_iberica(aud) and not aud.get("chuva_serie_propria"):
        return _rodape_iberico(aud, ingles)
    if aud.get("chuva_serie_propria"):
        linhas.append("Rainfall: series supplied by the user." if ingles else "Chuva: série fornecida pelo utilizador.")
        if credito:
            linhas.append(credito)
    else:
        pid = proc.get("pacote_id") or ""
        sha = str(proc.get("sha256_pacote") or "")[:8]
        try:
            atual = _pacote_atual()
        except Exception:
            atual = {}
        pid = pid or atual.get("pacote_id", "")
        sha = sha or str(atual.get("sha256_pacote", ""))[:8]
        versao = proc.get("versao_eobs") or atual.get("versao_eobs") or "v33.0e"
        pacote = (f" Pacote {pid}, SHA-256 {sha}." if pid else "")
        pacote_en = (f" Package {pid}, SHA-256 {sha}." if pid else "")
        if ingles:
            linhas.append(f"Rainfall: E-OBS {versao} (Cornes et al., 2018); use restricted to non-commercial research and "
                          f"education.{pacote_en}")
        else:
            linhas.append(f"Chuva: E-OBS {versao} (Cornes et al., 2018); uso restrito a pesquisa e educação não comerciais."
                          f"{pacote}")
        linhas.append(RECONHECIMENTO)
        if proc.get("mudou") and proc.get("aviso"):
            linhas.append(("Warning: the rainfall package changed since the project was saved. " if ingles else "Aviso: ")
                          + proc["aviso"])
        elif proc and not proc.get("registrado", True):
            linhas.append(proc.get("nota") or "")
        if ler_escolha() == USO_COMERCIAL:
            linhas.append("Declared use on this computer: commercial (the E-OBS licence does not allow it)."
                          if ingles else
                          "Uso declarado neste computador: comercial (a licença da E-OBS não o permite).")
        cidade = str(aud.get("climate_city_name") or "")
        if cidade:
            t = _q.texto_da_qualidade(cidade, "en" if ingles else "pt")
            if t:
                linhas.append(t)
    linhas.append(_q.linha_de_cobertura("en" if ingles else "pt"))
    return "<br/>".join(escape(l) for l in linhas if l)


def _rodape_iberico(aud: Dict[str, Any], ingles: bool) -> str:
    """Rodapé quando a chuva é do Iberia01 (ou ERA5 nas ilhas): fonte, licença ODbL, qualidade e cobertura."""
    from html import escape
    from triton.core import base_climatica_iberica as _ib
    lingua = "en" if ingles else "pt"
    linhas = []
    codigo = _ib.resolver(str(aud.get("climate_city_name") or ""))
    if codigo:
        linhas.append(_ib.texto_da_fonte(codigo, lingua))
        q = _ib.qualidade(codigo)
        if q:
            u = _ib.unidade(codigo)
            if ingles:
                linhas.append(f"Rainfall quality for {u['nome']}: level {q['nivel']}. Level reflects spatial representation "
                              f"of the grid, not a validation against local gauges.")
            else:
                linhas.append(f"Qualidade da chuva em {u['nome']}: nível {q['nivel']}. {q['motivo']}")
    else:
        linhas.append(_ib.texto_da_fonte("", lingua))
    try:
        p = _ib.pacote()
        if p.get("pacote_id"):
            linhas.append((f"Package {p['pacote_id']}, SHA-256 {p['sha256_pacote'][:8]}." if ingles
                           else f"Pacote {p['pacote_id']}, SHA-256 {p['sha256_pacote'][:8]}."))
    except Exception:
        pass
    linhas.append(_ib.linha_de_cobertura(lingua))
    return "<br/>".join(escape(l) for l in linhas if l)


def _pacote_atual() -> Dict[str, str]:
    from triton.core import base_climatica_portugal as _pt
    return _pt.pacote() if _pt.disponivel() else {}
