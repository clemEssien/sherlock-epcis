class ItemClass:
  def __init__(self, epc_class: URI = URI("")):
    self.epc_class = epc_class

  @property
  def epc_class(self) -> URI:
      return self._epc_class

  @epc_class.setter
  def epc_class(self, value: URI):
      if isinstance(value, str):
          value = URI(value)
      self._epc_class = value