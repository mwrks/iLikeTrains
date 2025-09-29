import math

class TrainPhysicsModel:
    """
    Model fisika kereta cepat, menghitung gaya resistif dan akselerasi.
    """
    def __init__(self, mass):
        # Massa total kereta (kg)
        self.mass = mass
        # Koefisien resistensi gelinding (Rolling Resistance)
        self.rollingResistance = 0.001
        # Koefisien gaya hambat udara (Air Drag Coefficient)
        self.airDragCoeff = 0.5
        # Luas permukaan frontal (m^2)
        self.frontalArea = 10 
        # Massa jenis udara (kg/m^3)
        self.airDensity = 1.225 
        # Gravitasi (m/s^2)
        self.g = 9.81
        # Gaya rem maksimum (Newton)
        self.maxBrakeForce = 800000 

    def calculate_resistive_forces(self, velocity):
        """Menghitung total gaya resistif (Rolling dan Drag)."""
        # Gaya Gelinding (Rolling Force)
        F_rolling = self.rollingResistance * self.mass * self.g
        
        # Gaya Hambat Udara (Air Drag Force)
        F_drag = 0.5 * self.airDensity * self.frontalArea * self.airDragCoeff * velocity**2
        
        return F_rolling, F_drag

    def calculate_acceleration(self, velocity, brake_force):
        """Menghitung akselerasi (decelerasi) total."""
        F_rolling, F_drag = self.calculate_resistive_forces(velocity)
        
        # Adaptive brake force at very low speeds (like in the original JS)
        adjusted_brake_force = brake_force
        if velocity < 5:
            # Mengurangi gaya rem secara linier saat kecepatan sangat rendah untuk mencegah overshoot/oscillasi.
            adjusted_brake_force *= (velocity / 5)
        
        # Total gaya resistif (Gaya rem + Gaya gelinding + Gaya hambat)
        # Tanda negatif karena ini adalah gaya yang memperlambat (deceleration)
        F_total = adjusted_brake_force + F_rolling + F_drag
        
        # Hukum Newton II: F = ma, maka a = F/m
        return -F_total / self.mass