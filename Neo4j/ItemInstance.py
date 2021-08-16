import re
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from JSONDeserialization import epcis_event as epcis

class ItemInstance:
  def __init__(self, epc: epcis.URI = epcis.URI("")):
    self.epc = epc

  @property
  def epc(self) -> epcis.URI:
      return self._epc

  @epc.setter
  def epc(self, value: epcis.URI):
      if isinstance(value, str):
          value = epcis.URI(value)
      self._epc = value