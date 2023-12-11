import serial
import random
import hashlib
import logging
import threading
from time import perf_counter
from pymodbus import pymodbus_apply_logging_config
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException, ModbusIOException
from pymodbus.pdu import ExceptionResponse


_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

SER_PORT = "COM14" # change this for testing
MODBUS_PORT = "COM9"
PHASE_LEN = 128 #x-axis
AMPLITUDE_LEN = 128#y-axis




def read_modbus():
    with ModbusSerialClient(
        port = MODBUS_PORT,
        baudrate=115200,
        bytesize=8,
        parity="N",
        stopbits=1,
        ) as modbus:
        modbus_read=0
        modbus_err =0
        modbus.connect()
        while modbus_read<1:
            try:
                reg = modbus.read_holding_registers(2048,55,247)
                _logger.info(f"Regs 2048-2103: {reg.registers}")
                reg = modbus.read_holding_registers(2144,100,247)
                _logger.info(f"Regs 2144-2244: {reg.registers}")
                reg = modbus.read_holding_registers(2244,92,247)
                _logger.info(f"Regs 2244-2336: {reg.registers}")
                modbus_read+=1
            except Exception:
                modbus_err+=1
    _logger.info(f"Modbus Read performed: {modbus_read}")
    _logger.info(f"Modbus Error record: {modbus_err}")

def send_serial():
    with serial.Serial() as ser:
        ser.baudrate=1000000
        ser.bytesize=8
        ser.parity="N"
        ser.stopbits=1
        ser.port=SER_PORT
        ser.timeout = 0.5
        ser.open()
        raster_read=0
        raster_err=0
        while raster_read<1:
            try:
                dummy_data = [random.randint(0,255) for _ in range(AMPLITUDE_LEN*AMPLITUDE_LEN)]
                dummy_sum = sum(dummy_data)
                _logger.info(f"sum: {dummy_sum}")
                t1 = perf_counter()
                ser.write(bytes(dummy_data))
                res= ser.read(4)
                t2 = perf_counter()
                res = [res_int for res_int in res]
                res_sum = (res[0]<<24)+(res[1]<<16)+(res[2]<<8)+res[3]
                _logger.info(f"byte: {res}, res_hash {res_sum}")
                _logger.info(f"Time: {t2-t1}Is hash match? {res_sum==dummy_sum}")
                raster_read+=1
            except Exception:
                 raster_err+=1
        _logger.info(f"Raster Read performed: {raster_read}")
        _logger.info(f"Raster Error record: {raster_err}")

if __name__ == '__main__':
    thread_A = threading.Thread(target=read_modbus)
    thread_B = threading.Thread(target=send_serial)

    # Start the threads
    thread_A.start()
    thread_B.start()

    # Wait for both threads to finish
    thread_A.join()
    thread_B.join()