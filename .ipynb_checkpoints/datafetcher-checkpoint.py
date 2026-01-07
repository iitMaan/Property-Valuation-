import os
import time
import requests
import pandas as pd

# ------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned", "train_clean.csv")
IMAGE_SAVE_DIR = os.path.join(BASE_DIR, "data", "images")
# ------------------------------------------

MAPBOX_TOKEN = "pk.eyJ1IjoiZG9vZmVuc2htaXJ0ejE2IiwiYSI6ImNtam9va285bzIybXAzZnNjczdmY2Y0cmQifQ.32nZl4pM6SgcqqmarBOmpg"
IMAGE_SIZE = "224x224"
ZOOM = 16
STYLE = "satellite-v9"

os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

def fetch_image(lat, lon, house_id, retries=3):
    url = (
        f"https://api.mapbox.com/styles/v1/mapbox/{STYLE}/static/"
        f"{lon},{lat},{ZOOM}/"
        f"{IMAGE_SIZE}"
        f"?access_token={MAPBOX_TOKEN}"
    )

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                with open(os.path.join(IMAGE_SAVE_DIR, f"{house_id}.png"), "wb") as f:
                    f.write(response.content)
                return
            else:
                print(f"Failed (status {response.status_code}) for ID {house_id}")

        except requests.exceptions.RequestException as e:
            print(f"Retry {attempt+1}/{retries} for ID {house_id}: {e}")
            time.sleep(2)

    print(f"Skipped ID {house_id} after retries")


def main():
    df = pd.read_csv(DATA_PATH)
    df = df.sample(4000, random_state=40)
    for _, row in df.iterrows():
        house_id = row["id"]
        lat = row["lat"]
        lon = row["long"]

        img_path = os.path.join(IMAGE_SAVE_DIR, f"{house_id}.png")
        if os.path.exists(img_path):
            continue

        fetch_image(lat, lon, house_id)
        time.sleep(0.5)  # avoid rate limit

if __name__ == "__main__":
    main()