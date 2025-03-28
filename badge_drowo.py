import csv
import os
from PIL import Image, ImageDraw, ImageFont


def read_names_from_csv(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        names = []
        for row in reader:
            if len(row) >= 2:
                first_names = " ".join(row[:-1])  # all elements except the last ones are first names
                last_name = row[-1]  # the last element is a surname
                names.append((first_names, last_name))
    return names


def generate_badge(template_path, output_path, first_name, last_name):
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)
    max_width, max_height = 520, 170  # this is the maximum dimension of the textbox for my template, is modified with each template
    font_size = 150  # start off with a big size

    font_path = "GeorgiaPro-Black.ttf"  # can change fonts but make sure the ttf file is installed

    while font_size > 10: #the point is to make the font size smaller and smaller until it fits in my textbox
        font = ImageFont.truetype(font_path, font_size)
        text = f"{first_name} {last_name}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # if the text fits in the box, stop
        if text_width <= max_width and text_height <= max_height:
            break
        font_size -= 2

    # if the writing becomes too small, split in two rows
    if font_size <= 50:
        font_size = 80  # reset the font size to a bigger value
        font = ImageFont.truetype(font_path, font_size)

        full_name = f"{first_name} {last_name}"
        words = full_name.split()
        half = len(words) // 2
        line1 = " ".join(words[:half])
        line2 = " ".join(words[half:])

        # adjust the font for each row to fit
        while font_size > 10:
            # Calculăm dimensiunile pentru fiecare linie
            bbox1 = draw.textbbox((0, 0), line1, font=font)
            bbox2 = draw.textbbox((0, 0), line2, font=font)
            text_width1 = bbox1[2] - bbox1[0]
            text_width2 = bbox2[2] - bbox2[0]

            # if both rows fit the maximum size, stop
            if text_width1 <= max_width and text_width2 <= max_width:
                break
            font_size -= 2  # Dacă nu încap, micșorăm fontul

            # update the font to the actual properties
            font = ImageFont.truetype(font_path, font_size)

        # calculate the dimensions for each row wirth the updates font
        bbox1 = draw.textbbox((0, 0), line1, font=font)
        bbox2 = draw.textbbox((0, 0), line2, font=font)
        text_width1 = bbox1[2] - bbox1[0]
        text_width2 = bbox2[2] - bbox2[0]

        # calculate the centering positions
        pos_x1 = 245 + (max_width - text_width1) // 2
        pos_x2 = 245 + (max_width - text_width2) // 2

        # positions on the badge; changes with each template
        pos_y1 = 475
        pos_y2 = 525 

        # adjust the space between the lines
        line_height = bbox1[3] - bbox1[1] + 10 
        pos_y2 = pos_y1 + line_height 

        draw.text((pos_x1, pos_y1), line1, fill="white", font=font)
        draw.text((pos_x2, pos_y2), line2, fill="white", font=font)

    else:
        # if the font is not too small, it fits on one row
        text_position = (245, 515)
        draw.text(text_position, text, fill="white", font=font)

    image.save(f"{output_path}/{first_name.replace(' ', '_')}_{last_name}.png")


def process_badges(csv_filename, template_path, output_path):
    os.makedirs(output_path, exist_ok=True)  #this creates the folder if it doesnt exist
    names = read_names_from_csv(csv_filename)
    for first_name, last_name in names:
        generate_badge(template_path, output_path, first_name, last_name)


# my current example of files
csv_filename1 = "logistic_data.txt"
template_path1 = "logistic_template.png"
output_path1 = "badges_logistic"
process_badges(csv_filename1, template_path1, output_path1)
