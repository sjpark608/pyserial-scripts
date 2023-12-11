from pymodbus import pymodbus_apply_logging_config
from pymodbus.client import ModbusSerialClient
import serial
import random
import hashlib
from pymodbus.exceptions import ModbusException, ModbusIOException
from pymodbus.pdu import ExceptionResponse
import logging
from time import perf_counter
_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PORT = "COM14" # change this for testing

# def tx256_rx256sum():
#         with serial.Serial() as ser:
#             ser.baudrate=1000000
#             ser.bytesize=8
#             ser.parity="N"
#             ser.stopbits=1
#             ser.port=PORT
#             ser.timeout = 0.5
#             ser.open()

#             dummy_data = [random.randint(0,255) for _ in range(128)]
#             dummy_sum = sum(dummy_data)
#             _logger.info(f"byte: {dummy_data}, sum: {dummy_sum}")
#             t1 = perf_counter()
#             ser.write(bytes(dummy_data))
#             res= ser.read(2)
#             t2 = perf_counter()
#             res = [res_int for res_int in res]
#             res_sum = res[0]*256+res[1]
#             _logger.info(f"byte: {res}, res_hash {res_sum}")
#             _logger.info(f"Time: {t2-t1}Is hash match? {res_sum==dummy_sum}")


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
print("connect to server")
client.connect()


cnt = 0
err_cnt=0
while cnt<100:
    cnt+=1
    try:
        reg = client.read_holding_registers(2048,55,247)
        print(reg.registers)
        reg = client.read_holding_registers(2144,100,247)
        print(reg.registers)
        reg = client.read_holding_registers(2244,92,247)
        print(reg.registers)
    except:
        err_cnt +=1

print(err_cnt)