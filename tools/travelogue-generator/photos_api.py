import os
import requests
import json
import webbrowser

class PhotosAPI:
    def __init__(self, credentials):
        self.creds = credentials
    
    def pick_photos(self, destination):
        """
        Creates a Picker session and asks the user to select photos.
        """
        print(f"\n--- GOOGLE PHOTOS PICKER ---")
        print(f"I am opening a secure Google window for you.")
        print(f"Please SEARCH for '{destination}' in the picker and select the photos you want to include in your post.")
        
        headers = {
            'Authorization': f'Bearer {self.creds.token}',
            'Content-Type': 'application/json'
        }
        
        # 1. Create a Picker Session
        session_url = "https://photospicker.googleapis.com/v1/sessions"
        response = requests.post(session_url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error creating Picker session: {response.status_code} - {response.text}")
            return []
            
        session = response.json()
        picker_uri = session.get('pickerUri')
        session_id = session.get('id')
        
        if not picker_uri:
            print("Error: No pickerUri received from Google.")
            return []
            
        print(f"\nClick this link to pick your photos:\n{picker_uri}\n")
        webbrowser.open(picker_uri)
        
        input("Press ENTER after you have finished picking your photos and clicked 'Done' in the browser...")
        
        # 2. Get the picked media items
        media_url = f"https://photospicker.googleapis.com/v1/mediaItems?sessionId={session_id}"
        media_response = requests.get(media_url, headers=headers)
        
        if media_response.status_code != 200:
            print(f"Error fetching picked photos: {media_response.status_code} - {media_response.text}")
            return []
            
        items = media_response.json().get('mediaItems', [])
        print(f"Found {len(items)} items in the session.")
        return items

    def download_photos(self, items, download_dir):
        """
        Downloads photos to a local directory using the nested baseUrl.
        """
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            
        local_files = []
        headers = {'Authorization': f'Bearer {self.creds.token}'}
        
        print(f"Attempting to download {len(items)} selected photos to {download_dir}...")
        
        for idx, item in enumerate(items):
            # The Picker API nests everything inside 'mediaFile'
            media_file = item.get('mediaFile', {})
            base_url = media_file.get('baseUrl')
            filename = media_file.get('filename', f"picked_{idx}.jpg")
            
            if not base_url:
                print(f"Skipping item {idx}: No baseUrl found in mediaFile.")
                continue
                
            download_url = f"{base_url}=d"
            filepath = os.path.join(download_dir, filename)
            
            # Download the actual image content
            if not os.path.exists(filepath):
                # Picker API baseUrl REQUIRES the Authorization header
                response = requests.get(download_url, headers=headers, stream=True)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Failed to download {filename}: Status {response.status_code}")
                    continue
            else:
                print(f"Already exists: {filename}")
                
            local_files.append((filepath, filename))
            
        return local_files
