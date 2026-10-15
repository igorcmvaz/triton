# Scripts

Command-line tools that ship with the source. None is imported by `triton/`; they run from outside,
on the project. Run them from this folder (`triton_int/`).

| Script | What it does |
| :--- | :--- |
| `qa_runner.py` | runs the verification layers (full suite and gates; see `--help`) |
| `bench_kernels.py` | compares the reference Python kernel with the compiled one |
| `gerar_avisos_de_terceiros.py` | writes `infos_licenses/AVISOS_DE_TERCEIROS.txt` (third-party notices) for this edition; `build_exe.py` runs it before packaging |

Scripts for building region-specific data (rainfall databases, tariff tables, worked-example
generators) belong to the regional editions and are not part of this one.
