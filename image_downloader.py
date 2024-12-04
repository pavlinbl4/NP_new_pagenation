import csv
import os
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image
from tqdm import tqdm


# pip install requests Pillow


def downloader(image_url: str, image_name: str, folder_path: Path):
    try:
        response = requests.get(image_url, stream=True)

        # Step 2: Open the image using Pillow
        image = Image.open(BytesIO(response.content))

        # Step 3: Convert to RGB (JPEG does not support transparency)
        rgb_image = image.convert('RGB')

        # Step 4: Save the image as JPEG
        rgb_image.save(f"{folder_path}/{image_name}.JPG", 'JPEG')

    except Exception as ex:
        print(ex)


def image_downloader(csv_file_path, month, month_number, current_year, folder_path):
    # create folder to downloading images
    path_to_folder = f"{folder_path}/{current_year}_{month_number}"
    os.makedirs(path_to_folder, exist_ok=True)

    # read data from csv file
    with open(csv_file_path, 'r') as input_file:
        reader = csv.reader(input_file)

        for row in tqdm(reader, colour='blue', ncols=1000, desc="Image downloading"):
            if month in row[0]:
                image_url = row[2]
                downloader(image_url, path_to_folder, f'{row[0]}__{row[1]}')


if __name__ == '__main__':
    image_downloader(f'{Path().home()}/Documents/NewProspect/NP.csv',
                     'июля', 7, 2023, f'{Path().home()}/Documents/NewProspect')
