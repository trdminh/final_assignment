import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import clip
import torch
from PIL import Image
import requests
import copy
from sklearn.metrics.pairwise import cosine_similarity



# Categories
categories = ["Bed Room", "Bath Room", "Living Room", "Laundry", "Garage", "Garden", "Kitchen", "Exterior",
              "Deck", "Study Room", "Swimming Pool", "Yard", "Media Room", "Floor Plan", "Front View",
              "Balcony", "Top View", "Gym", "Formal Dining", "Dining Room"]

category_synonyms = {
    "Bed Room": ["Bedroom", "Master Bedroom", "Guest Room", "Sleeping Area", "Resting Room", "Bunkroom"],
    "Bath Room": ["Bathroom", "Restroom", "Washroom", "Toilet", "Shower Room", "Powder Room", "Water Closet",
                  "WC""Room with a shower or bathtub, a sink, and a toilet",
                  "Room used for personal hygiene, bathing, and using the toilet",
                  "Room containing sanitary fixtures like a sink, toilet, and shower or bathtub"],
    "Living Room": ["Lounge", "Family Room", "Sitting Room", "Parlor", "Den", "Drawing Room", "Common Room"],
    "Laundry": ["Laundry Room", "Washing Room", "Utility Room", "Wash Area", "Clothes Room"],
    "Garage": ["Carport", "Vehicle Garage", "Auto Garage", "Car Garage", "Workshop"],
    "Garden": ["Outdoor Garden", "Flower Garden", "Botanical Garden", "Green Space", "Backyard Garden",
               "Flower Bed", "Planting Area"],
    "Kitchen": ["Kitchen", "Cooking Area", "Cookroom", "Kitchenette", "Galley Kitchen", "Cooking Space",
                "Culinary Room", "Culinary Studio", "Cookery", "Food Prep Area",
                "Baking Area", "Open Kitchen", "Modern Kitchen"],
    "Exterior": ["Outdoor View", "Building Exterior", "Outside View", "House Exterior", "Outdoor Facade"],
    "Deck": ["Patio", "Terrace", "Porch", "Veranda", "Sun Deck", "Outdoor Deck"],
    "Study Room": ["Home Office", "Workroom", "Library", "Reading Room", "Workspace", "Study Area"],
    "Swimming Pool": ["Pool", "Swimming Area", "Outdoor Pool", "Indoor Pool", "Poolside", "Plunge Pool"],
    "Yard": ["Private Yard", "Outdoor Yard", "Courtyard", "Patio Yard", "Garden Yard", "Backyard Yard", "Lawn Yard"],
    "Media Room": ["Home Theater", "Movie Room", "Cinema Room", "Entertainment Room", "Screening Room", "Theater Room"],
    "Floor Plan": ["House Layout", "Room Layout", "Building Plan", "Home Layout", "Floor Layout"],
    "Front View": ["Facade", "Front Side", "Exterior View", "Street View", "Building Front"],
    "Balcony": ["Veranda", "Outdoor Balcony", "Terrace", "Deck", "Outdoor Porch", "Juliet Balcony"],
    "Top View": ["Aerial View", "Bird's Eye View", "Overhead View", "Sky View", "Top-Down View"],
    "Gym": ["Fitness Room", "Exercise Room", "Workout Room", "Training Room", "Health Club", "Physical Training Room"],
    "Formal Dining": ["Eating Room", "Formal Eating Area", "Dining Space", "Dining Hall", "Banquet Room"],
    "Dining Room": ["Meal Room", "Eating Place", "Dining Area", "Breakfast Room", "Eating Space"]
}



device = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess = clip.load("ViT-L/14")

def add_embedding(data):
    images_batch = [preprocess(Image.open(requests.get(item["url"], stream=True).raw).convert('RGB')).unsqueeze(0).to(device) for item in data]
    text_token = clip.tokenize(categories).to(device)
    images_batch = torch.cat(images_batch, dim=0).to(device)
    with torch.no_grad():
        images_feature = model.encode_image(images_batch)
        text_features = model.encode_text(text_token)
    
    new_data = copy.deepcopy(data)
    for i, embed in enumerate(images_feature):
        new_data[i]["embed"] = embed
    
    return new_data

def calculate_similarities(data, threshold=0.9):
    new_data = add_embedding(data)
    embeddings = []
    for i in new_data:
        embeddings.append(i["embed"])
    
    similar_images = []
    
    embeddings = [emb.detach().cpu().numpy() for emb in embeddings]
    
    for i in range(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            
            similarity = cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
            
            if similarity > threshold:
                similar_images.append((i,j,similarity))
    return similar_images

def remove_duplicate_images(data):
    similar_images = calculate_similarities(data)
    to_remove = set()

    for index1, index2, _ in similar_images:
        to_remove.add(max(index1, index2))

    filtered_embeddings = [data[i] for i in range(len(data)) if i not in to_remove]

    return filtered_embeddings

def classification(data):
    '''
        Zero-Shot Inference: Model Applies Pre-trained Knowledge to Process Image-Text Pairs
        and Generate Relevant Predictions using the filtered data images.
    '''
    images_batch = [preprocess(Image.open(requests.get(item["url"], stream=True).raw).convert("RGB")).unsqueeze(0).to(device) for item in data]
    text_token = clip.tokenize(categories).to(device)
    images_batch = torch.cat(images_batch, dim=0).to(device)
    
    with torch.no_grad():
        images_feature = model.encode_image(images_batch)  # Encode image embeddings
        text_features = model.encode_text(text_token)     # Encode text embeddings

    # Normalize embeddings
    images_feature = images_feature / images_feature.norm(dim=-1, keepdim=True)
    text_features = text_features / text_features.norm(dim=-1, keepdim=True)
    # Calculate similarity scores (logits)
    logits_per_image = images_feature @ text_features.T  # Dot product for similarities
    probs = logits_per_image.softmax(dim=1)  # Convert to probabilities
    new_data = add_embedding(data)
    results = []
    for i, item in enumerate(data):
        predicted_category = categories[torch.argmax(probs[i])]  # Predicted class
        correct = predicted_category == item["category"]  # Compare with actual class
        results.append({
            "url": item["url"],
            "category": predicted_category,
            "actual_category": item["category"],
            "emb": new_data[i]["embed"],
            "star": item["star"],
            "correct": correct
        })

    return results

## function enhanced_classification has something wrong
async def enhanced_classification(data):
    results = []
    expanded_categories = []
    seen_synonyms = set()  # To track already used synonyms across all categories

    # Expand categories with synonyms
    for category in categories:
        expanded_categories.append(category)  # Add the original category first
        for synonym in category_synonyms.get(category, []):  # Handle missing keys gracefully
            if synonym not in seen_synonyms and synonym != category:
                expanded_categories.append(synonym)
                seen_synonyms.add(synonym)

    # Create reverse map from synonyms to original categories
    reverse_category_map = {synonym: category for category, synonyms in category_synonyms.items() for synonym in synonyms}
    reverse_category_map.update({category: category for category in categories})  # Map original categories to themselves

    # Tokenize expanded categories
    text_token = clip.tokenize(expanded_categories).to(device)

    # Process images
    images_batch = [preprocess(Image.open(requests.get(item["url"], stream=True).raw).convert("RGB")).unsqueeze(0).to(device) for item in data]
    images_batch = torch.cat(images_batch, dim=0).to(device)

    with torch.no_grad():
        images_feature = model.encode_image(images_batch)  # Encode image embeddings
        text_features = model.encode_text(text_token)     # Encode text embeddings

    # Normalize embeddings
    images_feature = images_feature / images_feature.norm(dim=-1, keepdim=True)
    text_features = text_features / text_features.norm(dim=-1, keepdim=True)

    # Calculate similarity scores (logits)
    logits_per_image = images_feature @ text_features.T  # Dot product for similarities
    probs = logits_per_image.softmax(dim=1)  # Convert to probabilities

    # Process results
    for i, item in enumerate(data):
        # Get the predicted category variant
        predicted_category_variant = expanded_categories[torch.argmax(probs[i])]  # Variant (may be a synonym)

        # Map the variant to the original category
        predicted_category = reverse_category_map.get(predicted_category_variant, predicted_category_variant)

        # Check correctness
        correct = predicted_category == item["category"]

        results.append({
            "url": item["url"],
            "category": predicted_category,
            "actual_category": item["category"],
            "star": item["star"],
            "correct": correct,
            "emb": images_feature[i].tolist()
        })

    return results
