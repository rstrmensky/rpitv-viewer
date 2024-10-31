import csv
import vlc
import pygame

PLAYLIST_FILE = 'playlist.csv'

# Load the playlist from CSV file
def load_playlist():
    playlist = []
    with open(PLAYLIST_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            playlist.append(row)
    return sorted(playlist, key=lambda x: int(x['display_order']))

playlist = load_playlist()

# Create the display
def display_init():
    pygame.display.init()
    pygame.display.set_caption("RPiTV Signage")
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
    screen.fill((0, 0, 0))
    return screen

# Display video using VLC
def display_video(file_path):
    instance = vlc.Instance('--no-xlib --fullscreen')
    player = instance.media_player_new()
    media = instance.media_new(file_path)
    player.set_media(media)
    player.play()

    while player.get_state() not in [vlc.State.Ended, vlc.State.Error]:
        pygame.time.Clock().tick(1)

    player.stop()
    instance.release()

# Display image using Pygame
def display_image(screen, file_path, display_time):
    image = pygame.image.load(file_path).convert()
    image = pygame.transform.scale(image, (pygame.display.Info().current_w, pygame.display.Info().current_h))
    screen.blit(image, (0, 0))
    pygame.display.flip()
    pygame.time.Clock().tick(1 / int(display_time))

# Main loop to display media from the playlist
def main_loop():
    try:
        pygame.init()
        screen = display_init()
        while True:
            for media in playlist:
                if media["media_type"] == "video":
                    pygame.display.quit()

                    print(f"Displaying video: {media['file_path']}")
                    display_video(media["file_path"])
                elif media["media_type"] == "image":
                    if not pygame.display.get_init():
                        screen = display_init()

                    print(f"Displaying image: {media['file_path']} for {media['display_time']} seconds")
                    display_image(screen, media["file_path"], media["display_time"])
    finally:
        pygame.quit()

if __name__ == "__main__":
    main_loop()
