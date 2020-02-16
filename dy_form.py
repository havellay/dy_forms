import json

from data_types import (
    DataType, TextDataType, NumberDataType,
    EnumeratedDataType, make_data_type_instance,
  )

from operators import (
    Operator, EqualOperator, FieldReferenceOperator,
    ValueOperator, make_operator_instance,
  )

from fields import Field

class Form(object):
  def __init__(
      self, title=None,
      description=None, fields=None
    ):
    self.title = title
    self.description = description
    self.on_load_fields = {}
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
      if field.is_on_load():
        self.on_load_fields[field_name] = field
    return

  def get_field(self, field_name):
    return self.fields.get(field_name)

  def load(self):
    """
    Looks at all fields and loads them
    """
    for field_name,field in self.fields.items():
      field.load()
    return

  def interactive(self):
    while True:
      self.print_status()
      ip = input("Select field to interact with, EXIT / SUBMIT : ")
      if ip == "EXIT":
        print("Exiting")
        break
      chosen_field = self.fields.get(ip)
      if chosen_field:
        dependent_fields = chosen_field.interactive()
        for field in dependent_fields:
          if field.eval_load_upon():
            field.activate()
          else:
            field.deactivate()
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
    return

def main():
  file_name = input(
    "Please enter location of form definition json file : "
  )
  with open(file_name, 'r') as fp:
    form_definition_dict = json.loads(fp.read())
  form = Form(**form_definition_dict)

  form.load()
  form.interactive()
  form.submit()

if __name__ == "__main__":
  main()

