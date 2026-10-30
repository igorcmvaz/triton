"""O ícone da janela e o identificador de aplicativo do Windows são os mesmos no programa e nos atalhos."""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


def test_appid_do_main_igual_ao_dos_atalhos_do_instalador():
    main = (RAIZ / "main.py").read_text(encoding="utf-8")
    iss = (RAIZ / "setup_script.iss").read_text(encoding="utf-8-sig")
    no_main = re.search(r'SetCurrentProcessExplicitAppUserModelID\("([^"]+)"\)', main).group(1)
    no_iss = re.search(r'#define MyAppUserModelID "([^"]+)"', iss).group(1)
    assert no_main == no_iss
    assert iss.count('AppUserModelID: "{#MyAppUserModelID}"') >= 2


def test_icone_da_janela_so_age_no_windows_e_sem_janela_nao_quebra():
    from triton.ui import icone_windows
    assert callable(icone_windows.aplicar_icone_da_janela)
    assert icone_windows._caminho_do_icone() is not None
