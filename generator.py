from PIL import Image, ImageDraw, ImageFont
import os

def make_cert(name):
    if not os.path.exists("uploads/certs"): os.makedirs("uploads/certs")
    img = Image.open("assets/template.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("assets/arial.ttf", 60)
    # Ismni markazga joylashtirish (koordinatalar namuna uchun)
    draw.text((350, 450), name, fill="black", font=font)
    path = f"uploads/certs/cert_{name}.jpg"
    img.save(path)
    return path
