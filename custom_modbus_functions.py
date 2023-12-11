'''
Osensa Custom Modbus Functions classes
'''

import struct
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
from pymodbus.pdu import ModbusRequest, ModbusResponse, ModbusExceptions
# pymodbus2.5.3
from pymodbus.client import ModbusSerialClient
# from pymodbus.compat import int2byte
# pymodbus3.0.0
# from pymodbus.client import ModbusSerialClient as ModbusClient
# --------------------------------------------------------------------------- #
# configure the client logging
# --------------------------------------------------------------------------- #
import logging
_logger = logging.getLogger(__name__)



class SecurityUnlockResponse(ModbusResponse):
    '''
    Security Unlock Response Class
    '''
    function_code = 100
    _rtu_frame_size = 6

    def __init__(self, values=None, **kwargs):
        ModbusResponse.__init__(self, **kwargs)
        self.values = values or []

    def encode(self):
        """ Encodes response pdu

        :returns: The encoded packet message
        """
        result = int2byte(len(self.values) * 2)
        for register in self.values:
            result += struct.pack('>H', register)
        return result

    def decode(self, data):
        """ Decodes response pdu

        :param data: The packet data to decode
        """
        self.values = struct.unpack('>H', data)


class SecurityUnlockRequest(ModbusRequest):
    '''
    Security Unlock Request Class
    Args:
        sub_func: (int) sub function number
                    1 = Customer unlock
                    2 = factory unlock
                    3 = change password
        curr_pwd: (int) current password
        new_pwd: (int) new password
        unit: (int) slave id
    '''
    function_code = 100
    _rtu_frame_size = 10

    def __init__(self, sub_func=None, curr_pwd = None, new_pwd = None, **kwargs):
        ModbusRequest.__init__(self, **kwargs)
        self.sub_func = sub_func
        self.curr_pwd = curr_pwd
        self.new_pwd = new_pwd

    def encode(self):
        return struct.pack('>HHH', self.sub_func, self.curr_pwd, self.new_pwd)

    def decode(self, data):
        self.sub_func, self.curr_pwd, self.new_pwd  = struct.unpack('>HHH', data)

    def execute(self, context):
        '''
        Execute Security Unlock request
        '''
        if 0 > self.curr_pwd or self.curr_pwd > 65536:
            return self.doException(ModbusExceptions.IllegalValue)
        if not context.validate(self.function_code, self.sub_func, self.curr_pwd, self.new_pwd):
            return self.doException(ModbusExceptions.IllegalAddress)
        values = context.getValues(self.function_code, self.sub_func,
                                   self.curr_pwd, self.new_pwd)
        return SecurityUnlockResponse(values)


class SelectSlaveChannelRespsonse(ModbusResponse):
    '''
    Select Slave channel response class
    '''
    function_code = 55
    _rtu_frame_size = 10

    def __init__(self, values=None, **kwargs):
        ModbusResponse.__init__(self, **kwargs)
        self.values = values or []

    def encode(self):
        """ Encodes response pdu

        :returns: The encoded packet message
        """
        result = int2byte(len(self.values) * 2)
        for register in self.values:
            result += struct.pack('>H', register)
        return result

    def decode(self, data):
        """ Decodes response pdu

        :param data: The packet data to decode
        """
        self.values = struct.unpack('>HHH', data)


class SelectSlaveChannelRequest(ModbusRequest):
    '''
    select slave channel request
    Args:
        channel: (int) channel number to read
        start_address: (int) starting address to read
        num_of_regs: (int) number of registers to read
        unit_id: (int) slave id
    '''
    function_code = 55
    _rtu_frame_size = 10

    def __init__(self, channel=None, start_address=None, num_of_regs=None, **kwargs):
        ModbusRequest.__init__(self, **kwargs)
        self.channel = channel
        self.start_address = start_address
        self.num_of_regs = num_of_regs

    def encode(self):
        return struct.pack('>HHH', self.channel, self.start_address, self.num_of_regs)

    def decode(self, data):
        self.channel, self.start_address, self.num_of_regs = struct.unpack('>HHH', data)

    def execute(self, context):
        if 0 > self.start_address or self.start_address > 65536:
            return self.doException(ModbusExceptions.IllegalValue)
        if not context.validate(self.function_code,
                                self.channel,
                                self.start_address,
                                self.num_of_regs):
            return self.doException(ModbusExceptions.IllegalAddress)
        values = context.getValues(self.function_code,
                                   self.channel,
                                   self.start_address,
                                   self.num_of_regs)
        return SelectSlaveChannelRespsonse(values)


class FWUploadCommandResponse(ModbusResponse):
    '''
    FW upload command response
    '''
    function_code = 50
    _rtu_frame_size = 8

    def __init__(self, values=None, **kwargs):
        ModbusResponse.__init__(self, **kwargs)
        self.values = values or []

    def encode(self):
        """ Encodes response pdu

        :returns: The encoded packet message
        """
        result = int2byte(len(self.values) * 2)
        for register in self.values:
            result += struct.pack('>HH', register)
        return result

    def decode(self, data):
        """ Decodes response pdu

        :param data: The packet data to decode
        """
        self.values = struct.unpack('>HH', data)


class FWUploadCommandRequest(ModbusRequest):
    '''
    FW upload command request
    Args:
        channel: (int) channel number to upload firmware
        unit_id: (int) slave id
    '''
    function_code = 50
    _rtu_frame_size = 8

    def __init__(self, channel=None, **kwargs):
        ModbusRequest.__init__(self, **kwargs)
        self.channel = channel
        self.zeros = 0

    def encode(self):
        return struct.pack('>HH', self.channel, self.zeros)

    def decode(self, data):
        self.channel = struct.unpack('>HH', data)

    def execute(self, context):
        if 0 > self.channel or self.channel > 10:
            return self.doException(ModbusExceptions.IllegalValue)
        if not context.validate(self.function_code,self.channel, self.zeros):
            return self.doException(ModbusExceptions.IllegalAddress)
        values = context.getValues(self.function_code,
                                   self.channel,
                                   self.zeros)
        return FWUploadCommandResponse(values)


class RelayTestResponse(ModbusResponse):
    '''
    Relay Test reponse
    '''
    function_code = 25
    _rtu_frame_size = 8

    def __init__(self, values=None, **kwargs):
        ModbusResponse.__init__(self, **kwargs)
        self.values = values or []

    def encode(self):
        """ Encodes response pdu

        :returns: The encoded packet message
        """
        result = int2byte(len(self.values) * 2)
        for register in self.values:
            result += struct.pack('>HH', register)
        return result

    def decode(self, data):
        """ Decodes response pdu

        :param data: The packet data to decode
        """
        self.values = struct.unpack('>HH', data)


class RelayTestRequest(ModbusRequest):
    '''
    Relay Test request
    Args:
        relay_number: (int) select relay to test
        relay_test_enable: (int) set and clear relay
        unit_id: (int) slave id
    '''
    function_code = 25
    _rtu_frame_size = 8

    def __init__(self, relay_number=None, relay_test_enable=None, **kwargs):
        ModbusRequest.__init__(self, **kwargs)
        self.relay_number = relay_number
        self.relay_test_enable = relay_test_enable

    def encode(self):
        return struct.pack('>HH', self.relay_number, self.relay_test_enable)

    def decode(self, data):
        self.relay_number, self.relay_test_enable = struct.unpack('>HH', data)

    def execute(self, context):
        if 0 > self.relay_number or self.relay_number > 10:
            return self.doException(ModbusExceptions.IllegalValue)
        if not context.validate(self.function_code,self.relay_number, self.relay_test_enable):
            return self.doException(ModbusExceptions.IllegalAddress)
        values = context.getValues(self.function_code,
                                   self.relay_number,
                                   self.relay_test_enable)
        return RelayTestResponse(values)

if __name__ == "__main__":
    baud_rate = input('baud rate 9600, 19200, 38400, 57600, [115200], ... : ')
    baud_rate = 115200 if baud_rate == '' else int(baud_rate)

    serial_port = input('serial port ... : ')
    serial_port = '/dev/ttyUSB0' if serial_port == '' else serial_port

    modbus_timeout = input('modbus timeout in milliseconds [50] : ')
    modbus_timeout = 0.05 if modbus_timeout == '' else int(modbus_timeout) / 1000.0

    ftx_slave_id = int(input('ftx slave id 1..247 : ').strip())

    with ModbusClient(method='rtu', timeout=modbus_timeout,
                      port=serial_port,
                      baudrate=baud_rate,
                      parity='N',
                      stopbits=1,
                      bytesize=8) as modbus_client:

        # modbus_client.register(SecurityUnlockResponse)
        # request = SecurityUnlockRequest(sub_func=3, curr_pwd=65535, new_pwd=65535, unit=ftx_slave_id)
        # response = modbus_client.execute(request)
        # print(response)

        # modbus_client.register(RelayTestResponse)
        # request = RelayTestRequest(relay_number=2, relay_test_enable=0, unit=244)
        # response = modbus_client.execute(request)
        # print(response)

        modbus_client.register(FWUploadCommandResponse)
        request = FWUploadCommandRequest(channel=1, unit=ftx_slave_id)
        response = modbus_client.execute(request)
        print(response)
        check =1