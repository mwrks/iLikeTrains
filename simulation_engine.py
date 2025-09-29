import numpy as np
from physics import TrainPhysicsModel
from controllers import PIDController, OpenLoopController

def simulate_braking(mass, initial_velocity, controller_type, controller_params):
    """
    Menjalankan simulasi pengereman kereta.

    :param mass: Massa total kereta (kg).
    :param initial_velocity: Kecepatan awal (m/s).
    :param controller_type: 'closed-loop' atau 'open-loop'.
    :param controller_params: Dictionary parameter (Kp, Ki, Kd) atau (constant_brake_force).
    :return: Dictionary berisi data simulasi (waktu, kecepatan, jarak, dll.).
    """
    dt = 0.01  # time step (seconds)
    max_time = 300  # max simulation time

    physics = TrainPhysicsModel(mass)
    
    # Inisialisasi controller
    if controller_type == 'closed-loop':
        kp, ki, kd = controller_params['kp'], controller_params['ki'], controller_params['kd']
        controller = PIDController(kp, ki, kd, setpoint=0)  # target velocity = 0
    elif controller_type == 'open-loop':
        constant_force = controller_params.get('constant_brake_force', 600000)
        controller = OpenLoopController(constant_force)
    else:
        raise ValueError("Invalid controller_type. Must be 'closed-loop' or 'open-loop'.")
    
    # Data list untuk menyimpan hasil simulasi
    time_list, velocity_list, distance_list, brake_force_list, acceleration_list = [], [], [], [], []
    
    v = initial_velocity  # m/s
    d = 0  # meters
    t = 0  # seconds
    stopping_time = None
    stopping_distance = None
    
    # Loop Simulasi Utama
    while t < max_time and v > 0.01:
        time_list.append(t)
        # Simpan kecepatan dalam km/h (seperti di kode JS)
        velocity_list.append(v * 3.6) 
        distance_list.append(d)
        
        # 1. Controller output
        control_output = controller.compute(v, dt)
        
        # 2. Hitung gaya rem yang diterapkan
        F_brake = 0
        if controller_type == 'closed-loop':
            # Gaya rem proporsional dengan output PID, dan dibatasi oleh F_max.
            # Menggunakan massa sebagai scaling factor (seperti di kode JS)
            F_brake = min(abs(control_output) * mass, physics.maxBrakeForce)
        else: # open-loop
            # Gaya rem adalah konstanta, dibatasi oleh F_max.
            F_brake = min(abs(control_output), physics.maxBrakeForce)

        brake_force_list.append(F_brake)
        
        # 3. Hitung akselerasi
        a = physics.calculate_acceleration(v, F_brake)
        acceleration_list.append(a)
        
        # 4. Update status menggunakan integrasi Euler
        v_next = v + a * dt
        v = max(0, v_next) # Kecepatan tidak boleh negatif
        d = d + v * dt
        t += dt
        
        # Deteksi berhenti
        if v <= 0.01 and stopping_time is None:
            stopping_time = t
            stopping_distance = d

    return {
        'time': np.array(time_list),
        'velocity': np.array(velocity_list),
        'distance': np.array(distance_list),
        'brake_force': np.array(brake_force_list),
        'acceleration': np.array(acceleration_list),
        'stopping_time': stopping_time,
        'stopping_distance': stopping_distance,
        'controller_type': controller_type
    }