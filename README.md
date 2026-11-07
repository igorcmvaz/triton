<div align="center">

# Triton

**Rainwater harvesting simulation for buildings**<br>
*Simulação de aproveitamento de água de chuva em edificações*

Triton is the official successor to [Netuno](https://sustainability.ufsc.br/#/netuno): the same validated calculation philosophy, expanded with life-cycle assessment (LCA), engineering economics, multi-criteria decision analysis (MCDA), and dedicated regional editions.

![Version](https://img.shields.io/badge/version-0.1.0%20Beta-1f497d)
![Python](https://img.shields.io/badge/python-3.12%2B-1f497d)
[![Official Portal & Download](https://img.shields.io/badge/download%20%26%20portal-sustainability.ufsc.br-059669)](https://sustainability.ufsc.br/#/triton)
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
      <a href="triton_prt"><img src="triton_prt/icons/triton_prt.png" width="140" alt="Triton Ibérica / Portugal"></a><br>
      <h3>Ibérica / Portugal (PRT)</h3>
      <sub><code>triton_prt/</code></sub>
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
      European rainfall (E-OBS & Iberia01) by municipality, Portuguese water tariffs (ERSAR), costs in euros and European Portuguese.
      Worked examples for Lisbon, Porto and Funchal.
    </td>
  </tr>
  <tr>
    <td align="center"><a href="triton_brl/README.md">README (pt)</a> · <a href="triton_brl/docs/en/README.md">README (en)</a></td>
    <td align="center"><a href="triton_int/README.md">README (pt)</a> · <a href="triton_int/docs/en/README.md">README (en)</a></td>
    <td align="center"><a href="triton_prt/README.md">README (pt)</a> · <a href="triton_prt/docs/en/README.md">README (en)</a></td>
  </tr>
</table>

All three share the same engine and the same version number. Each folder is self-contained, with its own source,
tests, manual and Windows installer build scripts, so you only need the one you use.

## Download & Usage Registration (Beta)

The standalone Windows installers (`.exe`) and technical manuals (`.pdf`) are **not** stored directly in this Git repository.

To download the latest **Beta** release (`v0.1.0`) and log your academic, teaching, or professional usage of the platform, please use the official UFSC portal as the primary entry point:

👉 **[https://sustainability.ufsc.br/#/triton](https://sustainability.ufsc.br/#/triton)**

*(PT: Para registrar o uso da ferramenta e baixar a versão mais recente do Beta com os instaladores e manuais oficiais, acesse o portal principal em **[https://sustainability.ufsc.br/#/triton](https://sustainability.ufsc.br/#/triton)**).*

After a quick registration on the portal (Name, Email, Institution/Company, Edition, and Purpose), you will immediately unlock the official release page containing the installers and manuals for all three editions:

| Edition | Windows Installer (`.exe`) | Technical Manual (`.pdf`) |
|---|---|---|
| **Brasil (BRL)** | `Triton_Brasil_Setup_v0.1.0.exe` | `Manual_Triton_Brasil_v0.1.0.pdf` |
| **Ibérica / Portugal (PRT)** | `Triton_Iberica_Setup_v0.1.0.exe` | `Manual_Triton_Iberica_v0.1.0_PT.pdf` |
| **International (INT)** | `Triton_Internacional_Setup_v0.1.0.exe` | `Manual_Triton_Internacional_v0.1.0_EN.pdf` |

> **Beta Feedback & Model Detailing:** Because water/sewer tariff calibration, daily precipitation series, and normative parameters are specific to each regional model, users are encouraged to collaborate by reporting any errors or suggested adjustments in the detailing via email (`igorcmvaz@gmail.com`) or through GitHub Issues.

The source code in this repository is the exact one the installers are built from; to build an installer yourself from source, run `python build_exe.py --installer` inside the respective edition folder.

## What Triton does

- **Water balance.** Daily simulation of the reservoir with the Triton operating rule (and Fewkes' φ rule as an option
  for a single tank), with mass-closure checks.
- **Sizing.** Reservoir volume curves, ideal volume by marginal gain, one or two tanks, first-flush discard.
- **Economics.** Water, sewer and energy tariffs, CAPEX and OPEX, payback and net present value.
- **Environment.** Life-cycle carbon and certification scoring (LEED, EDGE, AQUA-HQE and others).
- **Decision.** Multi-criteria ranking with TOPSIS, VIKOR, SMAA-VIKOR and PROMETHEE II.
- **Outputs.** Executive report, environmental audit and technical dossier in PDF; CAD, BIM and spreadsheet export.

## Quick start

To run from source (the compiled Windows installers are available via the [official portal](https://sustainability.ufsc.br/#/triton)):

```bash
cd triton_int                 # or triton_brl / triton_prt
pip install -r requirements.txt
python main.py
```

To run the tests of one edition (the edition is set by `TRITON_EDITION`):

```bash
cd triton_brl                 # or triton_int / triton_prt
pip install -r requirements.txt -r requirements-dev.txt
TRITON_EDITION=BRL python -m pytest tests/unit tests/test_essencial.py   # INT, PRT for the others
# Windows PowerShell: $env:TRITON_EDITION = "BRL"; python -m pytest tests/unit tests/test_essencial.py
```

## Cite

If you use Triton in academic work, you must cite it (clause 4 of the licence):

> Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Computational Platform for Rainwater Harvesting Simulation in Buildings (Editions: Brasil, International, and Ibérica)* (Version 0.1.0) [Computer software]. Universidade Federal de Santa Catarina (UFSC), Florianópolis, SC, Brazil.

Machine-readable metadata is in [`CITATION.cff`](CITATION.cff).

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
