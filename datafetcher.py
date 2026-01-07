import os
import time
import requests
import pandas as pd
import logging

# ------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned", "train_clean.csv")
IMAGE_SAVE_DIR = os.path.join(BASE_DIR, "data", "images")
LOG_PATH = os.path.join(BASE_DIR, "image_fetch.log")
# ------------------------------------------

MAPBOX_TOKEN = "pk.eyJ1IjoiZG9vZmVuc2htaXJ0ejE2IiwiYSI6ImNtam9va285bzIybXAzZnNjczdmY2Y0cmQifQ.32nZl4pM6SgcqqmarBOmpg"
IMAGE_SIZE = "224x224"
ZOOM = 16
STYLE = "satellite-v9"

os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

# ------------------------------------------
# Logging setup
# ------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ------------------------------------------

def fetch_image(lat, lon, house_id, retries=3):
    url = (
        f"https://api.mapbox.com/styles/v1/mapbox/{STYLE}/static/"
        f"{lon},{lat},{ZOOM}/"
        f"{IMAGE_SIZE}"
        f"?access_token={MAPBOX_TOKEN}"
    )

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                img_path = os.path.join(IMAGE_SAVE_DIR, f"{house_id}.png")
                with open(img_path, "wb") as f:
                    f.write(response.content)

                logger.info(f"Downloaded image for ID {house_id}")
                return

            else:
                logger.warning(
                    f"Status {response.status_code} for ID {house_id} (attempt {attempt})"
                )

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Request error for ID {house_id} (attempt {attempt}): {e}"
            )
            time.sleep(2)

    logger.error(f"Skipped ID {house_id} after {retries} retries")


def main():
    logger.info("Image fetching started")

    df = pd.read_csv(DATA_PATH)
    df = df.sample(4000, random_state=40)

    total = len(df)

    for idx, row in df.iterrows():
        house_id = row["id"]
        lat = row["lat"]
        lon = row["long"]

        if pd.isna(lat) or pd.isna(lon):
            logger.warning(f"Missing coordinates for ID {house_id}, skipping")
            continue

        img_path = os.path.join(IMAGE_SAVE_DIR, f"{house_id}.png")
        if os.path.exists(img_path):
            logger.info(f"Image already exists for ID {house_id}, skipping")
            continue

        fetch_image(lat, lon, house_id)

        if idx % 100 == 0:
            logger.info(f"Progress: {idx}/{total}")

        time.sleep(0.5)  # avoid rate limit

    logger.info("Image fetching completed")


if __name__ == "__main__":
    main()
