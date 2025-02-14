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
import numpy as np
PyObjectId = Annotated[str, BeforeValidator(str)]

class Agency(BaseModel):
    id: Optional[PyObjectId] =  Field(default_factory=ObjectId, alias="_id")
    agencyId: int = Field()
    banner: str = Field()
    contactDetails: str = Field()
    createdAt: datetime = Field()
    logo: str = Field()
    logoSmall: str = Field()
    name: str = Field()
    profileUrl: str = Field()
    updatedAt: datetime = Field()
    website: str = Field()
    
    def to_dict(self):
        data_dict = self.dict(by_alias=True, exclude_none=True)
        return data_dict
    
class Agent(BaseModel):
    id: Optional[PyObjectId] =  Field(default_factory=ObjectId, alias="_id")
    agentId: int = Field()
    createdAt: datetime = Field()
    email: str = Field()
    firstName: str = Field()
    isActiveProfilePage: bool = Field()
    lastName: str = Field()
    phoneNumber: str = Field()
    photo: str = Field()
    profileUrl: str = Field()
    updatedAt: datetime = Field()
    def to_dict(self):
        data_dict = self.dict(by_alias=True, exclude_none=True)
        return data_dict

class School(BaseModel):
    id: Optional[PyObjectId] =  Field(default_factory=ObjectId, alias="_id")
    address: str = Field()
    createdAt: datetime = Field()
    distance: float = Field()
    domainSeoUrlSlug: str = Field()
    educationLevel: str = Field()
    gender: str = Field()
    name: str = Field()
    postCode: str = Field()
    state: str = Field()
    type: str = Field()
    updatedAt: datetime = Field()
    url: str = Field()
    year: str = Field()
    def to_dict(self):
        data_dict = self.dict(by_alias=True, exclude_none=True)
        return data_dict
    
class Image(BaseModel):
    id: Optional[PyObjectId] =  Field(default_factory=ObjectId, alias="_id")
    category: str = Field()
    createdAt: datetime = Field()
    emb: torch.Tensor = Field()
    star: bool = Field()
    updatedAt: datetime = Field()
    url: str = Field()
    
    class Config:
        arbitrary_types_allowed = True
        
    def to_dict(self):
        data_dict = self.dict(by_alias=True, exclude_none=True)
        data_dict["emb"] = data_dict["emb"].tolist()
        return data_dict
    
class PropertyForSale(BaseModel):
    id: Optional[PyObjectId] =  Field(default_factory=ObjectId, alias="_id")
    agencyId: Optional[PyObjectId] = Field(default_factory=None)
    agentId: list[Optional[PyObjectId]] = Field()
    architecturalStyte: bool = Field()
    area: dict = Field()
    bath: int = Field()
    bed: int = Field()
    city: str = Field()
    constructionYear: str = Field()
    contactInfo: list = Field()
    coordinates: dict = Field()
    createdAt: datetime = Field()
    description: str = Field()
    expectedPrice: str = Field()
    features: dict = Field()
    historysale: dict = Field()
    imageid: list[Optional[PyObjectId]] = Field()
    images: list = Field()
    listingOption: str = Field()
    postcode: int = Field()
    pricing: dict = Field()
    propertyType: str = Field()
    published: bool = Field()
    recommended: bool = Field()
    schoolId: list[Optional[PyObjectId]] = Field()
    slug: str = Field()
    stakeholder: str = Field()
    state: str = Field()
    status: str = Field()
    street: str = Field()
    structuralRemodelYear: str = Field()
    suburb: str = Field()
    title: str = Field()
    embSemanticNomicTextV1: list = Field()
    updatedAt: datetime = Field()
    location: dict = Field()
    
    class Config:
        arbitrary_types_allowed = True
    
    def to_dict(self):
        data_dict = self.dict(by_alias=True, exclude_none=True)
        return data_dict