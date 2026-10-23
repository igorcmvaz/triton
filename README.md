<div align="center">

# Triton

**Rainwater harvesting simulation for buildings**<br>
*Simulação de aproveitamento de água de chuva em edificações*

Triton is the child of [Netuno](https://sustainability.ufsc.br/): the same calculation engine, with its own name,
logo, versioning and one edition for each region.

![Version](https://img.shields.io/badge/version-0.1.0-1f497d)
![Python](https://img.shields.io/badge/python-3.12%2B-1f497d)
[![Zenodo](https://img.shields.io/badge/installers-Zenodo-1f497d)](ZENODO_LINK)
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
tests, manual and Windows installer, so you only need the one you use.

## Download

The Windows installers are **not** in this repository. All three editions are published in a single Zenodo record,
with a DOI, so that each release can be cited and kept as it was released:

**[Triton on Zenodo](ZENODO_LINK)**

| Edition | Installer |
|---|---|
| Brasil (BRL) | `Triton_Setup_0_1_0.exe` |
| International (INT) | `Triton_INT_Setup_0_1_0.exe` |
| Ibérica (IBE) | `Triton_IBE_Setup_0_1_0.exe` |

Each version of the record holds the installers of all editions, their checksums (SHA-256) and the release notes. The
source code in this repository is the same one the installers are built from; to build an installer yourself, run
`python build_exe.py --installer` inside the edition folder.

## What Triton does

- **Water balance.** Daily simulation of the reservoir with the Triton operating rule (and Fewkes' φ rule as an option
  for a single tank), with mass-closure checks.
- **Sizing.** Reservoir volume curves, ideal volume by marginal gain, one or two tanks, first-flush discard.
- **Economics.** Water, sewer and energy tariffs, CAPEX and OPEX, payback and net present value.
- **Environment.** Life-cycle carbon and certification scoring (LEED, EDGE, AQUA-HQE and others).
- **Decision.** Multi-criteria ranking with TOPSIS and SMAA-VIKOR.
- **Outputs.** Executive report, environmental audit and technical dossier in PDF; CAD, BIM and spreadsheet export.

## Quick start

To run from source (the installers are on [Zenodo](#download)):

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

## Cite

If you use Triton in academic work, you must cite it (clause 4 of the licence):

> Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Computational Platform for Rainwater Harvesting Simulation in Buildings.* Federal University of Santa Catarina (UFSC), Florianópolis, Brazil.

Machine-readable metadata is in [`CITATION.cff`](CITATION.cff); the Zenodo DOI will be added to it with the first release.

## Roadmap

Planned versions (1.1 and 2.0) and the evidence behind them are in [`ROADMAP.md`](ROADMAP.md). The same numbering
applies to the three editions.

## Licence

Academic source-available, all rights reserved, free for non-commercial use. Citing the program is mandatory in any
work that uses its results. The full terms are in `LICENSE.md` inside each edition folder.

## Notes

- The Brasil edition's climate database is versioned as one SQLite file per CMIP6 model,
  `triton_brl/data/climbra_<model>.db` (19 files of 40 to 44 MB, 785 MB in all, each below GitHub's 100 MB limit). The
  single 820 MB `climbra.db` of earlier builds is not in Git; the program still reads it if present. See
  [`triton_brl/scripts/README.md`](triton_brl/scripts/README.md).
- «Netuno 1» to «Netuno 4» are the previous programme, kept as history in the manuals and in the comparisons.
- To cite Triton, use **Cite this repository** on GitHub (the root [`CITATION.cff`](CITATION.cff)); each edition also has its own
  `CITATION.cff` with the edition's abstract.

<div align="center">
<sub>Igor Catão Martins Vaz and Enedir Ghisi · Sustainable Environments Research Group (GPAS) ·
Federal University of Santa Catarina (UFSC), Florianópolis, Brazil</sub>
</div>
