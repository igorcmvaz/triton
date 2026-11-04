<div align="center">

# Triton

**Rainwater harvesting simulation for buildings**<br>
*Simulação de aproveitamento de água de chuva em edificações*

Triton is the child of [Netuno](https://sustainability.ufsc.br/): the same calculation engine, with its own name,
logo, versioning and one edition for each region.

![Version](https://img.shields.io/badge/version-0.1.0-1f497d)
![Python](https://img.shields.io/badge/python-3.12%2B-1f497d)
![Installers](https://img.shields.io/badge/installers-in%20preparation-lightgrey)
[![Licence: academic source-available](https://img.shields.io/badge/licence-academic%20source--available-lightgrey)](#licence)

</div>

---

## Three editions

<table>
  <tr>
    <td align="center" width="33%">
      <a href="triton_brl"><img src="triton_brl/icons/triton_brl.png" width="140" alt="Triton Brasil"></a><br>
      <h3>Brasil (BRL)</h3>
      <sub><code>triton_brl/</code></sub>
    </td>
    <td align="center" width="33%">
      <a href="triton_int"><img src="triton_int/icons/triton_int.png" width="140" alt="Triton International"></a><br>
      <h3>International (INT)</h3>
      <sub><code>triton_int/</code></sub>
    </td>
    <td align="center" width="33%">
      <a href="triton_ibe"><img src="triton_ibe/icons/triton_ibe.png" width="140" alt="Triton IBE"></a><br>
      <h3>Ibérica (IBE) · Triton IBE</h3>
      <sub><code>triton_ibe/</code></sub>
    </td>
  </tr>
  <tr>
    <td valign="top">
      Brazilian rainfall (CLIMBra, CMIP6), audited water and sewer tariffs for 652 municipalities, costs in reais and
      Brazilian standards (ABNT NBR 15527).
    </td>
    <td valign="top">
      Region-neutral. You supply rainfall, tariffs and costs in the currency of your choice. Worked examples for New
      York, London and Cape Town.
    </td>
    <td valign="top">
      Iberian Peninsula edition. Today only Portugal has data: European rainfall (E-OBS) by municipality (278 municipalities;
      Spain: 0 sites), Portuguese water tariffs, costs in euros and European Portuguese.
      Worked examples for Lisbon, Porto and Funchal.
    </td>
  </tr>
  <tr>
    <td align="center"><a href="triton_brl/README.md">README (pt)</a> · <a href="triton_brl/docs/en/README.md">README (en)</a></td>
    <td align="center"><a href="triton_int/README.md">README (pt)</a> · <a href="triton_int/docs/en/README.md">README (en)</a></td>
    <td align="center"><a href="triton_ibe/README.md">README (pt)</a> · <a href="triton_ibe/docs/en/README.md">README (en)</a></td>
  </tr>
</table>

All three share the same engine and the same version number. Each folder is self-contained, with its own source,
tests, and manual, so you only need the one you use.

## Download
The Windows installers are **not** in this repository. They are released in a single Zenodo record, so that each release can be cited and kept as it was released: DOI [10.5281/zenodo.23402916](https://doi.org/10.5281/zenodo.23402916), with the installers' SHA-256 checksums. Installers are not code-signed.
To run from the source code instead, see the [Quick start](#quick-start).

| Edition | Installer (in the Zenodo record) |
|---|---|
| Brasil (BRL) | `Triton_Brasil_Setup_v0.1.0.exe` |
| International (INT) | `Triton_Internacional_Setup_v0.1.0.exe` |
| Ibérica (IBE) | `Triton_Iberica_Setup_v0.1.0.exe` |

The source code in this repository is the same one the installers are built from. The repository holds what is needed
to run Triton from the command line and the graphical interface; the packaging tools are kept by the maintainer.

## What Triton does

- **Water balance.** Daily simulation of the reservoir with the Triton operating rule (and Fewkes' φ rule as an option
  for a single tank), with mass-closure checks.
- **Sizing.** Reservoir volume curves, ideal volume by marginal gain, one or two tanks, first-flush discard.
- **Economics.** Water, sewer and energy tariffs, CAPEX and OPEX, payback and net present value.
- **Environment.** Life-cycle carbon and certification scoring (LEED, EDGE, AQUA-HQE and others).
- **Decision.** Multi-criteria ranking with TOPSIS and SMAA-VIKOR.
- **Outputs.** Executive report, environmental audit and technical dossier in PDF; CAD, BIM and spreadsheet export.

## Quick start

To run from source (the installers are not published yet, see [Download](#download)):

```bash
cd triton_int                 # or triton_brl / triton_ibe
pip install -r requirements.txt
python main.py
```

To run the tests of one edition (the edition is set by `TRITON_EDITION`):

```bash
cd triton_brl                 # or triton_int / triton_ibe
pip install -r requirements.txt -r requirements-dev.txt
TRITON_EDITION=BRL python -m pytest tests/unit tests/test_essencial.py   # INT, IBE for the others
# Windows PowerShell: $env:TRITON_EDITION = "BRL"; python -m pytest tests/unit tests/test_essencial.py
```

## Data

Each edition documents its data (source, licence, coverage, period, gaps, quality and size): [Brazil](triton_brl/docs/DADOS.md) (Portuguese), [International](triton_int/docs/DADOS.md) (English) and [Iberian](triton_ibe/docs/DADOS.md) (European Portuguese). No tracked file exceeds 50 MiB; `python scripts/verificar_tamanhos.py` checks it and the GitHub workflow runs it.

## Cite

If you use Triton in academic work, you must cite it (clause 4 of the licence):

> Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Computational Platform for Rainwater Harvesting Simulation in Buildings.* Federal University of Santa Catarina (UFSC).

Machine-readable metadata is in [`CITATION.cff`](CITATION.cff); the DOI will be assigned when the release is published.

## Roadmap

Planned versions (1.1 and 2.0) and the evidence behind them are in [`ROADMAP.md`](ROADMAP.md). The same numbering
applies to the three editions.

## Licence

Academic source-available, all rights reserved, free for non-commercial use. Citing the program is mandatory in any
work that uses its results. The full terms are in `LICENSE.md` inside each edition folder.

## Notes

- The Brasil edition's climate database is versioned as one SQLite file per CMIP6 model,
  `triton_brl/data/climbra_<model>.db` (19 files of 40 to 43 MiB, 785 MiB in all, each below the project limit of 50 MiB, which is stricter than GitHub's 100 MiB). The
  single 820 MB `climbra.db` of earlier builds is not in Git; the program still reads it if present. See
  [`triton_brl/scripts/README.md`](triton_brl/scripts/README.md).
- «Netuno 1» to «Netuno 4» are the previous programme, kept as history in the manuals and in the comparisons.
- To cite Triton, use **Cite this repository** on GitHub (the root [`CITATION.cff`](CITATION.cff)); each edition also has its own
  `CITATION.cff` with the edition's abstract.

<div align="center">
<sub>Igor Catão Martins Vaz and Enedir Ghisi · Sustainable Environments Research Group (GPAS) ·
Federal University of Santa Catarina (UFSC), Florianópolis, Brazil</sub>
</div>
