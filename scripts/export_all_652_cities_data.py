"""Compatibilidade para o antigo exportador de tarifas.

O catálogo canônico passou a ser produzido por ``audit_tariffs.py`` dentro da
pasta ``tarifas``. Este arquivo permanece apenas para não quebrar comandos e
atalhos antigos do projeto.
"""

from audit_tariffs import main


if __name__ == "__main__":
    main()
