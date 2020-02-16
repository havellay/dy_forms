import json

from fields import Field

class Form(object):
  """
  Form contains Fields and Fields can contain values and have
  specific conditions that trigger them.
  """
  def __init__(
      self, title=None,
      description=None, fields=None
    ):
    self.title = title
    self.description = description
    self.fields = {}
    self.process_fields(fields)

  def is_duplicate_field_name(self, field_name):
    return not(self.fields.get(field_name))

  def process_fields(self, fields=None):
    for field_def in fields:
      field_name = field_def.get("fieldName")
      if not self.is_duplicate_field_name(field_name):
        raise Exception(
          "Form definition problem : field name issue"
        )
      field = Field(**field_def, form=self)
      self.fields[field_name] = field
    return

  def get_field(self, field_name):
    return self.fields.get(field_name)

  def load(self):
    for field_name,field in self.fields.items():
      field.load()
    return

  def process_dependent_fields(self, dependent_fields=None):
    """
    Fields can be dependent on one-another - If a particular
    field A becomes active (is displayed) when another field B
    contains a specific value, there is a forward directional
    dependency from field B to A. So, everytime data is entered
    in a field, all fields that have a forward dependencies to
    this field are evaluated and it is decided whether to
    activate them or not.
    """
    for field in dependent_fields:
      if field.eval_load_upon():
        field.activate()
      else:
        field.deactivate()
    return

  def interactive(self):
    while True:
      self.print_status()
      ip = input("Select field to interact with, EXIT / SUBMIT : ")
      if ip == "EXIT":
        print("Exiting")
        break
      elif ip == "SUBMIT":
        print("Submitting")
        self.submit()
        break
      chosen_field = self.fields.get(ip)
      if chosen_field:
        dependent_fields = chosen_field.interactive()
        self.process_dependent_fields(dependent_fields=dependent_fields)
      else:
        print("Incorrect field name")
    return

  def print_status(self):
    """
    Prints current active fields, data contained in active fields
    """
    for field_name,field in self.fields.items():
      if field.is_active:
        print("{}".format(field))
    return

  def submit(self):
    """ 
    Just prints a representation of the current state of the
    form's fields
    """
    submit_object = {}
    for field_name,field in self.fields.items():
      submit_object[field_name] = field.get_value()
    print(repr(submit_object))
    return submit_object

def main():
  file_name = input(
    "Please enter location of form definition json file : "
  )
  with open(file_name, 'r') as fp:
    form_definition_dict = json.loads(fp.read())
  form = Form(**form_definition_dict)

  form.load()
  form.interactive()

if __name__ == "__main__":
  main()

