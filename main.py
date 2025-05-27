import time
from ultrasonic_module import UltrasonicGateController
from MotorController import MotorController

# gate_Ultrasonic = UltrasonicGateController(26,19) #trig = 37 echo = 35
gate_Motor = MotorController(24) # 18
exit_Ultrasonic = UltrasonicGateController(5,6) #trig = 29 echo = 31
exit_Motor = MotorController(25) # 22


def extract_plate_text(image):
    print('使用ocr模型識別車牌號碼')
    print('辨識出來的車牌傳給停車場管理系統')
    print('停車場管理系統回傳成功訊息')
    time.sleep(0.05)
    gate_Motor.open_gate()
    time.sleep(0.05)

def getphoto():
    print('[ACTION] 和手機要照片')
    image = 123  # 模擬圖片
    extract_plate_text(image)

def wait_for_car(gate):
    car_detected = False
    while not car_detected:
        car_detected = gate.check_for_car()
        time.sleep(0.1)
    return car_detected

def run_system():
    try:
        print("🚦 start scanning ...")
        gate = UltrasonicGateController(26,19)
        while True:
            if wait_for_car(gate):
                getphoto()
    except KeyboardInterrupt:
        print("🔚 結束測試...")
    finally:
        gate.cleanup()
        gate_Motor.cleanup()

if __name__ == "__main__":
    run_system()
