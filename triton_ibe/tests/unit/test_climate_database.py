"""
Testes unitários para a Base de dados CLIMBra (climate_database.py).
Valida indexação, busca de cidades, leitura de 19 modelos CMIP6, cenários e recorte de datas.
"""

import numpy as np
import pytest

from triton.core.climate_database import (
    CLIMATE_MODELS,
    CLIMATE_SCENARIOS,
    get_climate_file_path,
    load_national_climate_series,
    find_matching_climate_city_name,
)


@pytest.mark.parametrize("city", [
    "São Paulo",
    "Brasília",
    "Florianópolis",
    "Manaus",
    "Salvador",
    "Cruzeiro do Sul",
    "Abaetetuba",
    "Goiânia",
])
def test_load_major_cities_historical(city):
    """Valida leitura da série histórica para diferentes capitais e municípios."""
    p_data, eff_start, eff_end, tot_days, sel_days, fpath = load_national_climate_series(
        city_name=city,
        model_name="ACCESS-CM2",
        scenario_key="HIST",
    )
    assert tot_days == 12419
    assert sel_days == tot_days
    assert eff_start == "01/01/1980"
    assert eff_end == "31/12/2013"
    assert len(p_data) == tot_days
    assert np.all(p_data >= 0.0)
    assert p_data.mean() > 0.5  # Média de chuva plausível em mm/dia


def test_load_different_gcm_models():
    """Valida se diferentes modelos climáticos são carregados com sucesso."""
    for model in ["ACCESS-CM2", "MIROC6", "MPI-ESM1-2", "EC-EARTH3"]:
        p_data, s_date, e_date, tot, sel, _ = load_national_climate_series(
            city_name="Florianópolis",
            model_name=model,
            scenario_key="HIST",
        )
        assert len(p_data) > 0
        assert np.isfinite(p_data.mean())


def test_load_future_scenarios():
    """Valida o carregamento dos cenários futuros contínuos SSP2-4.5 e SSP5-8.5 (2015-2100)."""
    for sc_key in ["SSP245", "SSP585"]:
        p_data, s_date, e_date, tot, sel, _ = load_national_climate_series(
            city_name="São Paulo",
            model_name="ACCESS-CM2",
            scenario_key=sc_key,
        )
        assert len(p_data) == 31411
        assert sel == tot
        assert s_date == "01/01/2015"
        assert e_date == "31/12/2100"


def test_date_slicing_temporal_filter():
    """Valida o recorte temporal personalizado por data inicial e final."""
    # Recorte de 10 anos exatos: 1990 a 1999 (10 anos = 3652 dias com anos bissextos 1992, 1996)
    p_data, s_date, e_date, tot, sel, _ = load_national_climate_series(
        city_name="Brasília",
        model_name="ACCESS-CM2",
        scenario_key="HIST",
        start_date_str="01/01/1990",
        end_date_str="31/12/1999",
    )
    assert s_date == "01/01/1990"
    assert e_date == "31/12/1999"
    assert sel == 3652
    assert sel < tot


def test_nonexistent_city_raises():
    """Valida que município inexistente gera FileNotFoundError informativo."""
    with pytest.raises(FileNotFoundError):
        load_national_climate_series("CidadeInexistenteXYZ123")


def test_climbra_db_integration():
    """Valida integração e leitura direta da base compilada (um banco por modelo)."""
    from triton.core.climate_database import get_climate_db_path, get_available_climate_cities
    import os

    db_path = get_climate_db_path()
    assert db_path is not None
    assert os.path.isfile(db_path)
    assert os.path.getsize(db_path) > 10 * 1024 * 1024  # uma parte tem ~40 MB; o banco único, ~820 MB

    cities = get_available_climate_cities()
    assert len(cities) == 652
    assert "São Paulo" in cities or "Sao Paulo" in cities or any("Paulo" in c for c in cities)

    # Leitura de teste e integridade
    p_data, s_date, e_date, tot, sel, fpath = load_national_climate_series(
        city_name="Florianópolis",
        model_name="INM-CM4",
        scenario_key="SSP245",
    )
    assert len(p_data) == 31411
    assert tot == 31411
    assert sel == 31411
    assert s_date == "01/01/2015"
    assert e_date == "31/12/2100"
    assert np.all(p_data >= 0.0)
