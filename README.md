Anime Film Engine v7 – Cinematic Visual Novel in Pygame

A Python engine built with Pygame that combines cinematic effects with a basic visual novel system. Perfect for creating short animated sequences, atmospheric scenes, and dialogue-driven storytelling.

Features
Cinematic Features

Dynamic day-night cycle with sun and moon.

Parallax clouds and distant hills for depth.

Aura effects around characters.

Rain with lightning and thunder, including camera shake.

Twinkling stars and fireflies / magical lights.

Film grain and vignette overlay for cinematic feel.

Letterbox effect, title screen, and scrolling credits.

Visual Novel Features

Multiple characters on screen (left, center, right).

Dialogue box with name tags and timed dialogue.

Scene triggers that control effects like rain, lightning, or fireflies.

Fully extendable timeline for new scenes and dialogues.

Requirements

Python 3.x

Pygame
 (pip install pygame)

Optional:

A background music file named music.mp3 in the same directory.

A thunder sound file named thunder.wav in the same directory.

How to Run

Clone this repository:

git clone https://github.com/hassanmiguel/ANIME-ENGINE-v3.git


Install Pygame if you haven’t:

pip install pygame


Place your music.mp3 and thunder.wav (optional) in the project folder.

Run the engine:

python main.py

How to Use / Extend

Add characters: Update the characters dictionary with new names, positions ("left", "center", "right"), and color or sprite.

characters["New Character"] = {"pos": "center", "color": (255,200,50)}


Add dialogue: Append new scene entries to the scenes list with time (in seconds), dialogue, and optional effects ("rain", "fireflies", "lightning").

scenes.append({
    "time": 50,
    "dialog": ("New Character", "This is a new line of dialogue."),
    "effects": ["rain"]
})


Add visual effects: Use add_aura(x, y) or add_rain(amount) anywhere in the timeline.

Modify timeline duration: Change TOTAL = 60 (seconds) to control the length of the animation.

Screenshots / Example

Optional: Add screenshots of your engine running here.

License

MIT License – free to use, modify, and share.
