from pdf2image import convert_from_bytes

def pdf_to_images(file):
    # Read file bytes
    pdf_bytes = file.read()

    # Convert PDF bytes directly to images
    images = convert_from_bytes(pdf_bytes)

    # Save or convert images to base64 strings
    base64_images = []
    for img in images:
        import io, base64
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        base64_images.append(img_str)
    return base64_images