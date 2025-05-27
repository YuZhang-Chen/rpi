import RPi.GPIO as GPIO
import time

class MotorController:
    def __init__(self, pin):
        self.pin = pin
        self.status = 'idle'

        GPIO.setmode(GPIO.BOARD)           # <== 加這行
        GPIO.setwarnings(False)          # <== 建議也加這行避免警告
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)  # 50Hz 的 PWM 頻率
        self.pwm.start(0)

    def is_busy(self):
        return self.status != 'idle'

    def set_angle(self, angle):
        # 將角度轉為 PWM 占空比
        duty = 2 + (angle / 18)
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)  # 等待馬達轉動到位
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)

    def gradual_set_angle(self, start_angle, end_angle, step=1, delay=0.005):
            """模擬緩慢轉動（速度由 delay 控制）"""
            if start_angle < end_angle:
                angles = range(start_angle, end_angle + 1, step)
            else:
                angles = range(start_angle, end_angle - 1, -step)

            for angle in angles:
                duty = 2 + (angle / 18)
                self.pwm.ChangeDutyCycle(duty)
                time.sleep(delay)

            self.pwm.ChangeDutyCycle(0)

    def open_gate(self):
        if self.is_busy():
            print("⚠️ 馬達忙碌中，跳過此次開門指令")
            return

        try:
            print("🚧 開門中... (轉90度)")
            self.status = 'opening'
            self.gradual_set_angle(0, 45, step=1)  # 模擬慢速開門
            time.sleep(5)
            self.gradual_set_angle(45, 0, step=1)  # 慢慢關回來
            print("✅ 柵欄已關閉")
        finally:
            self.status = 'idle'

    def cleanup(self):
        self.pwm.stop()

gate_Motor = MotorController(40)
gate_Motor.cleanup()
gate_Motor.open_gate()
