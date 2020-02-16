
class Operator(object):
  def __init__(self):
    return

class EqualOperator(Operator):
  def __init__(
      self, operator=None, operand1=None,
      operand2=None, form=None,
    ):
    self.operator = operator
    self.operand1 = make_operator_instance(
      definition_dict=operand1, form=form,
    )
    self.operand2 = make_operator_instance(
      definition_dict=operand2, form=form,
    )
    return

class FieldReferenceOperator(Operator):
  def __init__(
      self, operator=None, operand1=None,
      operand2=None, form=None,
    ):
    self.operator = operator
    try:
      self.field_reference = form.get_field(
        operand1.get("fieldName")
      )
    except Exception as e:
      raise e
    return

class ValueOperator(Operator):
  def __init__(
      self, operator=None, operand1=None,
      operand2=None, form=None,
    ):
    self.operator = operator
    self.type = operand1.get("type")
    self.value = operand1.get("value")
    return

def make_operator_instance(definition_dict=None, form=None):
  known_operators = {
    "EQUAL":EqualOperator,
    "FIELD":FieldReferenceOperator,
    "VALUE":ValueOperator,
  }
  return known_operators.get(
      definition_dict.get("operator")
    )(**definition_dict, form=form)
