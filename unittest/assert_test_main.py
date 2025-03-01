import unittest
from unittest.mock import AsyncMock, patch
from datetime import datetime
from bson import ObjectId
import torch
from upload_new_data import (
    create_agnecy_data, create_agent_data, create_school_data, create_image_data, created_property_for_sale
)

class TestDatabaseFunctions(unittest.IsolatedAsyncioTestCase):
    
    @patch("main.get_document_id", new_callable=AsyncMock)
    @patch("main.collection", new_callable=AsyncMock)
    async def test_create_agency_data(self, mock_collection, mock_get_document_id):
        mock_collection["Agency"].insert_one = AsyncMock(return_value=AsyncMock(inserted_id=ObjectId()))
        mock_get_document_id.return_value = False
        
        data = {
            "agencyId": "12345",
            "banner": "test_banner",
            "contactDetails": "test_contact",
            "logo": "test_logo",
            "logosmall": "test_logo_small",
            "name": "Test Agency",
            "profileUrl": "http://testagency.com",
            "website": "http://testagency.com"
        }
        result = await create_agnecy_data(data)
        self.assertIsInstance(result, ObjectId)
    
    @patch("main.get_document_id", new_callable=AsyncMock)
    @patch("main.collection", new_callable=AsyncMock)
    async def test_create_agent_data(self, mock_collection, mock_get_document_id):
        mock_collection["Agent"].insert_one = AsyncMock(return_value=AsyncMock(inserted_id=ObjectId()))
        mock_get_document_id.return_value = False
        
        data = [{
            "agentId": 13842784,
            "email": "agent@test.com",
            "firstName": "Mike",
            "isActiveProfilePage": True,
            "lastName": "Doan",
            "phoneNumber": "123456789",
            "photo": "http://photo.com",
            "profileUrl": "http://agent.com"
        }]
        result = await create_agent_data(data)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], ObjectId)
    
    @patch("main.get_document_id", new_callable=AsyncMock)
    @patch("main.collection", new_callable=AsyncMock)
    async def test_create_school_data(self, mock_collection, mock_get_document_id):
        mock_collection["School"].insert_one = AsyncMock(return_value=AsyncMock(inserted_id=ObjectId()))
        mock_get_document_id.return_value = False
        
        data = [{
            "address": "123 Street",
            "distances": 5.0,
            "domainSeoUrlSlug": "school-test",
            "educationLevel": "Primary",
            "gender": "Co-ed",
            "name": "Test School",
            "postcode": "12345",
            "state": "StateTest",
            "type": "Public",
            "url": "http://school.com",
            "year": "2024"
        }]
        result = await create_school_data(data)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], ObjectId)
    
    @patch("main.collection", new_callable=AsyncMock)
    async def test_create_image_data(self, mock_collection):
        mock_collection["Image"].insert_one = AsyncMock(return_value=AsyncMock(inserted_id=ObjectId()))
        emb = torch.tensor([0.1, 0.2, 0.3])
        data = [{
            "predicted_category": "Kitchen",
            "emb": emb,
            "star": False,
            "url": "http://image.com"
        }]
        result, new_images = await create_image_data(data)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], ObjectId)
        self.assertIsInstance(new_images, list)
    
    @patch("main.get_document_id", new_callable=AsyncMock)
    @patch("main.collection", new_callable=AsyncMock)
    async def test_created_property_for_sale(self, mock_collection, mock_get_document_id):
        mock_collection["PropertyForSale"].insert_one = AsyncMock(return_value=AsyncMock(inserted_id=ObjectId()))
        mock_get_document_id.return_value = False
        
        data = {
            "agency": {"agencyId": "12345", "banner": "", "contactDetails": "", "logo": "", "logosmall": "", "name": "", "profileUrl": "", "website": ""},
            "agent": [{"agentId": "A123", "email": "agent@test.com", "firstName": "", "isActiveProfilePage": True, "lastName": "", "phoneNumber": "", "photo": "", "profileUrl": ""}],
            "school": [{"address": "", "distances": 5.0, "domainSeoUrlSlug": "", "educationLevel": "", "gender": "", "name": "", "postcode": "", "state": "", "type": "", "url": "", "year": 2024}],
            "images": [{"category": "House", "star": 5, "url": "http://image.com"}],
            "propertyForSale": {
                "area": 120, "bath": 2, "bed": 3, "city": "Test City", "constructionYear": 2000,
                "contractInfo": "", "coordinates": {"lat": 10.5, "lng": 20.5}, "description": "Nice house",
                "expectedPrice": 500000, "features": [], "historySale": [], "listingOption": "For Sale",
                "postcode": "12345", "pricing": {}, "propertyType": "House", "published": True,
                "recommended": False, "slug": "test-house", "stakeHolder": "Owner", "state": "Test State",
                "status": "Available", "street": "Test Street", "structuralRemodelYear": 2015,
                "suburb": "Test Suburb", "title": "Beautiful House"
            }
        }
        url = "http://property.com"
        await created_property_for_sale(data, url)
        mock_collection["PropertyForSale"].insert_one.assert_called()

if __name__ == "__main__":
    unittest.main()
