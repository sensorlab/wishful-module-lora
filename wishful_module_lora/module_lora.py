import logging
import random
import wishful_upis as upis
import wishful_framework as wishful_module
from wishful_framework.classes import exceptions

import time
import serial
from vesna import alh

__author__ = "Matevz Vucnik"
__copyright__ = "Copyright (c) 2017, Jozef Stefan Instiute"
__version__ = "0.1.0"
__email__ = "matevz.vucnik@ijs.si"


@wishful_module.build_module
class LoraModule(wishful_module.AgentModule):
    node = None
    freq = 868000000
    bw = 125
    sf = 7
    cr = "4_5"
    pwr = 6
    
    def __init__(self, dev):
        super(LoraModule, self).__init__()
        self.log = logging.getLogger('LoraModule')
        ser = serial.Serial(dev, 115200, timeout=1)
        self.node = alh.ALHTerminal(ser)

    @wishful_module.bind_function(upis.radio.get_radio_info)
    def get_radio_info(self, platform_id):
        return self.node.get("loraRadioInfo").text

    @wishful_module.bind_function(upis.radio.set_parameters)
    def set_parameters(self, params):
        set_sf = 0
        if 7 <= params['SF'] <= 12:
            self.sf = params['SF']
        else:
            set_sf = 1
        
        set_cr = 0
        crs = ['4_5', '4_6', '4_7', '4_8']
        if params['CR'] in crs:
            self.cr = params['CR']
        else:
            set_cr = 1

        return {"SF": set_sf, "CR": set_cr}

    @wishful_module.bind_function(upis.radio.set_tx_power)
    def set_tx_power(self, power):
        if 2 <= power <= 14:
            self.pwr = power
            return 0
        else:
            return 1

    @wishful_module.bind_function(upis.radio.set_rxchannel)
    def set_rxchannel(self, freq_Hz, bandwidth):
        if 860000000 <= freq_Hz <= 920000000:
            self.freq = freq_Hz
        else:
            return 1
        
        bws = [125, 250, 500]
        if bandwidth in bws:
            self.bw = bandwidth
            return 0
        else:
            return 1

    @wishful_module.bind_function(upis.radio.set_txchannel)
    def set_txchannel(self, freq_Hz, bandwidth):
        if 860000000 <= freq_Hz <= 920000000:
            self.freq = freq_Hz
        else:
            return 1
        
        bws = [125, 250, 500]
        if bandwidth in bws:
            self.bw = bandwidth
            return 0
        else:
            return 1

    @wishful_module.bind_function(upis.net.inject_frame)
    def inject_frame(self, iface, frame, is_layer_2_packet, tx_count=1, pkt_interval=1):
        if 1 <= len(str(frame)) <= 64:
            res = self.node.post("loraTxStart", frame, "frequency="+str(self.freq)+"&bw="+str(self.bw)+"&sf="+str(self.sf)+"&cr="+self.cr+"&pwr="+str(self.pwr))
            return res.text
        else:
            return "Frame size must be between 1 and 64 bytes!"

    @wishful_module.bind_function(upis.net.sniff_layer2_traffic)
    def sniff_layer2_traffic(self, iface, sniff_timeout):
        res = self.node.get("loraRxStart", "frequency="+str(self.freq)+"&bw="+str(self.bw)+"&sf="+str(self.sf)+"&cr="+self.cr)
        for i in range(sniff_timeout):
            res = self.node.get("loraRxRead")
            if res.text != "No packet received":
                break
            time.sleep(1)
        return res.text
