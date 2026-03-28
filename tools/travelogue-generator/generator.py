import os
import time
from google import genai
from google.genai import types
from PIL import Image
import json

class TravelogueGenerator:
    def __init__(self, api_key=None):
        self.client = genai.Client(api_key=api_key)

    def generate_html_post(self, relevant_files, destination, start_date, template_content, image_subfolder):
        """
        Generates a high-quality, professional travelogue using Gemini 2.5 Flash.
        Strictly enforces the 'Golden' structure and dynamic image grids.
        """
        # Analyze a larger batch to find the best representative shots
        selection_batch_size = min(15, len(relevant_files))
        
        print(f"\n[AI] Deep analysis of {selection_batch_size} photos for narrative arc...")
        
        context_images = []
        image_metadata = []
        for i in range(selection_batch_size):
            filepath, filename = relevant_files[i]
            try:
                img = Image.open(filepath).convert("RGB")
                img.thumbnail((512, 512))
                context_images.append(img)
                web_path = f"../../assets/images/{image_subfolder}/{filename}"
                image_metadata.append({
                    "id": i + 1,
                    "filename": filename,
                    "web_path": web_path
                })
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
        
        metadata_str = json.dumps(image_metadata, indent=2)
        
        prompt = (
            f"You are a world-class travel writer for 'Desi European'. You are writing about a trip to {destination}.\n"
            f"DATE: {start_date}\n"
            f"PHOTO DATA (JSON):\n{metadata_str}\n\n"
            f"WRITING STYLE & STRUCTURE MANDATES:\n"
            f"1. FIRST-PERSON POV: Use 'I', 'we', 'my family'. Tell a story from your perspective.\n"
            f"2. THE HOOK: Do NOT start with 'I went to...'. Start with a sensory detail (the smell of old stone, the sound of a street musician) or a profound realization about the city.\n"
            f"3. THE GOLDEN STRUCTURE:\n"
            f"   - Introduction (The Hook)\n"
            f"   - Thematic Section 1 (e.g., The Atmosphere/Architecture)\n"
            f"   - Thematic Section 2 (e.g., Family moments/Desi-European cultural intersections)\n"
            f"   - Conclusion (Final reflection/The 'Soul' of the city)\n"
            f"4. PEOPLE: Identify and describe family members (parents, daughter, etc.) and their interactions naturally.\n"
            f"5. PHOTO SELECTION: Pick EXACTLY 4 of the most distinct photos from the provided data. "
            f"Identify one as the 'STAR' (Hero) image. Use its 'web_path' for the main hero image in the template.\n"
            f"6. DYNAMIC GRIDS: Intersperse the other 3 photos throughout the text using grids. "
            f"For example, a text block, then a grid-2, then more text, then a grid-1.\n"
            f"7. CODE: Use `<div class='photo-grid grid-X'>` where X is 1, 2, or 3. Nest images in `<div class='grid-item'>`.\n"
            f"8. LINKS: Ensure all relative links use `../../`.\n\n"
            f"--- TEMPLATE START ---\n{template_content}\n--- TEMPLATE END ---\n\n"
            f"Return ONLY the raw HTML code."
        )
        
        contents = [prompt] + context_images

        # Attempt generation
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents
            )
            html_output = response.text.strip()
            
            # Cleanup markdown
            if html_output.startswith('```html'): html_output = html_output[7:]
            if html_output.endswith('```'): html_output = html_output[:-3]
            
            # Link verification
            html_output = html_output.replace('href="../assets/', 'href="../../assets/')
            html_output = html_output.replace('src="../assets/', 'src="../../assets/')
            html_output = html_output.replace('href="../about.html"', 'href="../../about.html"')
            html_output = html_output.replace('href="../index.html"', 'href="../../index.html"')
            
            return html_output.strip()
            
        except Exception as e:
            print(f"Error during high-quality generation: {e}")
            return None
