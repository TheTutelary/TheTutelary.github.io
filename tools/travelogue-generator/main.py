import os
import argparse
import shutil
import re
from dotenv import load_dotenv

# We load dotenv before importing other modules just in case
load_dotenv()

from auth import get_credentials
from photos_api import PhotosAPI
from generator import TravelogueGenerator

def update_homepage(repo_root, destination, post_path, hero_img_path):
    """
    Automates homepage updates: changes thumbnail for destination and adds to latest.
    """
    index_path = os.path.join(repo_root, 'index.html')
    if not os.path.exists(index_path):
        return

    with open(index_path, 'r') as f:
        content = f.read()

    web_hero = hero_img_path.replace('../../', '')
    updated = False

    # 1. Update EVERY image that links to this post
    # Look for cards (dest-card or article-card) that contain the link to post_path
    # and update the <img> tag inside them.
    
    # Pattern to find a container (div or article) that has our post_path and an <img>
    # We'll do this block by block to be safe.
    blocks = re.split(r'(<(?:article|div) [^>]*class="(?:article|dest)-card"[^>]*>)', content)
    new_blocks = []
    
    for i in range(0, len(blocks)):
        block = blocks[i]
        if i > 0 and blocks[i-1].startswith('<'):
            # This is the content of a card
            if post_path in block:
                print(f"[Homepage] Found card matching {post_path}. Updating thumbnail...")
                # Update the <img> src in this block
                block = re.sub(r'(<img src=")([^"]*)(")', fr'\1{web_hero}\3', block, count=1)
                updated = True
            new_blocks.append(block)
        else:
            new_blocks.append(block)
            
    content = "".join(new_blocks)

    # 2. If it was NOT updated (meaning no card found), inject it as a new story
    if post_path not in content:
        print(f"[Homepage] Injecting new {destination} story into grid...")
        grid_marker = '<div class="article-grid">'
        grid_pos = content.find(grid_marker)
        if grid_pos != -1:
            insertion_point = grid_pos + len(grid_marker)
            new_card = f"""
            <article class="article-card">
                <a href="{post_path}">
                    <img src="{web_hero}" alt="{destination}">
                </a>
                <span class="meta">Travel Diary • {destination}</span>
                <h3><a href="{post_path}">{destination}: A Personal Journey</a></h3>
                <p>A new memory from our latest travels, written with a Desi heart and European soul.</p>
                <a href="{post_path}" class="read-link">Read Story</a>
            </article>"""
            content = content[:insertion_point] + new_card + content[insertion_point:]
            updated = True

    if updated:
        with open(index_path, 'w') as f:
            f.write(content)
        print("[Homepage] index.html updated successfully.")

def main():
    parser = argparse.ArgumentParser(description="Go Bananas Travelogue Generator.")
    parser.add_argument("destination", help="The destination (e.g., 'Prague').")
    parser.add_argument("start_date", help="Trip date (YYYY-MM-DD)")
    parser.add_argument("--rewrite", action="store_true", help="Skip Picker and rewrite based on local photos.")
    parser.add_argument("--month", help="Override month name (e.g. 'jun').")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    year = args.start_date.split('-')[0]
    
    # Organize monthly folders
    month_map = {"01":"jan","02":"feb","03":"mar","04":"apr","05":"may","06":"jun","07":"jul","08":"aug","09":"sep","10":"oct","11":"nov","12":"dec"}
    month_code = args.start_date.split('-')[1]
    month_name = args.month.lower() if args.month else month_map.get(month_code, "trip")

    dest_slug = args.destination.lower().replace(' ', '_')
    image_subfolder = f"{year}/{dest_slug}-{month_name}"
    
    # Structured Temp Storage
    temp_dir = os.path.join(repo_root, '.local_photos', year, f"{dest_slug}-{month_name}")
    target_img_dir = os.path.join(repo_root, 'assets', 'images', image_subfolder)

    # 1. Image Acquisition
    local_files = []
    if os.path.exists(temp_dir):
        for f in os.listdir(temp_dir):
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.webp')):
                local_files.append((os.path.join(temp_dir, f), f))

    if args.rewrite:
        print(f"[Rewrite Mode] Using {len(local_files)} existing photos from {temp_dir}...")
    elif not local_files:
        print("Authenticating with Google Photos...")
        creds = get_credentials()
        photos_api = PhotosAPI(creds)
        items = photos_api.pick_photos(args.destination)
        if items:
            local_files = photos_api.download_photos(items, temp_dir)

    if not local_files:
        print("No photos found. Run without --rewrite or check your selection.")
        return

    # 2. AI Content Generation
    api_key = os.getenv("GEMINI_API_KEY")
    generator = TravelogueGenerator(api_key=api_key)
    
    template_path = os.path.join(repo_root, 'posts', 'template.html')
    with open(template_path, 'r') as f:
        template_content = f.read()

    html_content = generator.generate_html_post(local_files, args.destination, args.start_date, template_content, image_subfolder)
    
    if not html_content:
        return

    # 3. Save Post
    out_dir = os.path.join(repo_root, 'posts', year)
    os.makedirs(out_dir, exist_ok=True)
    out_filename = f"{dest_slug}-{month_name}.html"
    out_filepath = os.path.join(out_dir, out_filename)
    
    with open(out_filepath, 'w') as f:
        f.write(html_content)

    # 4. Finalize Assets & Homepage
    os.makedirs(target_img_dir, exist_ok=True)
    
    # Detect the Hero image from the HTML output
    # We look for ANY image src that points to our organized folder
    hero_match = re.search(fr'src="(\.\./\.\./assets/images/{image_subfolder}/[^"]*)"', html_content)
    hero_web_path = hero_match.group(1) if hero_match else None
    
    # Fallback to first image if regex fails
    if not hero_web_path and local_files:
        hero_web_path = f"../../assets/images/{image_subfolder}/{local_files[0][1]}"
    
    print(f"\n[Finalizing] Syncing images to {target_img_dir}...")
    for src_path, filename in local_files:
        shutil.copy2(src_path, os.path.join(target_img_dir, filename))

    if hero_web_path:
        relative_post_path = f"posts/{year}/{out_filename}"
        update_homepage(repo_root, args.destination, relative_post_path, hero_web_path)

    print(f"\n🚀 SUCCESS! OVERHAUL COMPLETE.")
    print(f"Post: {out_filepath}")
    print(f"Images: {target_img_dir}")

if __name__ == '__main__':
    main()
