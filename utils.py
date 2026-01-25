from constants_and_b64_assets import *
import datetime
import copy
import requests
import base64


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
    if country_code not in FLAG_COORDINATES.keys():
        return ""
    return f"""<svg x="58" y="65" width="32" height="32" viewBox="0 0 32 24" overflow="hidden"> <image href="{FLAGS_PNG_B64}" x="{FLAG_COORDINATES[country_code][0]}" y="{FLAG_COORDINATES[country_code][1]}"></image> </svg>"""


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


def generate_avatar_png_b64(avatar_url):
    avatar_resp = requests.get(avatar_url)
    return f"""data:image/png;base64,{base64.b64encode(avatar_resp.content).decode("utf-8")}"""


def generate_svg(
    profile_url,
    avatar,
    country_code,
    username,
    league,
    title,
    joined,
    last_seen,
    rapid_stats,
    blitz_stats,
    bullet_stats,
):
    background_svg = (
        """<rect width="400" height="265" fill="#302e2b" rx="12" ry="12" />"""
    )
    avatar_svg = f"""<a href="{profile_url}" target="_blank"> <image href="{generate_avatar_png_b64(avatar_url=avatar) if avatar else NO_AVATAR_PNG_B64}" x="11" y="15" width="75" height="75" clip-path="inset(0% round 5px)" /> </a>"""
    flag_svg = generate_flag_svg(country_code=country_code)
    username_svg = f"""<a href="{profile_url}" target="_blank"> <text x="100" y="35" fill="#f9fafb" font-family="Arial, sans-serif" font-size="16" font-weight="bold">{username}</text> </a>"""
    if league:
        league_svg = f"""<image href="{LEAGUES_SVG_B64[league.lower()]}" x="100" y="50" width="30" /><text x="135" y="63" fill="#d1d5db" font-family="Arial, sans-serif" font-size="11">{league} league</text>"""
    else:
        league_svg = f"""<text x="100" y="63" fill="#d1d5db" font-family="Arial, sans-serif" font-size="11">No league</text>"""
    if title:
        title_svg = f"""<image x="280" y="19" height="20" href="{TITLES_SVG_B64[title]}"> </image>"""
        joined_svg_y = 55
        last_seen_svg_y = 70
    else:
        title_svg = ""
        joined_svg_y = 35
        last_seen_svg_y = 50
    joined_svg = f"""<text x="280" y="{joined_svg_y}" fill="#9ca3af" font-family="Arial, sans-serif" font-size="10">Joined: {joined}</text>"""
    last_seen_svg = f"""<text x="280" y="{last_seen_svg_y}" fill="#9ca3af" font-family="Arial, sans-serif" font-size="10">Last seen: {last_seen}</text>"""
    if rapid_stats:
        rapid_section = f"""<rect x="10" y="100" width="120" height="150" fill="#262522" rx="8" ry="8" /> <image href="{TIME_RAPID_SVG_B64}" x="30" y="112" width="25" /> <text x="80" y="130" fill="#ffffff" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle">Rapid</text> <text x="70" y="160" fill="#f9fafb" font-family="Arial, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">{rapid_stats["last"]["rating"]}</text> <text x="70" y="185" fill="#f9fafb" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Highest</text> <text x="70" y="200" fill="#d1d5db" font-family="Arial, sans-serif" font-size="14" text-anchor="middle">{rapid_stats["best"]["rating"]}</text> <text x="70" y="225" font-family="Arial, sans-serif" font-size="11" text-anchor="middle"> <tspan fill="#22c55e">{rapid_stats["record"]["win"]}</tspan> <tspan fill="white">/</tspan> <tspan fill="#6b7280">{rapid_stats["record"]["draw"]}</tspan> <tspan fill="white">/</tspan> <tspan fill="#ef4444">{rapid_stats["record"]["loss"]}</tspan> </text>"""
    if blitz_stats:
        blitz_section = f"""<rect x="140" y="100" width="120" height="150" fill="#262522" rx="8" ry="8" /> <image href="{TIME_BLITZ_SVG_B64}" x="165" y="112" width="25" /> <text x="208" y="130" fill="#ffffff" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle">Blitz</text> <text x="200" y="160" fill="#f9fafb" font-family="Arial, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">{blitz_stats["last"]["rating"]}</text> <text x="200" y="185" fill="#f9fafb" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Highest</text> <text x="200" y="200" fill="#d1d5db" font-family="Arial, sans-serif" font-size="14" text-anchor="middle">{blitz_stats["best"]["rating"]}</text> <text x="200" y="225" font-family="Arial, sans-serif" font-size="11" text-anchor="middle"> <tspan fill="#22c55e">{blitz_stats["record"]["win"]}</tspan> <tspan fill="white">/</tspan> <tspan fill="#6b7280">{blitz_stats["record"]["draw"]}</tspan> <tspan fill="white">/</tspan> <tspan fill="#ef4444">{blitz_stats["record"]["loss"]}</tspan> </text>"""
    if bullet_stats:
        bullet_section = f"""<rect x="270" y="100" width="120" height="150" fill="#262522" rx="8" ry="8" /> <image href="{TIME_BULLET_SVG_B64}" x="295" y="115" width="23" /> <text x="340" y="130" fill="#ffffff" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle">Bullet</text> <text x="330" y="160" fill="#f9fafb" font-family="Arial, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">{bullet_stats["last"]["rating"]}</text> <text x="330" y="185" fill="#f9fafb" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Highest</text> <text x="330" y="200" fill="#d1d5db" font-family="Arial, sans-serif" font-size="14" text-anchor="middle">{bullet_stats["best"]["rating"]}</text> <text x="330" y="225" font-family="Arial, sans-serif" font-size="11" text-anchor="middle"> <tspan fill="#22c55e">{bullet_stats["record"]["win"]}</tspan> <tspan fill="white">/</tspan> <tspan fill="#6b7280">{bullet_stats["record"]["draw"]}</tspan> <tspan fill="white">/</tspan> <tspan fill="#ef4444">{bullet_stats["record"]["loss"]}</tspan> </text>"""
    svg = "".join(
        [
            """<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">""",
            background_svg,
            avatar_svg,
            flag_svg,
            username_svg,
            league_svg,
            title_svg,
            joined_svg,
            last_seen_svg,
            rapid_section,
            blitz_section,
            bullet_section,
            """</svg>""",
        ]
    )
    return svg
