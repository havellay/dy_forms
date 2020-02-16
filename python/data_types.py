class DataType(object):
  pass

class TextDataType(DataType):
  def __init__(self, type=None):
    return

class NumberDataType(DataType):
  def __init__(self, type=None):
    return

class EnumeratedDataType(DataType):
  def __init__(self, type=None, values=None):
    return

def make_data_type_instance(definition_dict=None):
  known_data_types = {
    "text":TextDataType,
    "number":NumberDataType,
    "enumerated":EnumeratedDataType,
  }
  return known_data_types.get(
      definition_dict.get("type")
    )(**definition_dict)
