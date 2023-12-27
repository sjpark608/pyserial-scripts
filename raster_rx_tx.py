import serial
import random
import hashlib
import logging
from time import perf_counter,sleep
from dummy_raster_points import DUMMY_RASTER_IMAGE
from pymodbus import pymodbus_apply_logging_config
from pymodbus.client import ModbusSerialClient

from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse
_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PORT = "COM14" # change this for testing
PHASE_LEN = 128 #x-axis
AMPLITUDE_LEN = 128#y-axis

def gen_dummy_raster():
    phases = [[random.randint(0,255) for _ in range(AMPLITUDE_LEN)] for _ in range(PHASE_LEN)]
    # generate mxn matrix with x-axis represenst phase, y-axis represent amplitude of possible pd
    _logger.debug(f"{phases}")
    return phases

def gen_raster_md5(target_list):
    target_list_str = str(target_list)
    raster_hash = hashlib.md5(target_list_str.encode()).hexdigest()
    _logger.debug(f"MD5 Hash for the raster {raster_hash}")
    return raster_hash

def send_dummy_raster(phases):
    with serial.Serial() as ser:
        ser.baudrate=1000000
        ser.bytesize=8
        ser.parity="N"
        ser.stopbits=1
        ser.port=PORT

        for amplitudes in phases:
            for amplitude in amplitudes:
                _logger.debug(f"byte: {amplitude.to_bytes(1,'big')}")
                ser.write(amplitude.to_bytes(1,'big'))

def receive_dummy_raster():
    phases = [[0 for _ in range(AMPLITUDE_LEN)] for _ in range(PHASE_LEN)]
    with serial.Serial() as ser:
        ser.baudrate=1000000
        ser.bytesize=8
        ser.parity="N"
        ser.stopbits=1
        ser.port=PORT
        ser.timeout = 0.5

        for _ in range(PHASE_LEN):
            ser.read(AMPLITUDE_LEN)

def txrx_byte(num):
    with serial.Serial() as ser:
        ser.baudrate=1000000
        ser.bytesize=8
        ser.parity="N"
        ser.stopbits=1
        ser.port=PORT
        ser.open()

        _logger.info(f"byte: {num.to_bytes(1,'big')}")
        ser.write(num.to_bytes(1,'big'))
        res= ser.read(1)
        _logger.info(f"byte: {res}")

def txrx_256bytes():
        with serial.Serial() as ser:
            ser.baudrate=1000000
            ser.bytesize=8
            ser.parity="N"
            ser.stopbits=1
            ser.port=PORT
            ser.open()

            dummy_data = [random.randint(0,255) for _ in range(AMPLITUDE_LEN)]
            dummy_hash = gen_raster_md5(dummy_data)
            _logger.info(f"byte: {dummy_data}, hash: {dummy_hash}")
            ser.write(dummy_data)
            res= ser.read(256)
            res = [res_int for res_int in res]
            res_hash = gen_raster_md5(res)
            _logger.info(f"byte: {res}, res_hash {res_hash}")
            _logger.info(f"Is hash match? {res_hash==dummy_hash}")

def tx256_rx256sum():
        with serial.Serial() as ser:
            ser.baudrate=1000000
            ser.bytesize=8
            ser.parity="N"
            ser.stopbits=1
            ser.port=PORT
            ser.timeout = 0.5
            ser.open()

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

def send_dummy_raster():
    with serial.Serial() as ser:
        ser.baudrate=1000000
        ser.bytesize=8
        ser.parity="N"
        ser.stopbits=1
        ser.port=PORT
        ser.timeout = 0.5
        ser.open()

        dummy_data=DUMMY_RASTER_IMAGE
        _logger.info(f"Length of Bytes {len(dummy_data)}")
        t1 = perf_counter()
        ser.write(bytes(dummy_data))
        t2 = perf_counter()
        _logger.info(f"Time: {t2-t1}")

def read_channel(ch):
    client = ModbusSerialClient(
    "COM9",
    # framer=Framer.SOCKET,
    # timeout=10,
    # retries=3,
    # retry_on_empty=False,
    # close_comm_on_error=False,.
    # strict=True,
    baudrate=115200,
    bytesize=8,
    parity="N",
    stopbits=1,
    # handle_local_echo=False,
    )
    client.connect()
    ch_metric = client.read_holding_registers(5144+(ch*36),36,247)
    _logger.info(f"Ch Status: {ch_metric.registers[0]}")
    _logger.info(f"Ch Alarm: {ch_metric.registers[1]}")
    _logger.info(f"Ch Temperature: {ch_metric.registers[2]}")
    _logger.info(f"Ch Humidity: {ch_metric.registers[3]}")
    _logger.info(f"Ch Ultra Sound: {ch_metric.registers[4]}")
    _logger.info(f"Ch Peak PD: {ch_metric.registers[10]}")
    _logger.info(f"Ch Total PD: {ch_metric.registers[11]}")
    _logger.info(f"Ch Peak PD Bins: {ch_metric.registers[12:24]}")
    _logger.info(f"Ch Total PD Bins: {ch_metric.registers[24:36]}")
    client.close()

def update_raster_channel(ch):
    client = ModbusSerialClient(
    "COM9",
    # framer=Framer.SOCKET,
    # timeout=10,
    # retries=3,
    # retry_on_empty=False,
    # close_comm_on_error=False,.
    # strict=True,
    baudrate=115200,
    bytesize=8,
    parity="N",
    stopbits=1,
    # handle_local_echo=False,
    )
    client.connect()
    channel = client.read_holding_registers(5124,1,247)
    _logger.info(f"Current Raster Channel: {channel.registers[0]}")
    client.write_registers(5124,ch, 247)
    _logger.info(f"Updating channel to: {ch}")
    sleep(0.2)
    channel = client.read_holding_registers(5124,1,247)
    _logger.info(f"Current Raster Channel: {channel.registers[0]}")
    client.close()

def read_raster_through_modbus():
    client = ModbusSerialClient(
    "COM9",
    # framer=Framer.SOCKET,
    # timeout=10,
    # retries=3,
    # retry_on_empty=False,
    # close_comm_on_error=False,.
    # strict=True,
    baudrate=115200,
    bytesize=8,
    parity="N",
    stopbits=1,
    # handle_local_echo=False,
    )
    client.connect()
    raster_read = [[0 for row in range(128)] for col in range(128)]
    addrx = 16384
    t_1 = perf_counter()
    for col in raster_read:
        # 1 register holds two pixel values
        regs = client.read_holding_registers(addrx,64,247)
        for indx, reg in enumerate(regs):
            col[indx*2] = reg&0xFF
            col[indx*2+1] = reg>>8
        # increment address pointer by 64
        addrx+=64
    t_2 = perf_counter()
    print(f"raster = {raster_read}, time = {t_2-t_1}")
    client.close()

    with open("raster_modbus.txt", "a") as f:
        for col in raster_read:
            for row in col:
                f.write(f"{row},")
            f.write(f"\n")

# ser = serial.Serial(port=PORT, baudrate=1000000, bytesize=8, parity="N", stopbits=1)
if __name__ == '__main__':
    cmd = None
    while cmd != 0:
        cmd = int(input("""
                menu
                ----
                 (0). exit
                 (1). Send Dummy Raster
                 (2). Read Channel
                 (3). Update Raster Channel
                 (4). read raster from modbus
                """).strip())
        if cmd == 0:
            print('Exit program')
        elif cmd == 1:
            send_dummy_raster()
        elif cmd == 2:
            channel = int(input("select channel to read 0-7: ").strip())
            read_channel(channel)
        elif cmd == 3:
            channel = int(input("select channel to update raster 0-7: ").strip())
            update_raster_channel(channel)
        elif cmd == 4:
            read_raster_through_modbus()
        else:
            print(f'Invalid cmd = {cmd}')

    print('===================================================')
