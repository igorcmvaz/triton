"""Prepara, sem alterar os dados, as figuras usadas no manuscrito.

Os gráficos analíticos originais preservam títulos extensos para uso autônomo. Na
versão de periódico, esses supertítulos são redundantes com as legendas do artigo.
Este script remove apenas essa faixa superior, uniformiza a resolução e grava cópias
reproduzíveis em ``figuras_publicacao``.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "estudo_5_tipologias_residenciais" / "estudo_vaz" / "figuras"
OUTPUT = ROOT / "estudo_5_tipologias_residenciais" / "estudo_vaz" / "figuras_publicacao"

# Faixa superior (pixels na imagem original) que contém apenas o supertítulo.
CROP_TOP = {
    "fig17_climate_potential_degradation_map.png": 105,
    "fig7_optimal_storage_boxplots_grid_2x5.png": 85,
    "fig10_financial_payback_capex.png": 90,
    "matriz_multitipologia_co2_otimo_27_capitais.png": 78,
    "matriz_multitipologia_vpl_otimo_27_capitais.png": 72,
    "fig20_pareto_frontier_vpl_co2_payback.png": 82,
    "fig5_gcm_climate_model_uncertainty.png": 82,
    "fig9_regional_macro_analysis.png": 78,
    "fig11_spatial_tariffs_distribution_brasil.png": 88,
    "fig13_cost_benefit_breakdown_typologies.png": 78,
}

# Alguns supertítulos encostam visualmente nos títulos dos painéis. Em vez de
# recortar mais e arriscar perder "A)"/"B)", limpa-se somente a faixa residual.
WHITE_TOP = {
    "fig7_optimal_storage_boxplots_grid_2x5.png": 18,
    "fig20_pareto_frontier_vpl_co2_payback.png": 30,
    "fig5_gcm_climate_model_uncertainty.png": 30,
    "fig9_regional_macro_analysis.png": 30,
    "fig11_spatial_tariffs_distribution_brasil.png": 18,
    "fig13_cost_benefit_breakdown_typologies.png": 30,
}


def prepare_one(filename: str, crop_top: int) -> Path:
    source = SOURCE / filename
    if not source.exists():
        raise FileNotFoundError(source)
    with Image.open(source) as opened:
        image = opened.convert("RGB")
        image = image.crop((0, crop_top, image.width, image.height))
        clean_height = WHITE_TOP.get(filename, 0)
        if clean_height:
            image.paste("white", (0, 0, image.width, clean_height))
        # Leve correção para manter linhas e texto nítidos após redução no Word.
        image = ImageEnhance.Contrast(image).enhance(1.03)
        if image.width > 4200:
            height = round(image.height * 4200 / image.width)
            image = image.resize((4200, height), Image.Resampling.LANCZOS)
        OUTPUT.mkdir(parents=True, exist_ok=True)
        target = OUTPUT / filename
        image.save(target, format="PNG", dpi=(300, 300), optimize=True)
    return target


def main() -> None:
    for filename, crop_top in CROP_TOP.items():
        target = prepare_one(filename, crop_top)
        print(target)


if __name__ == "__main__":
    main()
