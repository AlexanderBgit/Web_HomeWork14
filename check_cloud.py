import cloudinary
from cloudinary.uploader import upload

# Встановлення конфігурації для Cloudinary
cloudinary.config(
    cloud_name = "", 
    api_key = "", 
    api_secret = "" 
)

# URL зображення, яке ви хочете завантажити
image_url = "https://upload.wikimedia.org/wikipedia/commons/a/ae/Olympic_flag.jpg"

# Параметри завантаження
upload_options = {
    "public_id": "olympic_flag",  # Ім'я, під яким зображення буде збережене в Cloudinary
}

# Завантаження зображення
result = upload(image_url, **upload_options)

# Виведення результатів
print(result)
