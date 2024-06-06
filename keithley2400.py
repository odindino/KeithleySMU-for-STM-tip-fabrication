import serial.tools.list_ports
import pyvisa as visa
import time


# get com port list
def get_com_list():
    com_list = []
    port_list = list(serial.tools.list_ports.comports())
    for port in port_list:
        com_list.append(port[0])
    return com_list


# make Keithley2400 class
class Keithley2400:
    def __init__(self):
        self.rm = visa.ResourceManager()
        self.login_status = 0
        self.output_status = 0

    def beep(self, freq, duration):
        self.keithley.write(f"SYST:BEEP:IMM {freq}, {duration}")
        time.sleep(0.3)
        # C4: 261.63Hz, # C4#: 277.18Hz, # D4: 293.66Hz, # D4#: 311.13Hz
        # E4: 329.63Hz, # F4: 349.23Hz, # F4#: 369.99Hz, # G4: 392.00Hz
        # G4#: 415.30Hz # A4: 440.00Hz, # A4#: 466.16Hz, # B4: 493.88Hz

    def idn_check(self):
        # if "KEITHLEY INSTRUMENTS INC.,MODEL 2400" in reading:
        if self.keithley.query("*IDN?").split(",")[1] == "MODEL 2400" or self.keithley.query("*IDN?").split(",")[1] == "MODEL 2410":
            return True

    def reset(self):
        self.keithley.write("*RST")

    def connect(self, com_port):
        self.com_port = com_port
        try:
            self.keithley = self.rm.open_resource(self.com_port)
            if self.idn_check():
                self.reset()
                print("Keithley 2400 connected")
                # G,G,G,#D
                self.beep(392, 1)
                self.beep(392, 1)
                self.beep(392, 1)
                self.beep(311.13, 1)

        except:
            try:
                resource_name = f"ASRL{self.com_port.replace('COM', '')}::INSTR"
                self.keithley = self.rm.open_resource(resource_name)
                if self.idn_check():
                    self.login_status = 1
                    self.reset()
                    print("Keithley 2400 connected")
                    # C,G,#F,G
                    self.beep(261.63*2, 0.3)
                    # self.beep(392*2, 0.3)
                    # self.beep(369.99*2, 0.3)
                    # self.beep(392*2, 0.3)
                    # time.sleep(1)
                    # self.beep(392*2, 0.8)
                    # time.sleep(0.5)
                    # self.beep(349.23*2, 0.6)
                    # time.sleep(0.5)
                    # self.beep(293.66*2, 0.8)

            except Exception as error:
                print("Keithley not connected")
                print(error)

    def set_remote_sense(self, switch):
        if switch == 1:
            self.keithley.write(":SYST:RSEN ON")
        elif switch == 0:
            self.keithley.write(":SYST:RSEN OFF")
        else:
            print("Invalid input")

    def set_measure_mode(self, mode):
        if mode == "VOLT":
            self.measure_mode = "VOLT"
            self.keithley.write(":SENS:FUNC 'VOLT'")
        elif mode == "CURR":
            self.measure_mode = "CURR"
            self.keithley.write(":SENS:FUNC 'CURR'")
        else:
            print("Invalid input")

    def set_source_mode(self, mode):
        if mode == "VOLT":
            self.source_mode = "VOLT"
            self.keithley.write(":SOUR:FUNC VOLT")
        elif mode == "CURR":
            self.source_mode = "CURR"
            self.keithley.write(":SOUR:FUNC CURR")
        else:
            print("Invalid input")

    def set_compliance(self, value):
        if self.measure_mode == "VOLT":
            self.keithley.write(f":SENS:VOLT:PROT {value}")
        elif self.measure_mode == "CURR":
            self.keithley.write(f":SENS:CURR:PROT {value}")
        else:
            print("Invalid input")

    def set_source(self, value):
        if self.source_mode == "VOLT":
            self.keithley.write(f":SOUR:VOLT {value}")
        elif self.source_mode == "CURR":
            self.keithley.write(f":SOUR:CURR {value}")
        else:
            print("Invalid input")

    def output(self, switch):
        if switch == 1:
            self.output_status = 1
            self.keithley.write(":OUTP ON")
        elif switch == 0:
            self.output_status = 0
            self.beep(261.63, 0.3)
            self.keithley.write(":OUTP OFF")
        else:
            print("Invalid input")

    # if

    # def read_data(self):
    #     reading = self.keithley.query(":READ?")
    #     if self.measure_mode == "VOLT":
    #         return float(reading.split(",")[0])
    #     elif self.measure_mode == "CURR":
    #         return float(reading.split(",")[1])
    #     else:
    #         print("Invalid input")

    def get_current(self):
        self.keithley.write(":SENS:FUNC 'CURR'")
        return_value = self.keithley.query(":READ?")
        curr = float(return_value.split(",")[1])
        return curr

    def disconnect(self):
        self.output(0)
        if self.login_status == 1:
            # G,F,D
            self.beep(392, 0.5)
            self.beep(349.23, 0.5)
            self.beep(293.66, 0.5)
        else:
            # F,F,F,D
            self.beep(349.23, 1)
            self.beep(349.23, 1)
            self.beep(349.23, 1)
            self.beep(293.66, 1)
        self.keithley.close()
        print("Keithley 2400 disconnected")
