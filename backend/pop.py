import os
import re
from mutagen.easyid3 import EasyID3

music_folder = "../music"

pattern = re.compile(r'^[^\"＂\']+["＂\'](.*?)["＂\']\s+by\s+([^[]+)', re.IGNORECASE)

# Map emoji to country
emoji_country = {
    "🇬🇧": "GB",
    "🇺🇸": "US",
    "🇪🇸": "ES",
    "🇫🇷": "FR",
    "🇩🇪": "DE",
    "🇮🇹": "IT",
    "🇯🇵": "JP",
    "🇨🇳": "CN",
    "🇷🇺": "RU",
    "🇧🇷": "BR",
    "🇵🇱": "PL",
    "🇨🇦": "CA",
    "🇦🇺": "AU",
    "🇳🇿": "NZ",
    "🇧🇪": "BE",
    "🇨🇷": "CR",
    "🇬🇷": "GR",
    "🇳🇱": "NL",
    "🇮🇳": "IN",
    "🇸🇪": "SE"
    # Add more as needed
}

for filename in os.listdir(music_folder):
    if not filename.endswith(".mp3"):
        continue

    match = pattern.search(filename)
    if match:
        title = match.group(1).strip()
        artist = match.group(2).strip()
    else:
        title = filename.replace(".mp3", "").strip()
        artist = "Unknown Artist"

    # Find emoji in filename for country
    country = "Unknown"
    for emoji, code in emoji_country.items():
        if emoji in filename:
            country = code
            break
    if(country == "Unknown"):
        print("No country emoji found for ", filename)


    filepath = os.path.join(music_folder, filename)
    try:
        audio = EasyID3(filepath)
    except:
        audio = EasyID3()  # create new tags if missing

    audio["title"] = title
    audio["artist"] = artist
    audio["releasecountry"] = country  # Store country in comment field
    audio.save(filepath)
    print(f"Tagged: {filename} -> Title: {title}, Artist: {artist}, Country: {country}")
