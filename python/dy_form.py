import json

from data_types import (
    DataType, TextDataType, NumberDataType,
    EnumeratedDataType, make_data_type_instance,
  )

from operators import (
    Operator, EqualOperator, FieldReferenceOperator,
    ValueOperator, make_operator_instance,
  )

class Field(object):
  def __init__(
      self, fieldName=None, dataType=None,
      onLoad=False, loadUpon=None, form=None
    ):
    self.name = fieldName
    self.data_type = make_data_type_instance(
      definition_dict=dataType,
    )
    self.on_load = onLoad
    self.form = form

    if loadUpon:
      self.load_upon = make_operator_instance(
        definition_dict=loadUpon,
        form=form
      )
      # self.load_upon.eval() -> returns True or False
    return

  def is_on_load(self):
    return self.on_load

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
    ###
    return

  def get_field(self, field_name):
    return self.fields.get(field_name)

  def load_form(self):
    return

  def process_field_dependencies(self):
    return

  def interactive(self):
    ip = ""
    self.print_status()
    while ip != "EXIT":
      ip = raw_input("Select field to interact with : ")
    return

  def print_status(self):
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

