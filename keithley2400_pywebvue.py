import json
import serial.tools.list_ports
import time
import threading
import webview
from keithley2400 import Keithley2400

keithley = Keithley2400()
measuring = False


class Api:
    def __init__(self):
        self.keithley = Keithley2400()

    def get_ports(self):
        print("get_com_list")
        port_list = list(serial.tools.list_ports.comports())
        com_list = [port[0] for port in port_list]
        print(f"Available COM ports: {com_list}")
        return com_list

    def connect(self, port):
        print(f"Connecting to port: {port}")
        try:
            keithley.connect(port)
            print(f"Connection status: {keithley.login_status}")
            if keithley.login_status == 1:
                print("Keithley 2400 connected successfully")
                keithley.set_measure_mode("CURR")  # 設置測量模式為電流
            else:
                print("Failed to connect to Keithley 2400")
            return keithley.login_status == 1
        except Exception as e:
            print(f"Error connecting to Keithley 2400: {str(e)}")
            return False

    def disconnect(self):
        keithley.disconnect()
        return keithley.login_status == 0

    def start_measurement(self):
        global measuring
        measuring = True
        keithley.output(1)

    def pause_measurement(self):
        global measuring
        measuring = False
        keithley.output(0)

    def stop_measurement(self):
        global measuring
        measuring = False
        keithley.output(0)

    def set_voltage(self, voltage):
        keithley.set_source_mode("VOLT")
        keithley.set_source(voltage)

    def set_compliance(self, compliance):
        keithley.set_compliance(compliance / 1000)

    def set_sensing_mode(self, mode):
        if mode == "2wire":
            keithley.set_remote_sense(0)
        elif mode == "4wire":
            keithley.set_remote_sense(1)

    def measure_current(self):
        while True:
            if measuring:
                current = keithley.get_current()
                formatted_current = f"{current:.2E}"
                print(f"Measured current: {formatted_current}")
                webview.windows[0].evaluate_js(
                    f"updateCurrent({json.dumps(formatted_current)})")
            time.sleep(1)


if __name__ == '__main__':
    api = Api()

    t = threading.Thread(target=api.measure_current)
    t.daemon = True
    t.start()

# set the size of the window to 1020x680
    window = webview.create_window(
        'Keithley 2400 Control', url="http://localhost:5173/", js_api=api, width=1020, height=720)
    webview.start(debug=True)
