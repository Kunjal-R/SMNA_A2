import json
import pandas as pd
from youtubeClient import youtubeClient


def fetchYoutubeData(videoIds, maxCommentsPerVideo=300, outputFile="youtubeDataDump.json"):

    client = youtubeClient()

    print(f"Fetching data for {len(videoIds)} videos...\n")

    statsResponse = client.videos().list(
        id=",".join(videoIds),
        part="snippet,statistics"
    ).execute()

    videos = []
    video_rows = []
    comment_rows = []

    for item in statsResponse.get("items", []):
        snippet = item["snippet"]
        stats = item.get("statistics", {})

        videoId = item["id"]

        video = {
            "title": snippet.get("title"),
            "videoId": videoId,
            "channelTitle": snippet.get("channelTitle"),
            "publishedAt": snippet.get("publishedAt"),
            "description": snippet.get("description"),
            "viewCount": int(stats.get("viewCount", 0)),
            "likeCount": int(stats.get("likeCount", 0)),
            "commentCount": int(stats.get("commentCount", 0)),
            "comments": []
        }

        video_rows.append({
            "video_id": videoId,
            "title": snippet.get("title"),
            "channel": snippet.get("channelTitle"),
            "published_at": snippet.get("publishedAt"),
            "description": snippet.get("description"),
            "view_count": int(stats.get("viewCount", 0)),
            "like_count": int(stats.get("likeCount", 0)),
            "comment_count": int(stats.get("commentCount", 0))
        })

        print(f"Fetching comments for: {snippet.get('title')[:60]}...")

        try:
            comments_fetched = 0
            next_page_token = None

            while True:
                request_limit = min(100, maxCommentsPerVideo - comments_fetched)

                if request_limit <= 0:
                    break

                commentResponse = client.commentThreads().list(
                    videoId=videoId,
                    part="snippet",
                    maxResults=request_limit,
                    pageToken=next_page_token,
                    textFormat="plainText",
                    order="relevance"
                ).execute()

                for commentThread in commentResponse.get("items", []):
                    topComment = commentThread["snippet"]["topLevelComment"]["snippet"]

                    comment_data = {
                        "video_id": videoId,
                        "video_title": snippet.get("title"),
                        "author": topComment.get("authorDisplayName"),
                        "comment_text": topComment.get("textDisplay"),
                        "comment_published_at": topComment.get("publishedAt"),
                        "comment_like_count": topComment.get("likeCount", 0)
                    }

                    video["comments"].append({
                        "author": comment_data["author"],
                        "text": comment_data["comment_text"],
                        "publishedAt": comment_data["comment_published_at"],
                        "likeCount": comment_data["comment_like_count"]
                    })

                    comment_rows.append(comment_data)

                    comments_fetched += 1

                    if comments_fetched >= maxCommentsPerVideo:
                        break

                if comments_fetched >= maxCommentsPerVideo:
                    break

                next_page_token = commentResponse.get("nextPageToken")

                if not next_page_token:
                    break

            print(f" → {len(video['comments'])} comments collected\n")

        except Exception as e:
            print(f" → Error or comments disabled: {e}\n")

        videos.append(video)

    with open(outputFile, "w", encoding="utf-8") as f:
        json.dump({"videos": videos}, f, ensure_ascii=False, indent=2)

    videos_df = pd.DataFrame(video_rows)
    comments_df = pd.DataFrame(comment_rows)

    videos_df.to_csv("videos.csv", index=False, encoding="utf-8")
    comments_df.to_csv("comments.csv", index=False, encoding="utf-8")

    print(f"\nDone. Data saved to:")
    print(f"- {outputFile}")
    print("- videos.csv")
    print("- comments.csv")


if __name__ == "__main__":

    VIDEO_IDS = [
        "laZpTO7IFtA",
        "p-N3-Q8WyfU",
        "qGx4VtwMnfM",
        "pYOsZhxLSOM",
        "f22lD2DVXH8",
        "H86iO0mtsDI",
        "-FNIAzYLCQA",
        "7Od5rp1AFYk",
        "tdIUMkXxtHg",
        "2wcusKGZ7dw",
        "Jfz0ghTlFzQ",
        "_zfN9wnPvU0",
        "aNvvOQMx0jY",
        "uw7kllUlI_g",
        "4esV4R3k1V8",
        "KiwIqjcgSQw",
        "daOX828qFME",
        "p5SepyRGECQ",
        "BFgg-Gy0E2g",
        "pH-ANrubHXg",
        "Uas_T2K8s9o",
        "f-e5_NomUpk"
    ]

    MAX_COMMENTS = 300

    fetchYoutubeData(VIDEO_IDS, MAX_COMMENTS)