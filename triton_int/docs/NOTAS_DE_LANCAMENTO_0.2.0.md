# Triton, International Edition (INT): release notes for version 0.2.0

Version 0.2.0 (beta), released on 11 November 2026. It changes the multi-criteria decision — eight criteria, objective weights by CRITIC and a choice band instead of a single volume — and adds the weight of the system; the rest of the program is that of version 0.1.0, whose notes stay in [`NOTAS_DE_LANCAMENTO_0.1.0.md`](NOTAS_DE_LANCAMENTO_0.1.0.md). The full history is in [`../CHANGELOG.md`](../CHANGELOG.md); the manual is [`../manual/en/Triton-User-Manual.pdf`](../manual/en/Triton-User-Manual.pdf).

**In short: the multi-criteria decision now has eight criteria in four dimensions, and the volume it chooses can change.** A study ranked with version 0.1.0 is reproduced with version 0.1.0.

## What changed

**Eight criteria in four dimensions.** Version 0.1.0 ranked the volumes by seven criteria in three dimensions, and three of them — the saving potential, the potable water consumption and, through the bill, the net present value — measured the same water saved. Version 0.2.0 uses:

| Dimension | Criterion | Direction | Definition in the program |
| :--- | :--- | :--- | :--- |
| technical | volumetric reliability | maximise | rainwater consumed ÷ rainwater demand (non-potable use plus irrigation), in % |
| technical | storage efficiency | maximise | rainwater delivered per day ÷ volume of the lower cistern, in % (the annual turnover ÷ 365); it falls with the volume and curbs oversizing |
| economic | net financial savings | maximise | NPV of the system against the baseline without a cistern |
| economic | levelised cost of water (LCOW) | minimise | (investment + discounted running costs: energy, O&M, chlorine, treatment line) ÷ discounted rainwater delivered, at the project's rate and horizon; the alternative with no cistern receives the worst LCOW observed plus 10% |
| economic | discounted payback | minimise | as in 0.1.0; a volume that does not pay back receives the worst observed plus 10% (at least one year more and at least 20 years) |
| environmental | net life-cycle CO₂e | minimise | net CO₂e at the end of the service life (negative = avoided), as in 0.1.0 |
| structural | dry mass of materials | minimise | dry mass of cisterns, pipes, pump and fittings, from the program's weight calculator |
| structural | annual overflow | minimise | volume overflowed per year, in m³/year |

**Weights.** Four dimension weights (technical, economic, environmental, structural), 25% each by default, each shared among the criteria of its dimension by the criterion shares (equal by default; only the proportion within the dimension matters). Eight direct weights, one per criterion, are also accepted. TOPSIS, VIKOR and PROMETHEE II use the same rule; SMAA-VIKOR draws the eight weights instead, with 25% expected on each dimension (version 0.1.0 drew them uniformly over the criteria, so a dimension with more criteria weighed more on average).

- **Three weights**, as projects and studies of version 0.1.0 declared them, are still accepted: the structural dimension receives their mean, so equal weights stay equal.
- **Seven values**, weights or shares of the old model, are refused with the message «O multicritério da versão 0.2.0 tem oito critérios em quatro eixos, e os sete valores do modelo anterior não correspondem a eles. Informe quatro pesos de eixo (técnico, econômico, ambiental, estrutural) ou oito pesos de critério.» (the seven values of the previous model do not correspond to the eight criteria; enter four dimension weights or eight criterion weights).

| Where | Dimension weights | Criterion shares |
| :--- | :--- | :--- |
| decision tab | one card per dimension with its weight at the top, 25% each; the profile «Balanced: 25% on each dimension», the four «Prioritise …» profiles, with 70% on one dimension and 10% on each of the others, and «Objective weights (CRITIC), computed from the results» | in each card, below the weight, the shares of its criteria; the «Equal shares» and «Recalculate» buttons below the cards |
| command line | `--weights t,e,a,s` (or eight values, or `critic`; three still accepted) | `--criterion-shares` with eight values, default `1,1,1,1,1,1,1,1` |
| project file | `analysis.topsis_weights` (four or eight values, or `"critic"`) | `analysis.topsis_criterion_shares` (eight values) |
| declarative study | `analise.pesos` (four or eight, or `"critic"`; three accepted) | `analise.partes_no_eixo` (eight values) |

**Objective weights by CRITIC (new).** Instead of declaring the weights, the analysis can compute them from its own results by the CRITIC method (Diakoulaki, D.; Mavrotas, G.; Papayannakis, L., 1995. Determining objective weights in multiple criteria problems: the CRITIC method. *Computers & Operations Research*, 22(7), 763–770, doi:10.1016/0305-0548(94)00059-H). Each criterion is rescaled from 0 (worst observed) to 1 (best); its information is its standard deviation times the sum of (1 − r) over the other criteria, r being the Pearson correlation; the weight is its share of the total. A constant criterion weighs zero. The weights come from the volumes above zero, are recomputed at every analysis and hold for TOPSIS, VIKOR and PROMETHEE II; SMAA keeps drawing its own. CRITIC measures contrast and independence in the results, not anyone's preference: the weights change with the set of volumes evaluated, and a criterion that varies a lot gains weight even if it matters little. It is a choice of method, not a default. With `--weight-sensitivity`, `critic` draws the four dimension weights. A new message answers an unknown word in place of the weights: «Pesos «X» desconhecidos: use números ou «critic».» (weights «X» unknown: use numbers or «critic»).

**A choice band instead of a single volume (new).** When several volumes score alike, the program no longer names one «best volume». It reports the **choice band**: the volumes above zero whose score, rescaled from the worst (0) to the best (1) of the volumes evaluated, lies within a tolerance of the best — 5% of the score range by default — with the volume of the highest score as information. The rule holds for TOPSIS (score), VIKOR (index Q, lower is better), PROMETHEE II (net flow) and SMAA (first-rank acceptability); the program also says whether the band is contiguous. The band depends on the grid of volumes and on the tolerance, so a study must declare both. It appears in the decision tab («TOPSIS band (equal weights): 2000–3000 L · highest score: 2000 L (0.78)»), in the text, HTML («Choice band (TOPSIS)») and JSON outputs of the command line (`topsis.choice_band`, `topsis.choice_band_min_volume_l`, `topsis.choice_band_max_volume_l`, `smaa_vikor.choice_band`), and in the declarative study (metrics `faixa_topsis_min_l` and `faixa_topsis_max_l`). The tolerance is set with `--score-band` (0 to 1, on every subcommand that takes `--weights`), `analysis.topsis_score_band` in the project file and `analise.tolerancia_faixa` in `estudo.json`.

**Weight of the system (new).** `triton analyze … --analysis all` (and `--analysis system_weight`) reports the dry mass, the water load and the operating load, in kg and kN, at three positions: basement or lower level, roof or upper level, and risers and network. The HTML report, the spreadsheet (sheet `system_weight` with the summary of the chosen volume; the values per volume are in the sheet `alternatives`) and the terminal text show the block. Its warnings use attention thresholds of the **program**, not of any standard — 500 kg on the roof with the upper tank full, an upper tank above 1,500 L, a cistern above 3,000 kg dry, and any concrete cistern — and ask for a check by the structural or foundation design.

## What it does to results

The multi-criteria ranking can change; the water balance, the economics and the life-cycle assessment do not. In the New York tutorial of the manual (candidate volumes from 1,000 to 12,000 L, polyethylene cistern, illustrative costs):

- with the four dimensions weighted equally, TOPSIS gives a choice band of **2,000 to 3,000 L**, with the highest score at 2,000 L (version 0.1.0 chose 4,000 L);
- with 70% on one dimension and 10% on each of the others, the band is: technical 1,000 L; economic 2,000–3,000 L; environmental 2,000–3,000 L; structural 3,000–4,000 L, with the highest score at 4,000 L;
- with the objective weights of CRITIC — technical 35.7%, economic 21.5%, environmental 10.5%, structural 32.3%; the payback weighs nothing because no volume pays back — the band is 3,000–4,000 L, with the highest score at 4,000 L;
- SMAA-VIKOR (5,000 draws, seed 42) puts 2,000 L first in 39.6% of the draws, 3,000 L in 25.8% and 4,000 L in 17.7%: no volume is robust to the weights;
- the most reliable volume is still 12,000 L, and the hydraulic criterion of the tutorial (marginal gain of 1 %/m³) still gives 4,000 L.

The technical dimension now balances reliability, which rises with the volume, against storage efficiency, which falls; that is why a dominant technical weight leads to the smallest volume. The tutorial keeps the 4,000 L of the hydraulic criterion, and the manual section «Which volume to choose, after all» shows what that choice gives up and when the smaller volume is the defensible one.

## Documentation

The manual describes the eight criteria, the LCOW equation, the weight rule, the objective weights of CRITIC, the choice band and the weight of the system in the sections «Which volume to choose, after all», «Comparing many cases at once», «Multi-criteria decision» and «Error messages and what to do»; the section «The report, and what to declare in a paper» asks a study to report the band and its tolerance; the section «Version history and what changed» has the entry of this version. The interactive figure of the decision on the offline site has four dimension weights, the criterion shares and the choice band.

## What was verified and what was not

Verified: the multi-criteria numbers printed in the manual are recomputed by the program at every build of the manual and checked by the manual's automatic tests; the TOPSIS and the choice band computed in the site page were checked against the program with Node, with differences only from the rounding of the matrix.

Not verified at the time of writing: the installer of version 0.2.0, which had not been built. Its checks and its SHA-256 belong to the Zenodo record when it is published.

## Report a problem

State the version (0.2.0), the edition and the steps, and attach the `.triton` file. Contact: igorcmvaz@gmail.com.

## How to cite

Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Computational Platform for Rainwater Harvesting Simulation in Buildings* (version 0.2.0) [Computer software]. Federal University of Santa Catarina (UFSC). https://doi.org/10.5281/zenodo.23402915

Version 0.2.0 has no DOI of its own yet: cite the DOI of all versions, 10.5281/zenodo.23402915, which always resolves to the most recent one. Version 0.1.0 has the DOI 10.5281/zenodo.23402916; use it, with version 0.1.0, to reproduce a study made with that version. When a study uses the example rainfall, also credit Open-Meteo.com (CC BY 4.0) and Hersbach et al. (2020).
