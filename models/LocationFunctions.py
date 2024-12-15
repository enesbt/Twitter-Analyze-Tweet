from transformers import pipeline
from googlemaps.exceptions import TransportError
from dotenv import load_dotenv
import googlemaps
import os

def get_location(text):
    pipe = pipeline("token-classification", model="akdeniz27/bert-base-turkish-cased-ner",device=0)
    if not text.strip():
        return None 
    result = pipe(text) 
    location = "" 
    
    for entity in result:
        token = entity['word']
        label = entity['entity']

        if 'LOC' in label:  
            if not token.startswith('##'):  
                if location:  
                    location += " " 
                location += token
            else:
                location += token.lstrip('##')  
                
    return location.strip() if location else None

def location_to_coordinates(address):
    try:
        load_dotenv()
        api_key = os.getenv("API_KEY2")
        gmaps = googlemaps.Client(key=api_key)
        geocode_result = gmaps.geocode(address, components={'country': 'TR'})
        if geocode_result:
            first_result = geocode_result[0]
            location = first_result['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            formatted_address = first_result['formatted_address']
            return formatted_address, latitude, longitude
        else:
            return address, None, None
    except (TransportError) as e:
        print(f"Error with address {address}: {e}")
        return address, None, None
    except Exception as e:
        print(f"Unexpected error with address {address}: {e}")
        return address, None, None

def address(text):
    location  = get_location(text)
    if location:
        address, latitude, longitude = location_to_coordinates(location)
        return address, latitude, longitude
    else:
        return None, None, None