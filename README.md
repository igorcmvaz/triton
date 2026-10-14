# Triton

Triton is the child of [Netuno](https://sustainability.ufsc.br/): a simulation tool for rainwater harvesting and
building water systems. This repository holds the three editions of version **1.0.0**, each in its own folder
with its own source, tests, manual and installer.

| Folder | Edition | Scope |
|---|---|---|
| [`triton_brl/`](triton_brl) | Brasil (BRL) | Brazilian rainfall, tariffs and standards |
| [`triton_int/`](triton_int) | International (INT) | Any location; user-supplied rainfall and tariffs |
| [`triton_prt/`](triton_prt) | Portugal (PRT) | Portuguese rainfall, tariffs and regulations |

Each folder is self-contained. Start with its `README.md` (Portuguese) or `README.en.md`.

## Running the tests of one edition

```bash
cd triton_brl            # or triton_int / triton_prt
pip install -r requirements.txt -r requirements-dev.txt
TRITON_EDITION=BRL python -m pytest tests/unit tests/test_essencial.py   # INT / PRT for the others
```

## Notes

- `triton_brl/data/climbra.db` (about 820 MB) is not versioned. It is built locally from the source data (see the manual).
- The editions are generated from the Netuno 5.0.1 source tree and renamed; the history of Netuno 1 to 4 is kept
  as history in the manuals and is not renamed.
- Citation metadata is in `CITATION.cff` inside each edition.
