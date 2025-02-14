import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from sentence_transformers import SentenceTransformer
import re 
from meta_property.meta_property import find_key
# Load the embedding model (https://huggingface.co/nomic-ai/nomic-embed-text-v1")
#
# Define a function to generate embeddings
def featureInfo(doc, inoutfeatures):
        features = doc['features'][inoutfeatures]
        if features is not None or not features:
            desFeatures = ' '.join([feature for feature in features])
        else:
            desFeatures = ''
        return desFeatures

def metaInfo(doc, meta): # meta can be bed, bath, floor, garage
        if meta == 'garage' or meta == 'floorNo':
            count = doc['features'][meta]
        else:
            count = doc[meta]
        if count <= 1:
            tag = ' '+meta+', '
        else:
            tag = ' ' + meta + 's, '
        if meta == 'garage' or meta == 'floorNo':
            desMeta = str(doc['features'][meta]) + tag
        else:
            desMeta = str(doc[meta]) + tag
        return desMeta
def get_embedding(data):
    model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
    #  Generates vector embeddings for the given data.
    embedding = model.encode(data)
    return embedding.tolist() 
async def emb_semantic_nomic(doc, proid, pro_col):
        embed_field = 'embSemanticNomicTextV1'
        description = doc['description']
        propertyType = doc['propertyType']
        metas = ['bed', 'bath', 'garage', 'floorNo']
        desMeta = ''
        for meta in metas:
            desMeta = desMeta + metaInfo(doc, meta)
        features = (propertyType + 'with ' + desMeta + featureInfo(doc, 'indoorFeatures') + ' ' +
                    featureInfo(doc, 'outdoorAmenities'))
        title = doc['title']
        street = doc['street']
        street = ' '.join(filter(None, street.split(' ')))
        if ',' in street:
            substate = street.split(',')[1]
            substate = ' '.join(filter(None, substate.split(' ')))
            newsubstate = []
            if len(substate.split(
                    ' ')) >= 3:  # add city into street if have suburb, state, postcode in substate
                newsubstate.extend(substate.split(' ')[:-2])  # suburb name
                newsubstate.extend([doc['city']])
                newsubstate.extend(substate.split(' ')[-2:])
                substate = ' '.join(newsubstate)
            street = street.split(',')[0] + ', ' + substate
        description = re.sub(r'(\\r\\n)+', r'', description)
        doc = title + ', ' + features + ' at ' + street + ', ' + description
        emb_norm = get_embedding(doc)
        return emb_norm
        