import re
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from JSONDeserialization import epcis_event as epc

class ItemInstance:
  def __init__(self, epc: epc.URI = epc.URI("")):
    self.epc = epc

  @property
  def epc_class(self) -> epc.URI:
      return self._epc_class

  @epc_class.setter
  def epc_class(self, value: epc.URI):
      if isinstance(value, str):
          value = epc.URI(value)
      self._epc_class = value