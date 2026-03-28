import os
from google import genai
from google.genai import types
import json
from PIL import Image

class IntelligentFilter:
    def __init__(self, api_key=None):
        self.client = genai.Client(api_key=api_key)

    def is_photo_relevant(self, image_path, destination):
        """
        Uses Gemini Vision to determine if a photo matches the given destination
        or travel vibe. Returns a boolean.
        """
        try:
            img = Image.open(image_path).convert("RGB")
            
            prompt = (
                f"Analyze this image. Does it look like it was taken in or around "
                f"'{destination}'? Look for landmarks, language on signs, architecture, "
                f"or general landscape that matches. "
                f"Return a JSON object with 'is_match' (boolean) and 'reason' (string). "
                f"Respond with ONLY the JSON object."
            )
            
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[prompt, img]
            )
            
            # Clean up potential markdown formatting
            text = response.text.strip()
            if text.startswith('```json'):
                text = text[7:]
            if text.endswith('```'):
                text = text[:-3]
                
            result = json.loads(text.strip())
            return result.get('is_match', False), result.get('reason', '')
            
        except Exception as e:
            print(f"Error filtering {image_path}: {e}")
            return False, str(e)

    def filter_photos(self, local_files, destination):
        """
        Filters a list of local file paths, returning only those relevant to the destination.
        """
        print(f"\nIntelligent Filtering: Analyzing {len(local_files)} photos for relevance to '{destination}'...")
        relevant_files = []
        
        for filepath, filename in local_files:
            is_match, reason = self.is_photo_relevant(filepath, destination)
            if is_match:
                print(f"[KEEP] {filename}: {reason}")
                relevant_files.append((filepath, filename))
            else:
                print(f"[SKIP] {filename}: {reason}")
                
        print(f"Filtering complete. Kept {len(relevant_files)} out of {len(local_files)} photos.")
        return relevant_files
