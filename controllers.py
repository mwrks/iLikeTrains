class PIDController:
    """
    Pengontrol PID (Closed-Loop) untuk sistem pengereman.
    Target setpoint: Kecepatan 0.
    """
    def __init__(self, kp, ki, kd, setpoint=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.integral = 0
        self.prev_error = 0

    def compute(self, current_value, dt):
        """Menghitung output gaya rem berdasarkan error."""
        error = self.setpoint - current_value
        
        # Suku Integral
        self.integral += error * dt
        
        # Anti-windup: membatasi nilai integral
        max_integral = 1000
        self.integral = max(-max_integral, min(max_integral, self.integral))
        
        # Suku Derivatif
        # Perubahan error per satuan waktu
        derivative = (error - self.prev_error) / dt
        
        # Output PID: P*error + I*integral + D*derivative
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        # Simpan error saat ini untuk perhitungan derivatif berikutnya
        self.prev_error = error
        
        # Output kontrol digunakan sebagai input untuk gaya rem
        return output

    def reset(self):
        """Mengatur ulang status internal controller."""
        self.integral = 0
        self.prev_error = 0

class OpenLoopController:
    """
    Pengontrol Open-Loop, memberikan gaya rem konstan.
    Tidak menggunakan feedback kecepatan.
    """
    def __init__(self, constant_brake_force):
        self.constant_brake_force = constant_brake_force

    def compute(self, current_value, dt):
        """Mengembalikan gaya rem konstan."""
        # Open-loop: mengembalikan gaya rem konstan terlepas dari kecepatan saat ini
        return self.constant_brake_force

    def reset(self):
        """Tidak ada yang perlu direset."""
        pass