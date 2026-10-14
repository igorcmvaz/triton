import os
import sys
import time
import argparse
import glob
import gc
import shutil
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Generator
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np

# Adiciona o repositório ao PATH para importação do pacote triton
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from triton.core.parser import load_precipitation, format_triton_float
from triton.core.simulation import run_single_simulation, run_sweep_simulation


def _worker_process_file(task_tuple: Tuple) -> Dict[str, Any]:
    """
    Função executada em paralelo em cada worker do pool para processar 1 arquivo de chuva.
    """
    (
        file_path,
        mode,
        fixed_vol,
        max_vol,
        sweep_step,
        area,
        residents,
        demand_per_capita,
        share,
        runoff,
        discard_mm,
        delta_ideal,
        upper_tank_vol,
        upper_tank_used,
        pumping_threshold
    ) = task_tuple

    file_name = os.path.basename(file_path)

    try:
        precip_data = load_precipitation(file_path)
        tot_demand = demand_per_capita * residents

        if mode == "fixed":
            sim_res = run_single_simulation(
                precip_data=precip_data,
                lower_tank_vol=fixed_vol,
                area=area,
                runoff_coeff=runoff,
                discard_mm=discard_mm,
                total_demand_per_day=tot_demand,
                rainwater_share=share,
                upper_tank_vol=upper_tank_vol,
                upper_tank_used=upper_tank_used,
                pumping_threshold=pumping_threshold
            )

            return {
                "success": True,
                "file_name": file_name,
                "file_path": file_path,
                "mode": "fixed",
                "days_simulated": len(precip_data),
                "area_m2": area,
                "residents": residents,
                "demand_l_capita_day": demand_per_capita,
                "total_demand_l_day": tot_demand,
                "rainwater_share_pct": share * 100.0,
                "runoff_coeff": runoff,
                "discard_mm": discard_mm,
                "lower_tank_vol_l": fixed_vol,
                "potential_potable_savings_pct": round(sim_res.potential_potable_savings_pct, 2),
                "avg_pluvial_consumed_l_day": round(sim_res.avg_pluvial_consumed_l_day, 1),
                "avg_potable_consumed_l_day": round(sim_res.avg_potable_consumed_l_day, 1),
                "avg_spilled_l_day": round(sim_res.avg_spilled_l_day, 1),
                "pct_days_full_satisfaction": round(sim_res.pct_days_full_satisfaction, 1),
                "pct_days_partial_satisfaction": round(sim_res.pct_days_partial_satisfaction, 1),
                "pct_days_null_satisfaction": round(sim_res.pct_days_null_satisfaction, 1),
                "error": ""
            }

        else:  # mode == "sweep"
            sweep_res = run_sweep_simulation(
                precip_data=precip_data,
                lower_tank_max=max_vol,
                lower_tank_step=sweep_step,
                area=area,
                runoff_coeff=runoff,
                discard_mm=discard_mm,
                total_demand_per_day=tot_demand,
                rainwater_share=share,
                upper_tank_vol=upper_tank_vol,
                upper_tank_used=upper_tank_used,
                pumping_threshold=pumping_threshold,
                delta_ideal_threshold=delta_ideal,
                store_daily_details=False
            )

            # Localiza o resultado pontual do volume ótimo indicado
            opt_single = None
            if sweep_res.results_by_volume:
                for r in sweep_res.results_by_volume:
                    if r.lower_tank_vol == sweep_res.optimal_lower_tank_vol:
                        opt_single = r
                        break
                if opt_single is None:
                    opt_single = sweep_res.results_by_volume[-1]

            return {
                "success": True,
                "file_name": file_name,
                "file_path": file_path,
                "mode": "sweep",
                "days_simulated": len(precip_data),
                "area_m2": area,
                "residents": residents,
                "demand_l_capita_day": demand_per_capita,
                "total_demand_l_day": tot_demand,
                "rainwater_share_pct": share * 100.0,
                "runoff_coeff": runoff,
                "discard_mm": discard_mm,
                "optimal_lower_tank_l": sweep_res.optimal_lower_tank_vol,
                "potential_potable_savings_pct": round(sweep_res.optimal_potential_pct, 2) if sweep_res.optimal_potential_pct is not None else 0.0,
                "avg_pluvial_consumed_l_day": round(opt_single.avg_pluvial_consumed_l_day, 1) if opt_single else 0.0,
                "avg_potable_consumed_l_day": round(opt_single.avg_potable_consumed_l_day, 1) if opt_single else 0.0,
                "avg_spilled_l_day": round(opt_single.avg_spilled_l_day, 1) if opt_single else 0.0,
                "pct_days_full_satisfaction": round(opt_single.pct_days_full_satisfaction, 1) if opt_single else 0.0,
                "pct_days_partial_satisfaction": round(opt_single.pct_days_partial_satisfaction, 1) if opt_single else 0.0,
                "pct_days_null_satisfaction": round(opt_single.pct_days_null_satisfaction, 1) if opt_single else 0.0,
                "error": ""
            }

    except Exception as exc:
        return {
            "success": False,
            "file_name": file_name,
            "file_path": file_path,
            "mode": mode,
            "error": str(exc)
        }


def get_csv_headers(mode: str) -> List[str]:
    if mode == "sweep":
        return [
            "Arquivo_Chuva", "Dias_Simulados", "Area_m2", "Moradores",
            "Demanda_L_hab_dia", "Demanda_Total_L_dia", "Substituicao_Pluvial_pct",
            "Coef_Escoamento", "Descarte_mm", "Volume_Otimo_Reservatorio_L",
            "Potencial_Economia_Potavel_pct", "Consumo_Pluvial_Medio_L_dia",
            "Consumo_Potable_Rede_Medio_L_dia", "Extravasamento_Medio_L_dia",
            "Atendimento_Total_Dias_pct", "Atendimento_Parcial_Dias_pct", "Atendimento_Nulo_Dias_pct"
        ]
    else:
        return [
            "Arquivo_Chuva", "Dias_Simulados", "Area_m2", "Moradores",
            "Demanda_L_hab_dia", "Demanda_Total_L_dia", "Substituicao_Pluvial_pct",
            "Coef_Escoamento", "Descarte_mm", "Volume_Reservatorio_Fixo_L",
            "Potencial_Economia_Potavel_pct", "Consumo_Pluvial_Medio_L_dia",
            "Consumo_Potable_Rede_Medio_L_dia", "Extravasamento_Medio_L_dia",
            "Atendimento_Total_Dias_pct", "Atendimento_Parcial_Dias_pct", "Atendimento_Nulo_Dias_pct"
        ]


def format_result_row(r: Dict[str, Any], mode: str) -> str:
    vol_val = r.get("optimal_lower_tank_l") if mode == "sweep" else r.get("lower_tank_vol_l")
    row = [
        str(r.get("file_name", "")),
        str(r.get("days_simulated", 0)),
        format_triton_float(r.get("area_m2", 0.0), 1),
        str(r.get("residents", 0)),
        format_triton_float(r.get("demand_l_capita_day", 0.0), 0),
        format_triton_float(r.get("total_demand_l_day", 0.0), 0),
        format_triton_float(r.get("rainwater_share_pct", 0.0), 1),
        format_triton_float(r.get("runoff_coeff", 0.0), 2),
        format_triton_float(r.get("discard_mm", 0.0), 1),
        format_triton_float(vol_val, 0),
        format_triton_float(r.get("potential_potable_savings_pct", 0.0), 2),
        format_triton_float(r.get("avg_pluvial_consumed_l_day", 0.0), 1),
        format_triton_float(r.get("avg_potable_consumed_l_day", 0.0), 1),
        format_triton_float(r.get("avg_spilled_l_day", 0.0), 1),
        format_triton_float(r.get("pct_days_full_satisfaction", 0.0), 1),
        format_triton_float(r.get("pct_days_partial_satisfaction", 0.0), 1),
        format_triton_float(r.get("pct_days_null_satisfaction", 0.0), 1)
    ]
    return ";".join(row)


def result_to_dict_typed(r: Dict[str, Any], mode: str) -> Dict[str, Any]:
    vol_val = r.get("optimal_lower_tank_l") if mode == "sweep" else r.get("lower_tank_vol_l")
    vol_col = "Volume_Otimo_Reservatorio_L" if mode == "sweep" else "Volume_Reservatorio_Fixo_L"
    return {
        "Arquivo_Chuva": str(r.get("file_name", "")),
        "Dias_Simulados": int(r.get("days_simulated", 0)),
        "Area_m2": float(r.get("area_m2", 0.0)),
        "Moradores": int(r.get("residents", 0)),
        "Demanda_L_hab_dia": float(r.get("demand_l_capita_day", 0.0)),
        "Demanda_Total_L_dia": float(r.get("total_demand_l_day", 0.0)),
        "Substituicao_Pluvial_pct": float(r.get("rainwater_share_pct", 0.0)),
        "Coef_Escoamento": float(r.get("runoff_coeff", 0.0)),
        "Descarte_mm": float(r.get("discard_mm", 0.0)),
        vol_col: float(vol_val) if vol_val is not None else 0.0,
        "Potencial_Economia_Potavel_pct": float(r.get("potential_potable_savings_pct", 0.0)),
        "Consumo_Pluvial_Medio_L_dia": float(r.get("avg_pluvial_consumed_l_day", 0.0)),
        "Consumo_Potable_Rede_Medio_L_dia": float(r.get("avg_potable_consumed_l_day", 0.0)),
        "Extravasamento_Medio_L_dia": float(r.get("avg_spilled_l_day", 0.0)),
        "Atendimento_Total_Dias_pct": float(r.get("pct_days_full_satisfaction", 0.0)),
        "Atendimento_Parcial_Dias_pct": float(r.get("pct_days_partial_satisfaction", 0.0)),
        "Atendimento_Nulo_Dias_pct": float(r.get("pct_days_null_satisfaction", 0.0))
    }


def init_results_csv(file_path: str, mode: str):
    """Inicializa o arquivo CSV criando a pasta de destino e escrevendo o cabeçalho."""
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    headers = get_csv_headers(mode)
    with open(file_path, "w", encoding="latin1", errors="replace") as f:
        f.write(";".join(headers) + "\n")


def append_batch_csv(results_batch: List[Dict[str, Any]], file_path: str, mode: str):
    """Adiciona um lote de resultados ao arquivo CSV de maneira otimizada."""
    lines = [format_result_row(r, mode) for r in results_batch]
    with open(file_path, "a", encoding="latin1", errors="replace") as f:
        f.write("\n".join(lines) + "\n")


def write_parquet_chunk(results_batch: List[Dict[str, Any]], mode: str, chunk_path: str):
    """Grava um lote de resultados diretamente em um arquivo Parquet intermediário."""
    import pandas as pd
    os.makedirs(os.path.dirname(os.path.abspath(chunk_path)), exist_ok=True)
    typed_dicts = [result_to_dict_typed(r, mode) for r in results_batch]
    df = pd.DataFrame(typed_dicts)
    df.to_parquet(chunk_path, index=False, compression="snappy")


def merge_parquet_chunks(chunk_paths: List[str], final_parquet_path: str):
    """Consolida múltiplos arquivos Parquet intermediários em um único arquivo Parquet final."""
    import pandas as pd
    if not chunk_paths:
        return
    dfs = [pd.read_parquet(cp) for cp in chunk_paths]
    final_df = pd.concat(dfs, ignore_index=True)
    os.makedirs(os.path.dirname(os.path.abspath(final_parquet_path)), exist_ok=True)
    final_df.to_parquet(final_parquet_path, index=False, compression="snappy")


def run_mass_simulations(
    input_dir: str,
    output_csv: str,
    mode: str = "sweep",
    fixed_vol: float = 5000.0,
    max_vol: float = 10000.0,
    sweep_step: float = 250.0,
    areas: List[float] = None,
    residents_list: List[int] = None,
    demands: List[float] = None,
    shares: List[float] = None,
    runoff: float = 0.75,
    discard: float = 2.0,
    delta_ideal: float = 5.0,
    workers: int = None,
    output_format: str = "csv",
    batch_size: int = 10000,
    cool_down_secs: float = 0.0
):
    """
    Executa simulação paralela de alta performance com gerenciamento de memória em streaming e suporte a Parquet.
    """
    if areas is None:
        areas = [100.0]
    if residents_list is None:
        residents_list = [4]
    if demands is None:
        demands = [200.0]
    if shares is None:
        shares = [0.40]

    # Busca todos os arquivos de precipitação (.csv e .txt)
    pattern_csv = os.path.join(input_dir, "**", "*.csv")
    pattern_txt = os.path.join(input_dir, "**", "*.txt")
    files = sorted(list(set(glob.glob(pattern_csv, recursive=True) + glob.glob(pattern_txt, recursive=True))))

    if not files:
        if os.path.isfile(input_dir):
            files = [input_dir]
        else:
            files = sorted(glob.glob(input_dir))

    total_files = len(files)
    if total_files == 0:
        print(f"[x] Nenhum arquivo de precipitação encontrado em: {input_dir}")
        return

    # Monta a grade de tarefas
    tasks = []
    for fpath in files:
        for area in areas:
            for res in residents_list:
                for dem in demands:
                    for sh in shares:
                        sh_val = sh / 100.0 if sh > 1.0 else sh
                        tasks.append((
                            fpath, mode, fixed_vol, max_vol, sweep_step,
                            area, res, dem, sh_val, runoff, discard,
                            delta_ideal, 500.0, False, 375.0
                        ))

    total_tasks = len(tasks)
    
    # Define limite de workers de CPU para evitar superaquecimento térmico
    cpu_cores = os.cpu_count() or 4
    num_workers = workers or max(1, cpu_cores - 1)

    # Configuração de caminhos de saída
    save_csv = output_format.lower() in ["csv", "both"]
    save_parquet = output_format.lower() in ["parquet", "both"]

    base_output_no_ext = os.path.splitext(output_csv)[0]
    final_csv_path = base_output_no_ext + ".csv"
    final_parquet_path = base_output_no_ext + ".parquet"
    chunks_dir = os.path.join(os.path.dirname(os.path.abspath(output_csv)), f"_tmp_parquet_chunks_{int(time.time())}")

    print("=" * 90)
    print("TRITON 5 -- MOTOR DE SIMULACAO PARALELA MASSIVA MULTI-CORE (STREAMING & PARQUET)")
    print("=" * 90)
    print(f" [+] Arquivos de Chuva Encontrados: {total_files:,}")
    print(f" [*] Configuracoes Fatoriais: {total_tasks // total_files:,} por arquivo")
    print(f" [*] Total de Simulacoes a Executar: {total_tasks:,}")
    print(f" [*] Modo de Operacao: {'VARREDURA (Volume Otimo Indicado)' if mode == 'sweep' else 'VOLUME FIXO (' + str(fixed_vol) + ' L)'}")
    print(f" [*] Processamento Paralelo: {num_workers} nucleos de CPU (Headroom OS: {max(0, cpu_cores - num_workers)} nucleos)")
    print(f" [*] Formato de Saida: {output_format.upper()} | Tamanho do Lote RAM: {batch_size:,} sim/lote")
    print("=" * 90)

    if save_csv:
        print(f"[+] Inicializando cabeçalho CSV em: {final_csv_path}")
        init_results_csv(final_csv_path, mode)

    start_time = time.time()
    completed_count = 0
    errors_count = 0
    parquet_chunk_paths = []
    
    chunk_buffer: List[Dict[str, Any]] = []
    chunk_index = 0

    def flush_chunk(is_final=False):
        nonlocal chunk_buffer, chunk_index, parquet_chunk_paths
        if not chunk_buffer:
            return

        chunk_index += 1
        
        # 1. Salva em CSV
        if save_csv:
            append_batch_csv(chunk_buffer, final_csv_path, mode)

        # 2. Salva em Parquet Intermediário
        if save_parquet:
            chunk_file = os.path.join(chunks_dir, f"part_{chunk_index:05d}.parquet")
            write_parquet_chunk(chunk_buffer, mode, chunk_file)
            parquet_chunk_paths.append(chunk_file)

        # 3. Limpa a RAM e força Coleta de Lixo
        chunk_buffer.clear()
        gc.collect()

        if cool_down_secs > 0 and not is_final:
            time.sleep(cool_down_secs)

    # Execução Streaming em Bounded Queue (evita alocar todos os Futures na RAM de uma só vez)
    max_in_flight = max(1, num_workers * 2)
    task_iter = iter(tasks)
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        active_futures = {}

        # Preenche a fila inicial de tarefas ativas
        for _ in range(max_in_flight):
            try:
                task = next(task_iter)
                fut = executor.submit(_worker_process_file, task)
                active_futures[fut] = task
            except StopIteration:
                break

        last_print_time = time.time()

        while active_futures:
            # Aguarda a conclusão de pelo menos uma tarefa ativa
            done_futures = []
            for fut in list(active_futures.keys()):
                if fut.done():
                    done_futures.append(fut)

            if not done_futures:
                # Breve pausa para não saturar a CPU na checagem de status
                time.sleep(0.005)
                continue

            for fut in done_futures:
                del active_futures[fut]
                completed_count += 1

                res = fut.result()
                if res.get("success"):
                    chunk_buffer.append(res)
                else:
                    errors_count += 1

                # Submete uma nova tarefa para manter a fila cheia
                try:
                    next_task = next(task_iter)
                    new_fut = executor.submit(_worker_process_file, next_task)
                    active_futures[new_fut] = next_task
                except StopIteration:
                    pass

                # Se o lote em RAM atingir o limite, descarrega no disco
                if len(chunk_buffer) >= batch_size:
                    flush_chunk()

                # Atualiza indicador de progresso no terminal
                now = time.time()
                if now - last_print_time >= 0.5 or completed_count == total_tasks:
                    elapsed = now - start_time
                    speed = completed_count / elapsed if elapsed > 0 else 0
                    pct = (completed_count / total_tasks) * 100.0
                    eta_sec = (total_tasks - completed_count) / speed if speed > 0 else 0
                    file_info = f" ({res.get('file_name', '')})" if res.get("file_name") else ""
                    sys.stdout.write(
                        f"\rProgresso: {completed_count:,}/{total_tasks:,} [{pct:.1f}%] | "
                        f"Velocidade: {speed:.1f} sim/s | ETA: {eta_sec:.0f}s{file_info}"
                    )
                    sys.stdout.flush()
                    last_print_time = now

    # Descarrega o lote final remanescente
    flush_chunk(is_final=True)
    sys.stdout.write("\n")

    # Se exportação em Parquet foi selecionada, realiza a união consolidada dos arquivos intermediários
    if save_parquet and parquet_chunk_paths:
        print(f"[+] Consolidadando {len(parquet_chunk_paths)} arquivos Parquet intermediários em: {final_parquet_path}...")
        merge_parquet_chunks(parquet_chunk_paths, final_parquet_path)
        # Remove a pasta temporária de chunks
        if os.path.exists(chunks_dir):
            shutil.rmtree(chunks_dir, ignore_errors=True)

    total_elapsed = time.time() - start_time

    print("=" * 90)
    print(f"[OK] PROCESSAMENTO CONCLUIDO COM SUCESSO EM {total_elapsed:.2f} SEGUNDOS!")
    print(f"     * Total de Simulacoes Concluidas: {(completed_count - errors_count):,}")
    print(f"     * Falhas/Erros: {errors_count:,}")
    print(f"     * Taxa Media de Desempenho: {((completed_count - errors_count) / total_elapsed):,.1f} simulacoes/segundo")
    if save_csv:
        print(f"     * Arquivo Final CSV: {final_csv_path}")
    if save_parquet:
        print(f"     * Arquivo Final Parquet Consolidado: {final_parquet_path}")
    print("=" * 90)


def main():
    parser = argparse.ArgumentParser(
        description="Triton — Executor Paralelo de Simulações Massivas em Streaming & Suporte Parquet."
    )
    parser.add_argument("--input-dir", "-i", required=True, help="Diretório contendo os arquivos de precipitação (.csv ou .txt).")
    parser.add_argument("--output", "-o", default="resultado_simulacoes_massivas.csv", help="Caminho do arquivo de saída (CSV ou Parquet).")
    parser.add_argument("--mode", choices=["sweep", "fixed"], default="sweep", help="Modo de simulação: 'sweep' (varredura com volume ótimo) ou 'fixed' (volume fixo).")
    parser.add_argument("--fixed-vol", type=float, default=5000.0, help="Volume do reservatório em Litros no modo 'fixed'.")
    parser.add_argument("--max-vol", type=float, default=10000.0, help="Volume máximo do reservatório em Litros no modo 'sweep'.")
    parser.add_argument("--step-vol", type=float, default=250.0, help="Passo de incremento de volume no modo 'sweep'.")
    parser.add_argument("--area", nargs="+", type=float, default=[100.0], help="Área de captação (m²). Aceita um ou múltiplos valores.")
    parser.add_argument("--residents", nargs="+", type=int, default=[4], help="Número de moradores. Aceita um ou múltiplos valores.")
    parser.add_argument("--demand", nargs="+", type=float, default=[200.0], help="Demanda per capita (L/hab/dia). Aceita um ou múltiplos valores.")
    parser.add_argument("--share", nargs="+", type=float, default=[40.0], help="Percentual de substituição pluvial (%%). Aceita um ou múltiplos valores.")
    parser.add_argument("--runoff", type=float, default=0.75, help="Coeficiente de escoamento superficial C.")
    parser.add_argument("--discard", type=float, default=2.0, help="Descarte de escoamento inicial (first flush em mm).")
    parser.add_argument("--delta-ideal", type=float, default=5.0, help="Limiar de indicação do volume ótimo (%%/m³).")
    parser.add_argument("--workers", "-w", type=int, default=None, help="Número de núcleos de CPU para processamento paralelo.")
    parser.add_argument("--format", choices=["csv", "parquet", "both"], default="csv", help="Formato de exportação: 'csv', 'parquet' ou 'both'.")
    parser.add_argument("--batch-size", type=int, default=10000, help="Tamanho do lote de simulações mantidas na RAM antes do salvamento incremental.")
    parser.add_argument("--cool-down", type=float, default=0.0, help="Pausa de descompressão térmica (segundos) entre o salvamento de lotes.")

    args = parser.parse_args()

    run_mass_simulations(
        input_dir=args.input_dir,
        output_csv=args.output,
        mode=args.mode,
        fixed_vol=args.fixed_vol,
        max_vol=args.max_vol,
        sweep_step=args.step_vol,
        areas=args.area,
        residents_list=args.residents,
        demands=args.demand,
        shares=args.share,
        runoff=args.runoff,
        discard=args.discard,
        delta_ideal=args.delta_ideal,
        workers=args.workers,
        output_format=args.format,
        batch_size=args.batch_size,
        cool_down_secs=args.cool_down
    )


if __name__ == "__main__":
    main()
