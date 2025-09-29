import pandas as pd
from simulation_engine import simulate_braking
from visualization import create_summary_table, plot_comparison_bar, plot_time_series, plot_brake_force

# --- Konfigurasi Parameter Simulasi ---
# PID Parameters (Closed-Loop) - Sama dengan nilai default di kode JS
PID_PARAMS = {
    'kp': 0.025,
    'ki': 0.0001,
    'kd': 0.1
}

# Open-Loop Parameters - Gaya Rem Konstan (N)
OPEN_LOOP_FORCE = 800000

# Massa Kereta (kg) - Sama dengan di kode JS
MASSES = [450000, 465000, 480000, 495000, 510000] 
LOAD_CONDITIONS = ['0% (Kosong)', '25%', '50%', '75%', '100% (Penuh)']

# Kecepatan Awal (km/h) - Sama dengan di kode JS
INITIAL_VELOCITIES_KMH = [300, 250, 200, 150] 

# Pilih Tipe Kontrol untuk dianalisis: 'closed-loop' atau 'open-loop'
CONTROL_TYPE = 'closed-loop' 

# -------------------------------------

def run_simulation_scenarios(control_type, pid_params, open_loop_force):
    """Menjalankan simulasi untuk semua skenario massa dan kecepatan."""
    all_results = []
    summary_data = []

    for mass_idx, mass in enumerate(MASSES):
        for v_kmh in INITIAL_VELOCITIES_KMH:
            v_ms = v_kmh / 3.6  # Konversi ke m/s
            
            # Siapkan parameter controller
            if control_type == 'closed-loop':
                controller_params = pid_params
            else:
                controller_params = {'constant_brake_force': open_loop_force}
            
            # Jalankan simulasi
            result = simulate_braking(mass, v_ms, control_type, controller_params)
            
            # Tambahkan metadata ke hasil simulasi
            result['mass'] = mass
            result['loadCondition'] = LOAD_CONDITIONS[mass_idx]
            result['initialVelocity'] = v_kmh
            
            all_results.append(result)
            
            # Siapkan data untuk ringkasan
            summary_data.append({
                'scenario': f"{LOAD_CONDITIONS[mass_idx]}, {v_kmh} km/h",
                'mass': mass / 1000, # dalam ton
                'velocity': v_kmh,
                'stoppingTime': result['stopping_time'],
                'stoppingDistance': result['stopping_distance'],
                'loadCondition': LOAD_CONDITIONS[mass_idx],
                'controlType': control_type
            })
            
    return all_results, summary_data

def run_comparison_analysis(pid_params, open_loop_force):
    """Menjalankan simulasi Closed-Loop dan Open-Loop untuk perbandingan (V0=300 km/h)."""
    comparison_data = []
    v_kmh = 300
    v_ms = v_kmh / 3.6

    for mass_idx, mass in enumerate(MASSES):
        load_condition = LOAD_CONDITIONS[mass_idx]

        # 1. Closed-Loop (PID)
        closed_result = simulate_braking(
            mass, v_ms, 'closed-loop', pid_params
        )

        # 2. Open-Loop (Konstanta)
        open_result = simulate_braking(
            mass, v_ms, 'open-loop', {'constant_brake_force': open_loop_force}
        )
        
        comparison_data.append({
            'loadCondition': load_condition,
            'closedLoop': closed_result['stopping_distance'],
            'openLoop': open_result['stopping_distance'],
            'closedTime': closed_result['stopping_time'],
            'openTime': open_result['stopping_time']
        })
        
    return comparison_data

# --- Main Execution ---
if __name__ == "__main__":
    print(f"Memulai Simulasi dengan Tipe Kontrol: {CONTROL_TYPE.upper()}...")
    
    # 1. Jalankan semua skenario untuk tipe kontrol yang dipilih
    results, summary = run_simulation_scenarios(CONTROL_TYPE, PID_PARAMS, OPEN_LOOP_FORCE)
    
    # 2. Tampilkan Ringkasan Hasil
    summary_df = create_summary_table(summary, CONTROL_TYPE)
        
    # --- NEW STABILITY CHART ---
    plot_brake_force(results)

    # 3. Buat Grafik Time Series
    plot_time_series(results, 'velocity', 'Grafik Kecepatan vs Waktu', 'Kecepatan (km/h)')
    plot_time_series(results, 'distance', 'Grafik Jarak vs Waktu', 'Jarak (m)')

    # 4. Jika Closed-Loop, jalankan dan tampilkan perbandingan
    if CONTROL_TYPE == 'closed-loop':
        print("\n--- Menjalankan Simulasi Open-Loop untuk Perbandingan (V0=300 km/h) ---")
        comparison_results = run_comparison_analysis(PID_PARAMS, OPEN_LOOP_FORCE)
        
        # 5. Tampilkan Grafik Perbandingan
        plot_comparison_bar(comparison_results)

    print("Simulasi Selesai. Grafik ditampilkan di jendela Matplotlib.")
    # main_simulation.py