# schemas.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from model import Client

class ClientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        load_instance = True