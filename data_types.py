class DataType(object):
  """
  All types of data that Fields can contain are derived from
  the DataType class.

  Each Field has a member data_type that it can use to check
  validity of input data. By having a separate instance of
  a DataType class for each field, other constraints such as
  size / length of data etc. may be enforced for each Field.
  
  A subordinate instance of DataType is one which doesn't have
  the full definition of the data type and will be superseded
  by a non subordinate data type instance. For example, a
  subordinate EnumeratedDataType instance will not have the
  full set of possible values that the enumerated type can
  hold, and so, cannot be expected to perform data ingestion
  or validation etc. Such subordinate fields exist as a place-
  holder for VALUE operators.
  """
  def __init__(self, type=None, subordinate=False):
    self.type=type
    self.subordinate=subordinate

  def to_string(self, value):
    return value.__str__()

  def is_subordinate(self):
    return self.subordinate

  def is_equal(self, value1, value2):
    return value1 == value2

class TextDataType(DataType):
  def process(self, value=None):
    return str(value)

class NumberDataType(DataType):
  def process(self, value=None):
    return float(value)

class EnumeratedDataType(DataType):
  def __init__(self, type=None, values=None, subordinate=False):
    self.type=type
    self.values=values
    self.subordinate=subordinate

  def process(self, value=None):
    if value in self.values:
      return value
    else:
      raise Exception("Unrecognized value")

def make_data_type_instance(definition_dict=None):
  known_data_types = {
    "text":TextDataType,
    "number":NumberDataType,
    "enumerated":EnumeratedDataType,
  }
  return known_data_types.get(
      definition_dict.get("type")
    )(**definition_dict)

