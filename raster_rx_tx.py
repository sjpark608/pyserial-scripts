import serial
import random
import hashlib
import logging
_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PORT = "COM7" # change this for testing
PHASE_LEN = 360 #x-axis
AMPLITUDE_LEN = 256#y-axis

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

# ser = serial.Serial(port=PORT, baudrate=1000000, bytesize=8, parity="N", stopbits=1)
