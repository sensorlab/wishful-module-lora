import logging
import random
import wishful_upis as upis
import wishful_framework as wishful_module
from wishful_framework.classes import exceptions

import time
from vesna import alh

__author__ = "Matevz Vucnik"
__copyright__ = "Copyright (c) 2017, Jozef Stefan Instiute"
__version__ = "0.1.0"
__email__ = "matevz.vucnik@ijs.si"


@wishful_module.build_module
class LoraModule(wishful_module.AgentModule):
    node = None
    
    def __init__(self, service, serial):
        super(LoraModule, self).__init__()
        self.log = logging.getLogger('LoraModule')
        self.node = alh.ALHWeb(service + "/communicator", serial)

    @wishful_module.bind_function(upis.radio.get_radio_info)
    def get_radio_info(self, platform_id):
        return self.node.get("loraRadioInfo").decode('ascii').strip()

    @wishful_module.bind_function(upis.radio.set_parameters)
    def set_parameters(self, params):
        return "hello"

    @wishful_module.bind_function(upis.radio.set_tx_power)
    def set_tx_power(self, params):
        return "hello"

    @wishful_module.bind_function(upis.radio.set_rxchannel)
    def set_rxchannel(self, params):
        return "hello"

    @wishful_module.bind_function(upis.radio.set_txchannel)
    def set_txchannel(self, params):
        return "hello"
