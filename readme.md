Cosmic Guardian: Last Stand is an intergalactic adventure where you, the last survivor on Earth, must defend against an extraterrestrial invasion. As the only line of defense, pilot a futuristic yet makeshift spaceship constructed from salvaged scrap parts. Face increasingly challenging enemy U.F.O's across five rounds. Between rounds, engage in cosmic knowledge challenges. Click buttons and type answers swiftly to save Earth. Will you become the Cosmic Guardian and prevent humanity's extinction? Good luck, commander!

# RULES.
Getting a question right gives +5 health, wrong -5. You have the options to skip questions.
You need to click in order to destroy the enemies.
You can click the spaceship to heal it.
The way that the game gets increasingly difficult is that there are different enemy levels, and they spawn on certain levels detailed in enemy_data.py. They deal different amounts of damage and go faster or slower.
The way that chance is implemented is by making it so they can spawn anywhere on the Y axis, but converges at one point. Also the enemies to spawn list gets shuffled, also adding chance / randomness (world.py).
You need to type in the answers in the general game window. You may need to type or click buttons a few times.
The screen size is 1920x1080. Resize it and run the program again if it is very zoomed in or having other display errors.