from flask import Flask, Response, url_for
import requests
import datetime
import copy
import re

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

BASE_URL = "https://api.chess.com"

STATS_SCHEMA = {
    "last": {"rating": "N/A"},
    "best": {"rating": "N/A"},
    "record": {
        "win": "-",
        "draw": "-",
        "loss": "-",
    },
}

USERNAME_REGEX = re.compile("^[A-Za-z0-9](?:[A-Za-z0-9_-]{1,}[A-Za-z0-9])$")


def validate_username(username):
    return bool(USERNAME_REGEX.fullmatch(username))


def convert_epoch_to_month_year(timestamp):
    dt_obj = datetime.datetime.fromtimestamp(timestamp)
    dt_month_year = dt_obj.strftime("%b, %Y")
    return dt_month_year


def format_last_online(timestamp):
    dt_obj = datetime.datetime.fromtimestamp(timestamp)
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    if dt_obj.date() == today.date():
        return "Today"
    elif dt_obj.date() == yesterday.date():
        return "Yesterday"
    elif dt_obj.year == today.year and dt_obj.month == today.month:
        return "This month"
    else:
        return convert_epoch_to_month_year(timestamp=timestamp)


def generate_flag_svg(country_code):
    flag_coordinates = {
        "AD": [-40, 0],
        "AE": [-80, 0],
        "AF": [-120, 0],
        "AG": [-160, 0],
        "AI": [-200, 0],
        "AL": [-240, 0],
        "AM": [-280, 0],
        "AO": [-320, 0],
        "AR": [-360, 0],
        "AS": [-400, 0],
        "AT": [-0, -32],  # Austria
        "AU": [-40, -32],
        "AW": [-80, -32],
        "AX": [-120, -32],
        "AZ": [-160, -32],
        "BA": [-200, -32],
        "BB": [-240, -32],
        "BD": [-280, -32],
        "BE": [-320, -32],
        "BF": [-360, -32],
        "BG": [-400, -32],
        "BH": [-0, -64],  # Bahrain
        "BI": [-40, -64],
        "BJ": [-80, -64],
        "BM": [-120, -64],
        "BN": [-160, -64],
        "BO": [-200, -64],
        "BR": [-240, -64],
        "BS": [-280, -64],
        "BT": [-320, -64],
        "BW": [-360, -64],
        "BY": [-400, -64],
        "BZ": [-0, -96],  # Belize
        "CA": [-40, -96],
        "CD": [-80, -96],
        "CF": [-120, -96],
        "CG": [-160, -96],
        "CH": [-200, -96],
        "CI": [-240, -96],
        "CL": [-280, -96],
        "CM": [-320, -96],
        "CN": [-360, -96],
        "CO": [-400, -96],
        "CR": [-0, -128],  # Costa Rica
        "CU": [-40, -128],
        "CV": [-80, -128],
        "CW": [-120, -128],
        "CY": [-160, -128],
        "CZ": [-200, -128],
        "DE": [-240, -128],
        "DJ": [-280, -128],
        "DK": [-320, -128],
        "DM": [-360, -128],
        "DO": [-400, -128],
        "DZ": [-0, -160],  # ALgeria
        "EC": [-40, -160],
        "EE": [-80, -160],
        "EG": [-120, -160],
        "EH": [-160, -160],
        "ER": [-200, -160],
        "ES": [-240, -160],
        "ET": [-280, -160],
        "EU": [-320, -160],
        "FD": [-360, -160],
        "FI": [-400, -160],
        "FJ": [-0, -192],  # Fiji
        "FK": [-40, -192],
        "FM": [-80, -192],
        "FO": [-120, -192],
        "FR": [-160, -192],
        "GA": [-200, -192],
        "XE": [-240, -192],
        "XS": [-280, -192],
        "GB": [-320, -192],
        "XW": [-360, -192],
        "GD": [-400, -192],
        "GE": [-0, -224],  # Georgia
        "GF": [-40, -224],
        "GG": [-80, -224],
        "GH": [-120, -224],
        "GI": [-160, -224],
        "GL": [-200, -224],
        "GM": [-240, -224],
        "GN": [-280, -224],
        "GP": [-320, -224],
        "GQ": [-360, -224],
        "GR": [-400, -224],
        "GS": [-0, -256],  # South Georgia and the South Sandwich Islands
        "GT": [-40, -256],
        "GU": [-80, -256],
        "GW": [-120, -256],
        "GY": [-160, -256],
        "HK": [-200, -256],
        "HN": [-240, -256],
        "HR": [-280, -256],
        "HT": [-320, -256],
        "HU": [-360, -256],
        "ID": [-400, -256],
        "IE": [-0, -288],  # Ireland
        "IL": [-40, -288],
        "IM": [-80, -288],
        "IN": [-120, -288],
        "IQ": [-160, -288],
        "IR": [-200, -288],
        "IS": [-240, -288],
        "IT": [-280, -288],
        "JE": [-320, -288],
        "JM": [-360, -288],
        "JO": [-400, -288],
        "JP": [-0, -320],  # Japan
        "KG": [-40, -320],
        "KH": [-80, -320],
        "KI": [-120, -320],
        "KM": [-160, -320],
        "KE": [-200, -320],
        "KN": [-240, -320],
        "KP": [-280, -320],
        "KR": [-320, -320],
        "KW": [-360, -320],
        "KY": [-400, -320],
        "KZ": [-0, -352],  # Kazakhstan
        "LA": [-40, -352],
        "LB": [-80, -352],
        "LC": [-120, -352],
        "LI": [-160, -352],
        "LK": [-200, -352],
        "LR": [-240, -352],
        "LS": [-280, -352],
        "LT": [-320, -352],
        "LU": [-360, -352],
        "LV": [-400, -352],
        "LY": [-0, -384],  # Libiya
        "MA": [-40, -384],
        "MC": [-80, -384],
        "MD": [-120, -384],
        "ME": [-160, -384],
        "MG": [-200, -384],
        "MH": [-240, -384],
        "MK": [-280, -384],
        "ML": [-320, -384],
        "MM": [-360, -384],
        "MN": [-400, -384],
        "MO": [-0, -416],  # Macao
        "MQ": [-40, -416],
        "MR": [-80, -416],
        "MS": [-120, -416],
        "MT": [-160, -416],
        "MU": [-200, -416],
        "MV": [-240, -416],
        "MW": [-280, -416],
        "MX": [-320, -416],
        "MY": [-360, -416],
        "MZ": [-400, -416],
        "NA": [-0, -448],  # Namibia
        "NC": [-40, -448],
        "NE": [-80, -448],
        "NG": [-120, -448],
        "NI": [-160, -448],
        "NL": [-200, -448],
        "NO": [-240, -448],
        "NP": [-280, -448],
        "NR": [-320, -448],
        "NU": [-360, -448],
        "NZ": [-400, -448],
        "OM": [-0, -480],  # Oman
        "PA": [-40, -480],
        "PE": [-80, -480],
        "PF": [-120, -480],
        "PG": [-160, -480],
        "PH": [-200, -480],
        "PK": [-240, -480],
        "PL": [-280, -480],
        "PM": [-320, -480],
        "PR": [-360, -480],
        "PS": [-400, -480],
        "PT": [-0, -512],  # Portugal
        "PW": [-40, -512],
        "PY": [-80, -512],
        "QA": [-120, -512],
        "RE": [-160, -512],
        "RO": [-200, -512],
        "RS": [-240, -512],
        "RU": [-280, -512],
        "RW": [-320, -512],
        "SA": [-360, -512],
        "SB": [-400, -512],
        "SC": [-0, -544],  # Seychelles
        "SD": [-40, -544],
        "SE": [-80, -544],
        "SG": [-120, -544],
        "SI": [-160, -544],
        "SK": [-200, -544],
        "SL": [-240, -544],
        "SM": [-280, -544],
        "SN": [-320, -544],
        "SO": [-360, -544],
        "SR": [-400, -544],
        "SS": [-0, -576],  # South Sudan
        "ST": [-40, -576],
        "SV": [-80, -576],
        "SX": [-120, -576],
        "SY": [-160, -576],
        "SZ": [-200, -576],
        "TC": [-240, -576],
        "TD": [-280, -576],
        "TG": [-320, -576],
        "TH": [-360, -576],
        "TJ": [-400, -576],
        "TL": [-0, -608],  # Timor-Leste
        "TM": [-40, -608],
        "TN": [-80, -608],
        "TO": [-120, -608],
        "TR": [-160, -608],
        "TT": [-200, -608],
        "TV": [-240, -608],
        "TW": [-280, -608],
        "TZ": [-320, -608],
        "UA": [-360, -608],
        "UG": [-400, -608],
        "US": [-0, -640],  # USA
        "UY": [-40, -640],
        "UZ": [-80, -640],
        "VA": [-120, -640],
        "VC": [-160, -640],
        "VE": [-200, -640],
        "VG": [-240, -640],
        "VI": [-280, -640],
        "VN": [-320, -640],
        "VU": [-360, -640],
        "WS": [-400, -640],
        "XA": [-0, -672],  # Canary islands
        "XB": [-40, -672],
        "XC": [-80, -672],
        "XG": [-120, -672],
        "XK": [-160, -672],
        "XT": [-200, -672],
        "YE": [-240, -672],
        "YT": [-280, -672],
        "ZA": [-320, -672],
        "ZM": [-360, -672],
        "ZW": [-400, -672],
        "XX": [-0, -704],  # Internaltional
        "SANCTIONED": [-40, -704],
        "XO": [-80, -704],
        "XP": [-120, -704],
        "MP": [-160, -704],
    }
    if country_code not in flag_coordinates.keys():
        return ""
    return f"""<svg x="58" y="65" width="32" height="32" viewBox="0 0 32 24" overflow="hidden"> <image href="{url_for("static", filename="assets/flags.png")}" x="{flag_coordinates[country_code][0]}" y="{flag_coordinates[country_code][1]}"></image> </svg>"""


def normalize_stats(stats):
    normalized_stats = copy.deepcopy(STATS_SCHEMA)
    if stats:
        if "last" in stats.keys() and "rating" in stats["last"].keys():
            normalized_stats["last"]["rating"] = stats["last"]["rating"]
        if "best" in stats.keys() and "rating" in stats["best"].keys():
            normalized_stats["best"]["rating"] = stats["best"]["rating"]
        if "record" in stats.keys() and "win" in stats["record"].keys():
            normalized_stats["record"]["win"] = stats["record"]["win"]
        if "record" in stats.keys() and "draw" in stats["record"].keys():
            normalized_stats["record"]["draw"] = stats["record"]["draw"]
        if "record" in stats.keys() and "loss" in stats["record"].keys():
            normalized_stats["record"]["loss"] = stats["record"]["loss"]
    return normalized_stats


def generate_svg(
    profile_url,
    avatar,
    country_code,
    username,
    league,
    joined,
    last_seen,
    rapid_stats,
    blitz_stats,
    bullet_stats,
):
    background_svg = (
        """<rect width="400" height="265" fill="#302e2b" rx="12" ry="12" />"""
    )
    avatar_svg = f"""<a href="{profile_url}" target="_blank"> <image href="{avatar if avatar else url_for("static", filename="assets/no-avatar.png")}" x="11" y="15" width="75" height="75" clip-path="inset(0% round 5px)" /> </a>"""
    flag_svg = generate_flag_svg(country_code=country_code)
    username_svg = f"""<a href="{profile_url}" target="_blank"> <text x="100" y="35" fill="#f9fafb" font-family="Arial, sans-serif" font-size="16" font-weight="bold">{username}</text> </a>"""
    if league:
        league_svg = f"""<image href="{url_for("static", filename=f"assets/{league.lower()}.svg")}" x="100" y="50" width="30" /><text x="135" y="63" fill="#d1d5db" font-family="Arial, sans-serif" font-size="11">{league} league</text>"""
    else:
        league_svg = f"""<text x="100" y="63" fill="#d1d5db" font-family="Arial, sans-serif" font-size="11">No league</text>"""
    joined_svg = f"""<text x="280" y="35" fill="#9ca3af" font-family="Arial, sans-serif" font-size="10">Joined: {joined}</text>"""
    last_seen_svg = f"""<text x="280" y="50" fill="#9ca3af" font-family="Arial, sans-serif" font-size="10">Last seen: {last_seen}</text>"""
    if rapid_stats:
        rapid_section = f"""<rect x="10" y="100" width="120" height="150" fill="#262522" rx="8" ry="8" /> <image href="{url_for("static", filename="assets/time-rapid.svg")}" x="30" y="112" width="25" /> <text x="80" y="130" fill="#ffffff" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle">Rapid</text> <text x="70" y="160" fill="#f9fafb" font-family="Arial, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">{rapid_stats["last"]["rating"]}</text> <text x="70" y="185" fill="#f9fafb" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Highest</text> <text x="70" y="200" fill="#d1d5db" font-family="Arial, sans-serif" font-size="14" text-anchor="middle">{rapid_stats["best"]["rating"]}</text> <text x="70" y="225" font-family="Arial, sans-serif" font-size="11" text-anchor="middle"> <tspan fill="#22c55e">{rapid_stats["record"]["win"]}</tspan> <tspan fill="white">/</tspan> <tspan fill="#6b7280">{rapid_stats["record"]["draw"]}</tspan> <tspan fill="white">/</tspan> <tspan fill="#ef4444">{rapid_stats["record"]["loss"]}</tspan> </text>"""
    if blitz_stats:
        blitz_section = f"""<rect x="140" y="100" width="120" height="150" fill="#262522" rx="8" ry="8" /> <image href="{url_for("static", filename="assets/time-blitz.svg")}" x="165" y="112" width="25" /> <text x="208" y="130" fill="#ffffff" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle">Blitz</text> <text x="200" y="160" fill="#f9fafb" font-family="Arial, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">{blitz_stats["last"]["rating"]}</text> <text x="200" y="185" fill="#f9fafb" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Highest</text> <text x="200" y="200" fill="#d1d5db" font-family="Arial, sans-serif" font-size="14" text-anchor="middle">{blitz_stats["best"]["rating"]}</text> <text x="200" y="225" font-family="Arial, sans-serif" font-size="11" text-anchor="middle"> <tspan fill="#22c55e">{blitz_stats["record"]["win"]}</tspan> <tspan fill="white">/</tspan> <tspan fill="#6b7280">{blitz_stats["record"]["draw"]}</tspan> <tspan fill="white">/</tspan> <tspan fill="#ef4444">{blitz_stats["record"]["loss"]}</tspan> </text>"""
    if bullet_stats:
        bullet_section = f"""<rect x="270" y="100" width="120" height="150" fill="#262522" rx="8" ry="8" /> <image href="{url_for("static", filename="assets/time-bullet.svg")}" x="295" y="115" width="23" /> <text x="340" y="130" fill="#ffffff" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle">Bullet</text> <text x="330" y="160" fill="#f9fafb" font-family="Arial, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">{bullet_stats["last"]["rating"]}</text> <text x="330" y="185" fill="#f9fafb" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Highest</text> <text x="330" y="200" fill="#d1d5db" font-family="Arial, sans-serif" font-size="14" text-anchor="middle">{bullet_stats["best"]["rating"]}</text> <text x="330" y="225" font-family="Arial, sans-serif" font-size="11" text-anchor="middle"> <tspan fill="#22c55e">{bullet_stats["record"]["win"]}</tspan> <tspan fill="white">/</tspan> <tspan fill="#6b7280">{bullet_stats["record"]["draw"]}</tspan> <tspan fill="white">/</tspan> <tspan fill="#ef4444">{bullet_stats["record"]["loss"]}</tspan> </text>"""
    svg = "".join(
        [
            """<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">""",
            background_svg,
            avatar_svg,
            flag_svg,
            username_svg,
            league_svg,
            joined_svg,
            last_seen_svg,
            rapid_section,
            blitz_section,
            bullet_section,
            """</svg>""",
        ]
    )
    return svg


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
