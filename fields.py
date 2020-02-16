from data_types import make_data_type_instance

from operators import make_operator_instance

class Field(object):
  def __init__(
      self, fieldName=None, dataType=None,
      onLoad=False, loadUpon=None, form=None
    ):
    self.name = fieldName
    self.is_active = False

    self.data_type = make_data_type_instance(
      definition_dict=dataType,
    )
    self.value = None

    self.on_load = onLoad
    self.forward_dependency = []
    # refer Form.process_dependent_fields()

    if loadUpon:
      """
      load_upon is an operator that can be evaluated
      When load_upon is evaluated to True, this particular
      Field must now become active
      """
      self.load_upon = make_operator_instance(
        definition_dict=loadUpon,
        form=form
      )
      # When processing fields, we can only know the reverse dependencies;
      # using these, we register forward dependencies at a later stage.
      self.load_upon_reverse_dependencies = self.load_upon.find_dependencies()
      for field in self.load_upon_reverse_dependencies:
        field.register_forward_dependency(dependent_field=self)

  def register_forward_dependency(self, dependent_field=None):
    self.forward_dependency.append(dependent_field)
    return

  def eval_load_upon(self):
    return self.load_upon.eval()

  def is_on_load(self):
    return self.on_load

  def activate(self):
    self.is_active = True
    return

  def deactivate(self):
    self.is_active = False
    return

  def load(self):
    if self.is_on_load():
      self.is_active = True
    return

  def __str__(self):
    return (
      "%15s %15s %20s" % (self.name, self.data_type.type, self.data_type.to_string(self.value))
    )

  def set_value(self, value=None):
    """
    Uses an instance of the appropriate data type
    to check whether value is appropriate for this
    Field; if yes, stores in self.value
    """
    try:
      self.value = self.data_type.process(value)
    except Exception as e:
      return False
    return True

  def get_value(self):
    return self.value

  def get_data_type(self):
    return self.data_type

  def interactive(self):
    forward_dependency_to_return = []
    ip = input("%s selected; Enter text to change value / EXIT : "%(self.name))
    if ip != "EXIT":
      if self.set_value(value=ip):
        print("Value changed successfully")
        forward_dependency_to_return = self.forward_dependency
      else:
        print("Incorrect value for this field")
    print("Returning to form menu")
    return forward_dependency_to_return

