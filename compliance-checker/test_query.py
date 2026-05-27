from app.services.document_processor import extract_text_from_pdf
import os

# Find the uploaded file
upload_dir = "uploads"
files = os.listdir(upload_dir)
print("Files in uploads:", files)

# Extract and print the full text
if files:
    path = os.path.join(upload_dir, files[0])
    text = extract_text_from_pdf(path)
    print(f"\nTotal characters extracted: {len(text)}")
    print("\n--- EXTRACTED TEXT ---")
    print(text)