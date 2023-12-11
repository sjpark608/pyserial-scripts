import serial
import random
import hashlib
import logging
from time import perf_counter
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

# ser = serial.Serial(port=PORT, baudrate=1000000, bytesize=8, parity="N", stopbits=1)
if __name__ == '__main__':
    cmd = None
    while cmd != 0:
        cmd = int(input("""
                menu
                ----
                 (0). exit
                 (1). simple test
                 (2). send 256 receive 256
                 (3). send 128, receive sum of 128
                """).strip())
        if cmd == 0:
            print('Exit program')
        elif cmd == 1:
            num = int(input("enter number to send: ").strip())
            txrx_byte(num)
        elif cmd ==2:
            for _ in range(1):
                txrx_256bytes()
        elif cmd ==3:
            for _ in range(128):
                tx256_rx256sum()
        else:
            print(f'Invalid cmd = {cmd}')

    print('===================================================')
