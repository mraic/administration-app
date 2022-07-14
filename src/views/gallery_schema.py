from marshmallow import fields

from src.views import BaseSchema


class GallerySchema(BaseSchema):
    id = fields.UUID(dump_only=False)
    main_photo = fields.Str(required=True)
    path = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    items_id = fields.UUID(requried=True)


gallery_schema = GallerySchema()
