import requests
import os
from pathlib import Path
from dotenv import load_dotenv
import random


HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }


def download_image(url, filename):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    file_extension = get_file_extension(url)
    img_path = os.path.join('images', f'{filename}{file_extension}')
    with open(img_path, 'wb') as file:
        file.write(response.content)
    return img_path


def get_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_file_extension(file_name):
    return os.path.splitext(file_name)[-1]


def create_default_folder():
    Path('images').mkdir(parents=True, exist_ok=True)


def get_last_comics_id():
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    return response.json()['num']


def get_upload_url():
    params = {
        'access_token': os.getenv('access_token'),
        'v': 5.103,
        'group_id': os.getenv('group_id')
    }
    response = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params=params)
    response.raise_for_status()
    check_status(response)
    return response.json()['response']['upload_url']


def check_status(response):
    if 'error' in response.json():
        raise requests.exceptions.HTTPError(response.json()['error'])


def upload_photo(upload_url, img_path):
    with open(img_path, 'rb') as file:
        files ={
            'photo': file
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
    return response.json()


def save_photo(upload_image_info):
    data = {
        'access_token': os.getenv('access_token'),
        'group_id': os.getenv('group_id'),
        'v': 5.103,
        'server': upload_image_info['server'],
        'photo': upload_image_info['photo'],
        'hash': upload_image_info['hash']
    }
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', data=data)
    response.raise_for_status()
    check_status(response)
    return response.json()


def publish_photo(result_save_photo, message):
    data = {
        'access_token': os.getenv('access_token'),
        'group_id': os.getenv('group_id'),
        'v': 5.103,
        'attachments': 'photo{}_{}'.format(result_save_photo['response'][0]['owner_id'],
                                           result_save_photo['response'][0]['id']),
        'owner_id': '-{}'.format(os.getenv('group_id')),
        'from_group': 1,
        'message': message
    }
    response = requests.post('https://api.vk.com/method/wall.post', data=data)
    response.raise_for_status()
    check_status(response)
    return response.json()


def main():
    create_default_folder()
    try:
        last_comics_id = get_last_comics_id()
        comics_id = random.randint(1, last_comics_id)
        comics_info = get_content(f'https://xkcd.com/{comics_id}/info.0.json')
        img_path = download_image(comics_info['img'], comics_id)
        upload_url = get_upload_url()
        upload_image_info = upload_photo(upload_url, img_path)
        result_save_photo = save_photo(upload_image_info)
        result_publish = publish_photo(result_save_photo, comics_info['alt'])
        os.remove(img_path)
    except requests.exceptions.HTTPError as error:
        print(f'Can`t get data:\n{error}')


if __name__ == '__main__':
    load_dotenv()
    random.seed()
    main()
