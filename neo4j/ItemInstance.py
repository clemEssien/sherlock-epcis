import re
class URI:
    """Provides a class for URI objects as defined in [EPCIS1.2, Section 6.4]

    Attributes:
        uri_str : str
            string representation of the URI.

    GS1 URI Syntax:
        "urn" : <Namespace Identifier> : <Namespace Specfic String> : <Scheme> : <Value>
        examples:
            "urn:epc:id:sgtin:0614141.107346.2018"
            "urn:epcglobal:cbv:bizstep:receiving"
    """

    def __init__(self, uri_str: str):
        """Creates a new URI instance from the given string"""
        self.uri_str: str = uri_str
        self._split_uri: "list[str]" = []
        self._is_split: bool = False
        if re.search("[a-z]+:[a-z]+:[a-z]+:[a-z]+:[a-z0-9.*]+", self.uri_str):
            self._split_uri = self.uri_str.split(":")
            self._is_split = True

    def __repr__(self) -> str:
        rep = "URI(" + self.uri_str + ")"
        return rep

    def __str__(self) -> str:
        return self.uri_str

    @property
    def prefix(self) -> str:
        """returns the URI's prefix"""
        if self._is_split:
            return "{}:{}:{}".format(
                self._split_uri[0], self._split_uri[1], self._split_uri[2]
            )
        return None

    @property
    def scheme(self) -> str:
        """returns the URI's scheme"""
        if self._is_split:
            return self._split_uri[3]
        return None

    @property
    def value(self) -> str:
        """returns the value stored in the URI"""
        if self._is_split:
            return self._split_uri[4]
        return None

class ItemInstance:
  def __init__(self, epc: URI = URI("")):
    self.epc = epc

  @property
  def epc_class(self) -> URI:
      return self._epc_class

  @epc_class.setter
  def epc_class(self, value: URI):
      if isinstance(value, str):
          value = URI(value)
      self._epc_class = value