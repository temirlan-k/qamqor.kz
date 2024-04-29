import json
from datetime import datetime
from decimal import Decimal
import uuid
from sqlalchemy.ext.declarative import DeclarativeMeta

from schemas.product import ProductOutDB

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, uuid.UUID):
            return str(obj)  
        return json.JSONEncoder.default(self, obj)
