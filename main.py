import csv
import os
from PIL import Image, ImageDraw, ImageFont

output_path = "badges"
os.makedirs(output_path, exist_ok=True) # ma asigur ca exista folderul (la un moment dat aveam o problema ; cred ca pot fi scoase astea 2 linii

def read_names_from_csv(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        names = []
        for row in reader:
            if len(row) >= 2:
                first_names = " ".join(row[:-1])  # Toate elementele mai puțin ultimul sunt prenume (asa m-am gandit eu, poate fi schimbat)
                last_name = row[-1]  # Ultimul element este numele de familie
                names.append((first_names, last_name))
    return names


def generate_badge(template_path, output_path, first_name, last_name):
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)
    max_width, max_height = 630, 100  # Basically fac un chenar in care sa se incadreze textul care are marimile astea
    font_size = 150  # Dimensiune inițială mai mare

    while font_size > 10:
        font = ImageFont.truetype("calibri.ttf", font_size)
        text = f"{first_name} {last_name}"
        bbox = draw.textbbox((0, 0), text, font=font)  # iau bounding box-ul textului
        text_width = bbox[2] - bbox[0]  # Width of the text
        text_height = bbox[3] - bbox[1]  # Height of the text
        if text_width <= max_width and text_height <= max_height:
            break
        font_size -= 2

    # print(f"Font size for {first_name} {last_name}: {font_size}")
    text_position = (200, 970)  # Pozitia de la care sa inceapa sa scrie in template
    draw.text(text_position, text, fill="black", font=font)
    image.save(f"{output_path}/{first_name.replace(' ', '_')}_{last_name}.png")


def process_badges(csv_filename, template_path, output_path):
    names = read_names_from_csv(csv_filename)
    for first_name, last_name in names:
        generate_badge(template_path, output_path, first_name, last_name)
    # print("\nGenerated badges for the following names:")
    # for first_name, last_name in names:
        # print(f"- {first_name} {last_name}")

# Exemplu de apel
csv_filename = "nume.txt"
template_path = "badge_template.png"
output_path = "badges"
process_badges(csv_filename, template_path, output_path)
