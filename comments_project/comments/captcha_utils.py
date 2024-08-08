import os
import random
import string
from captcha.image import ImageCaptcha
from django.conf import settings


def generate_captcha():
    static_dir = os.path.join(settings.BASE_DIR, 'static', 'captcha')

    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    for file_name in os.listdir(static_dir):
        file_path = os.path.join(static_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    image_captcha = ImageCaptcha()
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    image = image_captcha.generate_image(captcha_text)

    image_file_name = f'captcha_{captcha_text}.png'
    image_file_path = os.path.join(static_dir, image_file_name)
    image.save(image_file_path, format='PNG')

    return captcha_text, image_file_name
