from marshmallow import fields

from src.views import BaseSchema


class GallerySchema(BaseSchema):
    id = fields.UUID(dump_only=True)
    main_photo = fields.Str()
    path = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    items_id = fields.UUID(requried=True)

gallery_schema = GallerySchema()