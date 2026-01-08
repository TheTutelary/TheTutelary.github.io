Deployment Guide: Desi European

This guide explains how to take the files we created and deploy them to GitHub Pages properly.

Phase 1: Create the Folder Structure (On your Computer)

Create a new folder on your Desktop named my-website.

Inside that folder, create the following structure:

my-website/
├── index.html       (Paste the code from File 1)
├── about.html       (Paste the code from File 2)
├── template.html    (Paste the code from File 3)
└── README.md        (This file)


Phase 2: Upload to GitHub

Go to your GitHub Repository (yourusername.github.io).

Click Add file -> Upload files.

Drag and drop all the files you created (index.html, about.html, template.html) into the box.

In the "Commit changes" box at the bottom, type: "Launched full site structure".

Click the green Commit changes button.

Phase 3: How to Write a New Post (The Workflow)

When you want to write a new story (e.g., "My Trip to Berlin"):

Open your GitHub repository.

Click on template.html.

Click the Copy icon (two squares) to copy the raw code.

Go back to the main page and click Add file -> Create new file.

Name the file: berlin-trip.html.

Paste the code you copied.

Edit the Title and Text inside the file.

Commit the file.

Important: Linking the new post

After creating berlin-trip.html, you must update your Homepage (index.html) so people can find it!

Open index.html.

Find the Latest Stories section.

Change one of the links (href="template.html") to href="berlin-trip.html".

Update the title and image for that card.

Commit changes.

Phase 4: The "Pro" Move (CSS Extraction)

Currently, the styling (CSS) is repeated in every file. This is okay for now, but if you want to change the Main Color (Orange) later, you have to do it in 3 files.

To fix this:

Create a new file on GitHub named style.css.

Copy everything between the <style> and </style> tags from index.html and paste it there.

In your HTML files (index.html, about.html, etc.), delete the <style>...</style> block.

Replace it with this single line:
<link rel="stylesheet" href="style.css">

Now, you have one file to control the design of the entire website!