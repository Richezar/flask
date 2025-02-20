from pydantic import BaseModel, field_validator, ValidationError

class BaseAdvertisementSchema(BaseModel):
    title: str
    description: str
    owner: str

class CreateAdvertisement(BaseAdvertisementSchema):
    pass

class UpdateAdvertisement(BaseAdvertisementSchema):
    title: str | None = None
    description: str | None = None
    owner: str | None = None

def validate_json(schema_cls: type[CreateAdvertisement] | type[UpdateAdvertisement], json_data: dict):
    try:
        schema_obj = schema_cls(**json_data)
        return schema_obj.dict(exclude_unset=True)
    except ValidationError as e:
        errors = e.errors()
        for error in errors:
            error.pop("ctx", None)
        raise HttpError(400, errors)