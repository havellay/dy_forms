from data_types import make_data_type_instance

class Operator(object):
  """
  An Operator allows definition of a condition that can be evaluated;
  This can be done by calling the eval() method;
  At this time, only EqualOperator, FieldReferenceOperator and ValueOperator
  are defined. Other possible operators are ContainsOperator, GreaterThanOperater,
  AndOperator, NotOperator etc.
  Such Operators allow for specification of non-trivial conditions.
  """
  def __init__(self):
    pass

  def find_dependencies(self):
    return []
  
class EqualOperator(Operator):
  """
  EqualOperator has two operands and checks whether first operand's value
  is equal to the second operand;
  """
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

  def find_dependencies(self):
    dependencies = []
    dependencies.extend(self.operand1.find_dependencies())
    dependencies.extend(self.operand2.find_dependencies())
    return dependencies

  def eval(self):
    """
    Since ValueOperators can have an incomplete data-type instance,
    it is important to use the more complete data-type definition
    for evaluation.
    """
    op1_eval,op1_data_type = self.operand1.eval()
    op2_eval,op2_data_type  = self.operand2.eval()
    if type(op1_data_type) != type(op2_data_type):
      raise Exception("Load Upon Compute Error")
    # Type promotion of sorts;
    data_type = op1_data_type if op2_data_type.is_subordinate() else op2_data_type
    return op1_data_type.is_equal(op1_eval, op2_eval)

class FieldReferenceOperator(Operator):
  """
  Used to denote value contained in a Field when defining conditions
  in loadUpon
  """
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

  def find_dependencies(self):
    return [self.field_reference]
  
  def eval(self):
    return self.field_reference.get_value(),self.field_reference.get_data_type()

class ValueOperator(Operator):
  def __init__(
      self, operator=None, operand1=None,
      operand2=None, form=None,
    ):
    self.operator = operator
    self.type = operand1.get("type")
    self.value = operand1.get("value")

  def __str__(self):
    return

  def find_dependencies(self):
    return []

  def eval(self):
    return self.value,make_data_type_instance({"type":self.type, "subordinate":True})

def make_operator_instance(definition_dict=None, form=None):
  known_operators = {
    "EQUAL":EqualOperator,
    "FIELD":FieldReferenceOperator,
    "VALUE":ValueOperator,
  }
  return known_operators.get(
      definition_dict.get("operator")
    )(**definition_dict, form=form)
