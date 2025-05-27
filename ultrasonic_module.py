# ultrasonic_module.py
import time
import RPi.GPIO as GPIO

class UltrasonicGateController:
    def __init__(self, trig_pin, echo_pin, threshold_cm=30):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.threshold_cm = threshold_cm
        self.car_detected = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def measure_distance(self):
        # 發出超聲波
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)
        start = 0

        # 等待回音
        while GPIO.input(self.echo_pin) == 0:
            start = time.time()

        while GPIO.input(self.echo_pin) == 1:
            end = time.time()

        # 計算距離
        elapsed = end - start
        distance = (elapsed * 34300) / 2  # 單位：cm
        return distance

# ultrasonic_module.py
    def check_for_car(self):
        distance = self.measure_distance()
        print(f"[INFO] 距離: {distance:.2f} cm")
        if distance < self.threshold_cm:
            if not self.car_detected:
                self.car_detected = True
        else:
            self.car_detected = False

        return self.car_detected  # 加上這行

    # def on_car_detected(self):
    #     # 模擬控制馬達（目前還沒接上）
    #     print("[ACTION] 偵測到車輛！啟動閘門模擬...")
    #     return self.car_detected

    def cleanup(self):
        GPIO.cleanup()

