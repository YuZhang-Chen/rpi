# main.py
import time
import threading
from ultrasonic_module import UltrasonicGateController
from MotorController import MotorController

# 入口設備
ENTRANCE_TRIG = 26
ENTRANCE_ECHO = 19
ENTRANCE_MOTOR_PIN = 13

# 出口設備（假設使用另一組腳位）
EXIT_TRIG = 6
EXIT_ECHO = 5
EXIT_MOTOR_PIN = 11

def gate_handler(name, gate_sensor, gate_motor):
    print(f"🚦 [{name}] 開始監聽超聲波感測器...")
    try:
        while True:
            if gate_sensor.check_for_car():
                print(f"[{name}] 偵測到車輛")
                print("[ACTION] 和手機要照片")
                print("使用ocr模型識別車牌號碼")
                print("辨識出來的車牌傳給停車場管理系統")
                print("停車場管理系統回傳成功訊息")
                gate_motor.open_gate()
                time.sleep(1)  # 防止重複觸發
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"🔚 [{name}] 中止監聽")
    finally:
        gate_sensor.cleanup()
        gate_motor.cleanup()

if __name__ == "__main__":
    # 初始化感測器與馬達
    entrance_sensor = UltrasonicGateController(ENTRANCE_TRIG, ENTRANCE_ECHO, threshold_cm=50)
    entrance_motor = MotorController(ENTRANCE_MOTOR_PIN)

    exit_sensor = UltrasonicGateController(EXIT_TRIG, EXIT_ECHO, threshold_cm=50)
    exit_motor = MotorController(EXIT_MOTOR_PIN)

    # 建立兩個執行緒
    entrance_thread = threading.Thread(target=gate_handler, args=("入口", entrance_sensor, entrance_motor))
    exit_thread = threading.Thread(target=gate_handler, args=("出口", exit_sensor, exit_motor))

    # 啟動執行緒
    entrance_thread.start()
    exit_thread.start()

    # 主程式等待兩執行緒完成（實際上是無限循環，除非按 Ctrl+C）
    entrance_thread.join()
    exit_thread.join()
