import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connection.connect_to_mongodb import get_document_id, get_emb_image
from connection.connect_to_mongodb import collection
from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from typing import Optional
import torch
PyObjectId = Annotated[str, BeforeValidator(str)]
class AgencyUpdate(BaseModel):
    agencyId : Optional[int] = Field(default=None)
    banner : Optional[str] = Field(default=None)
    contractDetails : Optional[str] = Field(default=None)
    logo : Optional[str] = Field(default=None)
    logoSmall : Optional[str] = Field(default=None)
    name : Optional[str] = Field(default=None)
    profileUrl : Optional[str] = Field(default=None)
    updateAt: datetime = Field(default=datetime.now())
    website : Optional[str] = Field(default=None)
     
class ImageUpdate(BaseModel):
    category : Optional[str] = Field(default=None)
    emb : Optional[torch.Tensor] = Field(default=None)
    star: Optional[bool] = Field(default=None)
            
