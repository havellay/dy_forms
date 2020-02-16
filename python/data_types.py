class DataType(object):
  def __init__(self, type=None, subordinate=False):
    self.type=type
    self.subordinate=subordinate

  def get_name(self):
    return self.type

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

