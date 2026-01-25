from flask import Flask, Response
import requests
from constants_and_b64_assets import *
from utils import *

app = Flask(__name__)


@app.route("/<username>")
def index(username):

    if not validate_username(username=username):
        return {"error": "Invalid username"}, 400

    # Profile
    profile_url = f"{BASE_URL}/pub/player/{username}"
    profile_resp = requests.get(profile_url, headers=HEADERS)
    if profile_resp.status_code != 200:
        return {"error": "Could not fetch profile data from chess.com"}, 404
    profile_body = profile_resp.json()
    avatar_url = profile_body.get("avatar")
    profile_url = profile_body["url"]
    title = profile_body.get("title")
    country_url = profile_body["country"]
    country_code = country_url.split("/")[-1]
    last_online = profile_body["last_online"]
    last_online_formatted = format_last_online(timestamp=last_online)
    joined = profile_body["joined"]
    joined_month_year = convert_epoch_to_month_year(timestamp=joined)
    league = profile_body.get("league")

    # Stats
    stats_url = f"{BASE_URL}/pub/player/{username}/stats"
    stats_resp = requests.get(stats_url, headers=HEADERS)
    if stats_resp.status_code != 200:
        return {"error": "Could not fetch stats data from chess.com"}, 404
    stats_body = stats_resp.json()
    rapid_stats = normalize_stats(stats=stats_body.get("chess_rapid"))
    blitz_stats = normalize_stats(stats=stats_body.get("chess_blitz"))
    bullet_stats = normalize_stats(stats=stats_body.get("chess_bullet"))

    svg = generate_svg(
        profile_url=profile_url,
        avatar=avatar_url,
        country_code=country_code,
        username=username,
        league=league,
        title=title,
        joined=joined_month_year,
        last_seen=last_online_formatted,
        rapid_stats=rapid_stats,
        blitz_stats=blitz_stats,
        bullet_stats=bullet_stats,
    )

    return Response(
        svg,
        mimetype="image/svg+xml",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


if __name__ == "__main__":
    app.run(debug=True)
