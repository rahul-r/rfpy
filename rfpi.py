#!/usr/bin/env python3

import sys
import wiringpi

INPUT = 0
OUTPUT = 1
LOW = 0
HIGH = 1

repeat = 10


class Pulse:
    high = None
    low = None


class Protocol:
    pulse_len = None
    sync = Pulse()
    zero = Pulse()
    one = Pulse()


class RF(object):
    def __init__(self):
        self.pin = 0
        self.protocol = Protocol()
        self.protocol.pulse_len = 189
        self.protocol.sync.high = 1
        self.protocol.sync.low = 31
        self.protocol.zero.high = 1
        self.protocol.zero.low = 3
        self.protocol.one.high = 3
        self.protocol.one.low = 1

    def init(self, pin=0, pulse_len=189):
        self.pin = pin
        self.protocol.pulse_len = pulse_len
        if wiringpi.wiringPiSetup() != 0:
            print('Cannot initialize wiringPi')
            return False
        wiringpi.pinMode(self.pin, OUTPUT)
        return True

    def send(self, code, num_bits=24):
        """code: The code to send
           num_bits: Number of bits to send"""
        if type(code) != int:
            print('The parameter code must be an int, given {}'.format(type(code)))
            return
        print('Sending {}, {}'.format(code, self.protocol.pulse_len))
        bit_mask = pow(2, num_bits)
        for _ in range(repeat):
            code_bits = code
            for _ in range(num_bits):
                code_bits = code_bits << 1
                if (code_bits & bit_mask) == bit_mask:
                    self._transmit(self.protocol.one)
                    #print(1, end='')
                else:
                    self._transmit(self.protocol.zero)
                    #print(0, end='')
            self._transmit(self.protocol.sync)
            #print()

    def _transmit(self, pulse):        
        wiringpi.digitalWrite(self.pin, HIGH)
        wiringpi.delayMicroseconds(self.protocol.pulse_len * pulse.high)
        wiringpi.digitalWrite(self.pin, LOW)
        wiringpi.delayMicroseconds(self.protocol.pulse_len * pulse.low)
        

if __name__ == '__main__':
    code = int(sys.argv[1])
    rf = RF()
    rf.init()
    rf.send(code)
