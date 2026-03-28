# Google Photos Travelogue Generator

This tool securely connects to your Google Photos, retrieves photos within a specific date range, **intelligently filters them based on your destination's visual context** using Google Gemini 1.5 Pro, and automatically generates an HTML travelogue post based on your website's template.

## Features
- **Secure OAuth Integration:** Read-only access to your Google Photos library.
- **Intelligent Filtering:** API limitations prevent us from seeing exact GPS coordinates on downloaded photos. This tool bypasses that by using Google Gemini Vision to visually analyze the batch of photos and keep only the ones that match the intended destination (e.g., recognizing landmarks or signs).
- **Automated Generation:** Feeds the relevant photos into Gemini 1.5 Pro to write a thorough, engaging travelogue post directly into your HTML template structure.
- **Git Safety:** Downloaded photos are stored in `.local_photos/` and excluded from your git repository to save space.

## Prerequisites

1. **Google Cloud Console:**
   - Create a project at [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the **Google Photos Library API**.
   - Create OAuth 2.0 Client ID credentials (Desktop Application).
   - Download the JSON file and save it as `credentials.json` in this directory (`tools/travelogue-generator/`).

2. **Google Gemini API Key:**
   - Get an API key from [Google AI Studio](https://aistudio.google.com/).
   - Create a file named `.env` in this directory and add:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

## Installation

We recommend creating a virtual environment:

```bash
cd tools/travelogue-generator/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the script by providing the destination, start date, and end date:

```bash
python main.py "Destination Name" YYYY-MM-DD YYYY-MM-DD
```

**Example:**
```bash
python main.py "Prague" 2022-06-01 2022-06-15
```

The first time you run this, a browser window will open asking you to log in to your Google Account and grant permission to view your photos. A `token.json` file will be saved locally so you don't have to log in every time.

The generated HTML file will automatically be saved into `posts/YYYY/destination-name.html`.