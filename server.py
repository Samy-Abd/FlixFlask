from flask import Flask, render_template, send_from_directory
import os
import random

app = Flask(__name__, template_folder='templates', static_folder='static')

def get_random_anime_info():
    anime_list = 'anime_list.txt'
    with open(anime_list, 'r') as file:
        lines = file.read().splitlines()
    selected_animes = random.sample(lines, 3)  # Ensure unique selection
    anime_info = []
    for anime in selected_animes:
        name, synopsis = anime.split(', ', 1)
        image_folder = os.path.join(app.static_folder, 'images', name.replace(' ', ' '))
        image_files = os.listdir(image_folder)
        image_file = random.choice(image_files)
        # image_path = os.path.join('images', name.replace(' ', ' '), image_file)
        image_path = 'images/' + name+ '/' + image_file
        anime_info.append({'name': name, 'synopsis': synopsis, 'image_path': image_path})
    return anime_info

def get_video_id(anime_name):
    with open('anime_video_ids.txt', 'r') as file:
        for line in file:
            name, video_id = line.strip().split(', ')
            if name == anime_name:
                return video_id
    return None

@app.route('/in_progress')
def in_progress():
    return render_template('in_progress.html')

@app.route('/anime/<anime_name>')
def anime_page(anime_name):
    video_id = get_video_id(anime_name)
    # Optional: You might want to fetch more details about the anime here
    return render_template('anime_page.html', anime_name=anime_name, video_id=video_id)


def get_specific_anime_info(anime_name):
    # Assuming you have a function or a way to get specific anime info
    # This is a placeholder function. You need to implement it based on your data structure.
    anime_list = 'anime_list.txt'
    with open(anime_list, 'r') as file:
        for line in file:
            name, synopsis = line.strip().split(', ', 1)
            if name == anime_name:
                image_folder = os.path.join(app.static_folder, 'images', name.replace(' ', '_'))
                image_files = os.listdir(image_folder)
                image_file = random.choice(image_files)
                image_path = 'images/' + name.replace(' ', '_') + '/' + image_file
                return {'name': name, 'synopsis': synopsis, 'image_path': image_path}
    return None




@app.route('/')
def home():
    profile_image_dir = os.path.join(app.static_folder, "images/pfps")
    profile_images = os.listdir(profile_image_dir)
    profile_image = random.choice(profile_images)
    anime_info = get_random_anime_info()
    return render_template('index.html', profile_image=profile_image, anime_info=anime_info)

if __name__ == '__main__':
    app.run(debug=True)
