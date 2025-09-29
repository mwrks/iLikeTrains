import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_summary_table(summary_data, control_type):
    """Mencetak ringkasan hasil ke konsol."""
    df = pd.DataFrame(summary_data)
    print(f"\n=======================================================")
    print(f"  RINGKASAN HASIL SIMULASI: {control_type.upper()}")
    print(f"=======================================================")
    print(df[['scenario', 'mass', 'velocity', 'stoppingTime', 'stoppingDistance']].to_markdown(index=False, floatfmt=(".0f", ".0f", ".0f", ".2f", ".0f")))
    print("-------------------------------------------------------\n")
    return df

def plot_comparison_bar(comparison_data):
    """Membuat grafik batang perbandingan Closed-Loop vs Open-Loop."""
    df_comp = pd.DataFrame(comparison_data)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(df_comp['loadCondition']))  # label lokasi
    width = 0.35  # lebar bar
    
    rects1 = ax.bar(x - width/2, df_comp['closedLoop'], width, label='Closed-Loop (PID)', color='#3b82f6')
    rects2 = ax.bar(x + width/2, df_comp['openLoop'], width, label='Open-Loop', color='#f97316')

    ax.set_ylabel('Jarak Pengereman (m)')
    ax.set_xlabel('Kondisi Beban (Massa)')
    ax.set_title('Perbandingan Jarak Pengereman: Closed-Loop vs Open-Loop (V₀ = 300 km/h)')
    ax.set_xticks(x)
    ax.set_xticklabels(df_comp['loadCondition'])
    ax.legend()
    
    # Menambahkan label nilai di atas bar
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()
    plt.show()

def plot_time_series(all_results, data_key, title, ylabel):
    """Membuat grafik time series (Kecepatan vs Waktu atau Jarak vs Waktu)."""
    
    # Filter data hanya untuk V0 = 300 km/h (seperti di kode JS)
    filtered_results = [r for r in all_results if r['initialVelocity'] == 300]
    
    plt.figure(figsize=(12, 7))
    colors = ['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6'] # warna dari kode JS

    for idx, result in enumerate(filtered_results):
        plt.plot(result['time'], result[data_key], 
                 label=result['loadCondition'], 
                 color=colors[idx % len(colors)], 
                 linewidth=2)

    plt.title(f'{title} - {result["controller_type"].capitalize()} (V₀ = 300 km/h)')
    plt.xlabel('Waktu (s)')
    plt.ylabel(ylabel)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title="Kondisi Beban")
    plt.show()