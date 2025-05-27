import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

SERVO_PIN = 40
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # 關閉訊號避免抖動

try:
    while True:
        print("➡️ 轉到 0 度")
        set_angle(0)
        time.sleep(1)

        print("➡️ 轉到 90 度")
        set_angle(90)
        time.sleep(1)

        print("➡️ 轉到 180 度")
        set_angle(180)
        time.sleep(1)

except KeyboardInterrupt:
    print("🛑 測試結束")
finally:
    pwm.stop()
    GPIO.cleanup()
