"""O ícone do programa precisa dos tamanhos pequenos, e precisa ser quadrado.

O Windows desenha o ícone da barra de título a 16 px e o da barra de tarefas a
32 ou 48. Um `.ico` que traga só o quadro de 256 px — pior ainda, um quadro não
quadrado, de 256x250 — não é redimensionado: a janela simplesmente aparece sem
ícone. Foi o que aconteceu quando o aplicativo reiniciou para trocar de idioma,
e o ícone novo entrou em uso pela primeira vez.

Este teste percorre os ícones que o programa procura, na ordem em que procura, e
recusa o que não servir.
"""
import os

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ICONES = os.path.join(RAIZ, "icons")

PROCURADOS = (
    "triton.ico",
    "icon.ico",
    "triton_brl.png",
    "triton_int.png",
    "triton_prt.png",
    "triton.png",
    "icon.png",
    "Triton2.png",
)

#: Tamanhos que o Windows pede. Sem eles, não há ícone na tela.
INDISPENSAVEIS = {16, 32, 48}


def _quadros(caminho):
    from PIL import Image
    with Image.open(caminho) as im:
        return sorted(im.info.get("sizes", []) or [im.size])


@pytest.mark.parametrize("nome", [n for n in PROCURADOS if n.endswith(".ico")])
def test_o_ico_traz_os_tamanhos_que_o_windows_pede(nome):
    caminho = os.path.join(ICONES, nome)
    if not os.path.isfile(caminho):
        pytest.skip(f"{nome} não está no repositório")
    larguras = {l for l, _ in _quadros(caminho)}
    faltam = sorted(INDISPENSAVEIS - larguras)
    assert not faltam, (f"{nome} não tem os quadros de {faltam} px; "
                        f"tem {sorted(larguras)}")


@pytest.mark.parametrize("nome", [n for n in PROCURADOS if n.endswith(".ico")])
def test_todo_quadro_do_ico_e_quadrado(nome):
    """256x250 não é ícone: o Windows descarta o quadro e a janela fica sem nada.

    A regra vale para o `.ico`, onde o sistema escolhe um quadro pronto e não
    redimensiona. Um `.png` de recurso pode não ser quadrado — o Qt o reduz
    preservando a proporção —, e por isso o `Triton2.png`, que é o logotipo de
    último recurso, não entra nesta verificação.
    """
    caminho = os.path.join(ICONES, nome)
    if not os.path.isfile(caminho):
        pytest.skip(f"{nome} não está no repositório")
    tortos = [(l, a) for l, a in _quadros(caminho) if l != a]
    assert not tortos, f"{nome} tem quadro não quadrado: {tortos}"


def test_o_primeiro_da_lista_e_o_que_o_instalador_usa():
    """Um ícone na janela e outro no atalho é defeito que ninguém percebe cedo."""
    spec = open(os.path.join(RAIZ, "Triton.spec"), encoding="utf-8").read()
    iss = open(os.path.join(RAIZ, "setup_script.iss"), encoding="utf-8").read()
    primeiro = next(n for n in PROCURADOS
                    if os.path.isfile(os.path.join(ICONES, n)) and n.endswith(".ico"))
    assert primeiro in spec, (f"Triton.spec não usa {primeiro}, que é o primeiro "
                              f"ícone que o programa carrega")
    assert f'#define MyAppIcon "icons\\{primeiro}"' in iss, (
        f"setup_script.iss não usa {primeiro} como MyAppIcon"
    )
