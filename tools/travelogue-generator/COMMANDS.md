# 🍌 Desi European: Travelogue Engine Guide

This document covers all the commands and workflows for your automated travelogue system.

## 🛠 Setup (One-time)
Before running the engine, ensure your virtual environment is active:
```bash
cd tools/travelogue-generator/
source venv/bin/activate
```

---

## 🚀 Core Commands

### 1. Generate a New Post
Use this when you have new photos in Google Photos. It will open the Picker, download photos, and generate the story.
```bash
python main.py "Destination Name" YYYY-MM-DD
```
*Example:* `python main.py "Prague" 2022-06-15`

### 2. Rewrite/Refine an Existing Post
Use this to regenerate the story or fix the layout without downloading photos again. It uses the photos already in your `.local_photos/` folder.
```bash
python main.py "Destination Name" YYYY-MM-DD --rewrite
```
**Pro Tip:** You can manually add/remove photos from the structured `.local_photos/YYYY/destination-month/` folder and then run `--rewrite` to force the AI to use your specific selection.

### 3. Local Publishing (Preview)
Start the local server to see your changes exactly as they will appear online.
```bash
# From the repository root
python3 -m http.server 8000
```
*Access at:* [http://localhost:8000](http://localhost:8000)

---

## 📁 System Structure

- **Raw Downloads (Ignored by Git):** `.local_photos/[Year]/[destination]-[month]/`
- **Permanent Images (Tracked by Git):** `assets/images/[Year]/[destination]-[month]/`
- **Automated Processing:** The engine automatically converts all images to **WebP** (optimized for speed) and **strips all GPS/EXIF metadata** before moving them to the permanent assets folder to ensure your family's privacy.
- **Blog Posts:** `posts/[Year]/[destination]-[month].html`
- **Homepage Automation:** The engine automatically updates `index.html` with:
    - The "Star" image for the destination card.
    - A new story card in the "Latest Stories" section.

---

## 🧠 Advanced Tips
- **Hero Image:** If you want to change the "Star" image on the homepage, rename your preferred photo to something distinct in the local folder and run `--rewrite`. The AI will prioritize high-impact shots.
- **Month Overrides:** If the automatic month extraction (from the date) is wrong, use:
  `python main.py "Prague" 2022-06-15 --month "jul"`
- **Clean Slate:** To fully reset a trip, delete its folder in both `.local_photos` and `assets/images` before running the generate command.
