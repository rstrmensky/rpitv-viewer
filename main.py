import time
import subprocess

# Function to run the playlist update script
def run_playlist():
    try:
        subprocess.run(["python", "rpitv-playlist.py"])
    except subprocess.CalledProcessError as e:
        print(f"Error running playlist update: {e}")

# Function to start the player process
def run_player():
    try:
        player_process = subprocess.Popen(["python", "rpitv-player.py"])
        return player_process
    except Exception as e:
        print(f"Error starting player process: {e}")
        return None

if __name__ == "__main__":
    try:
        # Run update playlist initially
        run_playlist()

        # Start player process
        player_process = run_player()

        # Check for updates every 5 minutes
        while True:
            time.sleep(300)  # 300 seconds = 5 minutes
            run_playlist()
            # If player process is not running, start it again
            if player_process and player_process.poll() is not None:
                player_process = run_player()

    except KeyboardInterrupt:
        print("Hlavný proces prerušený užívateľom.")

        if player_process:
            player_process.terminate()

        print("Ukončenie dokončené.")
