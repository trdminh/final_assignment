import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from typing import Optional
from datetime import datetime
import torch
PyObjectId = Annotated[str, BeforeValidator(str)]

class Agency(BaseModel):
    id: Optional[PyObjectId] =  Field(default_factory=ObjectId, alias="_id")
    agencyId: Optional[int] = Field(default=None)
    banner: Optional[str] = Field(default=None)
    contactDetails: Optional[str] = Field(default=None)
    createdAt: datetime = Field(default=datetime.now())
    logo: Optional[str] = Field(default=None)
    logoSmall: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    profileUrl: Optional[str] = Field(default=None)
    updatedAt: datetime = Field(default=datetime.now())
    website: Optional[str] = Field(default=None)
    
    def to_dict(self):
        data_dict = self.dict(by_alias=True, exclude_none=True)
        return data_dict
    
class Agent(BaseModel):
    id: Optional[PyObjectId] =  Field(default_factory=ObjectId, alias="_id")
    agentId: Optional[int] = Field(default=None)
    createdAt: datetime = Field(default=datetime.now())
    email: Optional[str] = Field(default=None)
    firstName: Optional[str] = Field(default=None)
    isActiveProfilePage: Optional[bool] = Field()
    lastName: Optional[str] = Field(default=None)
    phoneNumber: Optional[str] = Field(default=None)
    photo: Optional[str] = Field(default=None)
    profileUrl: str = Field()
    updatedAt: datetime = Field(default=datetime.now())
    def to_dict(self):
        data_dict = self.dict(by_alias=True, exclude_none=True)
        return data_dict

class School(BaseModel):
    id: Optional[PyObjectId] =  Field(default_factory=ObjectId, alias="_id")
    address: Optional[str] = Field(default=None)
    createdAt: datetime = Field(default=datetime.now())
    distance: Optional[float] = Field(default=None)
    domainSeoUrlSlug: Optional[str] = Field(default=None)
    educationLevel: Optional[str] = Field(default=None)
    gender: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    postCode: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    updatedAt: datetime = Field(default=datetime.now())
    url: Optional[str] = Field(default=None)
    year: Optional[str] = Field(default=None)
    def to_dict(self):
        data_dict = self.dict(by_alias=True, exclude_none=True)
        return data_dict
    
class Image(BaseModel):
    id: Optional[PyObjectId] =  Field(default_factory=ObjectId, alias="_id")
    category: Optional[str] = Field(default=None)
    createdAt: datetime = Field(default=datetime.now())
    emb: Optional[list] = Field(default=None)
    star: Optional[bool] = Field(default=None)
    updatedAt: datetime = Field(default=datetime.now())
    url: Optional[str] = Field(default=None)
    
    class Config:
        arbitrary_types_allowed = True
        
    def to_dict(self):
        data_dict = self.dict(by_alias=True, exclude_none=True)
        return data_dict
    
class PropertyForSale(BaseModel):
    id: Optional[PyObjectId] =  Field(default_factory=ObjectId, alias="_id")
    agencyId: Optional[PyObjectId] = Field(default_factory=None)
    agentId: Optional[list[PyObjectId]] = Field(default=None)
    architecturalStyte: Optional[bool] = Field(default=None)
    area: Optional[dict] = Field(default=None)
    bath: Optional[int] = Field(default=None)
    bed: Optional[int] = Field(default=None)
    city: Optional[str] = Field(default=None)
    constructionYear: Optional[str] = Field(default=None)
    contactInfo: Optional[list] = Field(default=None)
    coordinates: Optional[dict] = Field(default=None)
    createdAt: datetime = Field(default=datetime.now())
    description: Optional[str] = Field(default=None)
    expectedPrice: Optional[str] = Field(default=None)
    features: Optional[dict] = Field(default=None)
    historysale: Optional[list] = Field(default=None)
    imageid: list[Optional[PyObjectId]] = Field()
    images: Optional[list] = Field(default=None)
    listingOption: Optional[str] = Field(default=None)
    postcode: Optional[int] = Field(default=None)
    pricing: Optional[dict] = Field(default=None)
    propertyType: Optional[str] = Field(default=None)
    published: Optional[bool] = Field(default=None)
    recommended: Optional[bool] = Field(default=None)
    schoolId: Optional[list[PyObjectId]] = Field()
    slug: Optional[str] = Field(default=None)
    stakeholder: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    street: Optional[str] = Field(default=None)
    structuralRemodelYear: Optional[str] = Field(default=None)
    suburb: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    embSemanticNomicTextV1: Optional[list] = Field(default=None)
    updatedAt: datetime = Field(default=datetime.now())
    url: str = Field()
    location: Optional[dict] = Field(default=None)
    
    class Config:
        arbitrary_types_allowed = True
    
    def to_dict(self):
        data_dict = self.dict(by_alias=True, exclude_none=True)
        return data_dict
    
class PropertySold(BaseModel):
    id: Optional[PyObjectId] =  Field(default_factory=ObjectId, alias="_id")
    agencyId: Optional[PyObjectId] = Field(default_factory=None)
    agentId: list[Optional[PyObjectId]] = Field()
    architecturalStyte: Optional[bool] = Field(default=None)
    area: Optional[dict] = Field(default=None)
    bath: Optional[int] = Field(default=None)
    bed: Optional[int] = Field(default=None)
    city: Optional[str] = Field(default=None)
    constructionYear: Optional[str] = Field(default=None)
    contactInfo: Optional[list] = Field(default=None)
    coordinates: Optional[dict] = Field(default=None)
    createdAt: datetime = Field()
    description: Optional[str] = Field(default=None)
    expectedPrice: Optional[str] = Field(default=None)
    features: Optional[dict] = Field(default=None)
    historysale: Optional[list[dict]] = Field(default=None)
    imageid: list[Optional[PyObjectId]] = Field()
    images: list = Field()
    listingOption: Optional[str] = Field(default=None)
    postcode: Optional[int] = Field(default=None)
    pricing: Optional[dict] = Field(default=None)
    propertyType: Optional[str] = Field(default=None)
    published: bool = Field()
    recommended: bool = Field()
    schoolId: list[Optional[PyObjectId]] = Field()
    slug: Optional[str] = Field(default=None)
    stakeholder: str = Field()
    state: str = Field()
    status: str = Field()
    street: str = Field()
    structuralRemodelYear: str = Field()
    suburb: str = Field()
    title: str = Field()
    # embSemanticNomicTextV1: list = Field()
    updatedAt: datetime = Field()
    url: str = Field()
    location: dict = Field()
    
    class Config:
        arbitrary_types_allowed = True
    
    def to_dict(self):
        data_dict = self.dict(by_alias=True, exclude_none=True)
        return data_dict
    
class HistoryForSale(BaseModel):
    id: Optional[PyObjectId] =  Field(default_factory=ObjectId, alias="_id")
    createdAt: Optional[datetime] = Field(default=None)
    historyprofile: Optional[list[dict]] = Field(default=None)
    url: Optional[str] = Field(default=None)
    updatedAt: Optional[datetime] = Field()
    
    def to_dict(self):
        data_dict = self.dict(by_alias=True, exclude_none=True)
        return data_dict
    
    