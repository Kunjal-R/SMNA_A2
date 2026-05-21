import sys
from googleapiclient.discovery import build


def youtubeClient():
    try:
        apiKey = "AIzaSyCV8cUc0AnPS0GB_8YusKJWGHBzc4S3BHA"

        youtube = build(
            "youtube",
            "v3",
            developerKey=apiKey
        )

    except Exception as e:
        sys.stderr.write(f"Failed to create YouTube client: {e}\n")
        sys.exit(1)

    return youtube