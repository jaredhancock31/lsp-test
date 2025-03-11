from .exceptions import ValidationError

def new_quote():
    json_data = "foo"
    try:
        raise ValidationError("Invalid JSON. Please provide a valid JSON.")
    except ValidationError as err:
        return err.messages, 422

    return "done"