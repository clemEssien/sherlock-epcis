from uuid import UUID, uuid4
import uuid


class User:
  # epc_class: epc.URI = epc.URI("")
  def __init__(self, id, name):
    self.id = id
    self.name = name