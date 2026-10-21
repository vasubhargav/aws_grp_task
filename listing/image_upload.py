import cloudinary.uploader


def upload_property_image(image_file):
    result = cloudinary.uploader.upload(
        image_file,
        folder="bluenest/properties",
        resource_type="image",
    )

    return result["secure_url"]