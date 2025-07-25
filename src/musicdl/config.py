from datetime import datetime
import warnings
import sys
import os

from dotenv import dotenv_values, find_dotenv

def load_config(dotenv_path: str = None):
    if dotenv_path is not None and not os.path.exists(dotenv_path):
        dotenv_path = os.path.abspath(dotenv_path)
        warnings.warn(f"Note: {dotenv_path} does not exist")
        dotenv_path = find_dotenv(filename=".env", usecwd=True)
        if dotenv_path != "":
            warnings.warn(f"using {dotenv_path}")
        else:
            warnings.warn("using enviroment variables")
    elif dotenv_path is None:
        dotenv_path = find_dotenv(filename=".env", usecwd=True)
    dotenv_path = os.path.abspath(dotenv_path)
    env = dotenv_values(dotenv_path)

    config = {
        # https://developer.spotify.com/documentation/web-api/tutorials/getting-started
        "client_id": env.get("SPOTIFY_CLIENT_ID") or os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": env.get("SPOTIFY_CLIENT_SECRET") or os.getenv("SPOTIFY_CLIENT_SECRET"),

        # specify the directory where data should be stored prior to creating zip file
        "datadir": env.get("DATADIR") or "./data",

        # specify where zip file should be stored (default: tracks_{TODAYSDATE}.zip)
        "zip": env.get("ZIPFILE") or None

        # "hash_mp3_storage": env.get("HASH_MP3_STORAGE") or "False"
        # "num_bins": env.get("NUM_BINS") or "10"
        # "single_file": env.get("SINGLE_FILE") or "True"
    }
    client_id, client_secret = config.get("client_id"), config.get("client_secret")
    if client_id is None or client_secret is None or client_id == "" or client_secret == "":
        print("\n".join([f"Spotify API Credentials not found in {dotenv_path} or in environment variables",
                         "Please provide SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET",
                         "https://developer.spotify.com/documentation/web-api/tutorials/getting-started"
                         ]))
        exit(1)

    config["music_db"] = os.path.join(config["datadir"], "music.db")
    config["mp3_storage"] = os.path.join(config["datadir"], "mp3s")
    config["csv_storage"] = config["datadir"]
    config["single_file"] = True

    # make the zip file path a callable so that we have the correct date when exporting
    if config["zip"] is None:
        config["zip"] = lambda: f'tracks-{datetime.today().strftime("%Y-%m-%d")}.zip'
    else:
        config["zip"] = lambda: config["zip"]

    #config["hash_mp3_storage"] = config["hash_mp3_storage"] == "True"
    #config["num_bins"] = int(config["num_bins"])
    #config["single_file"] = config["single_file"] == "True"

    ###################################################################
    # NOTE: utilize the following config options if you find yourself 
    #       wanting to download a massive number of mp3 files

    config["hash_mp3_storage"] = False
    config["num_bins"] = 10   # [1,100]

    ###################################################################




    return config

config: dict[str, str] = load_config()
