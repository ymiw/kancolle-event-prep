import json
import os
from data import *
from io import BytesIO
from os import path
from PIL import Image, ImageDraw, ImageFont

FONT_SHIP_LEVEL = ImageFont.truetype("verdana.ttf", 28)


def get_marker(ship_level):
    if ship_level < 1:
        return MARKER_DONT_HAVE
    elif ship_level < 26:
        return MARKER_NOT_USABLE
    elif ship_level < 41:
        return MARKER_ALMOST_UNUSABLE
    elif ship_level < 65:
        return MARKER_PROBABLY_USEABLE
    elif ship_level <= 99:
        return MARKER_SUFFICIENT

    return MARKER_MARRIED


def get_portrait_bounds(fleet, position):
    fleet = fleet.lower().strip()

    if fleet not in FLEET_INFO:
        return None

    row = int(position / 5)
    column = position % 5
    pos_x = FLEET_INFO[fleet]["x"]
    pos_y = FLEET_INFO[fleet]["y"]
    offset_x = 0

    # Little hack to get correct positioning
    # TODO: fix this
    if column == 3:
        offset_x += 1
    elif column == 4:
        pos_x += 1

    # Spacing
    pos_x += (column * PORTRAIT_SPACING_HORIZONTAL) + (column * PORTRAIT_WIDTH)
    pos_y += (row * PORTRAIT_SPACING_VERTICAL) + (row * PORTRAIT_HEIGHT)

    return pos_x + 1, pos_y, pos_x + PORTRAIT_WIDTH + 1 + offset_x, pos_y + PORTRAIT_HEIGHT


def get_ship_name(ship_id):
    if not isinstance(ship_id, str):
        ship_id = str(ship_id)

    if ship_id not in SHIP_DB:
        return None
    elif SHIP_DB[ship_id][1]:
        return SHIP_DB[ship_id][1]

    # Some ships don't have romanized equivalent, like Z1/Z3
    return SHIP_DB[ship_id][0]


def parse_profile(profile_contents):
    ship_levels = {}

    try:
        data = json.loads(profile_contents)

        # ships -> masterId maps to whocallsthefleet ship db id
        for key, val in data["ships"].items():
            ship_name = get_ship_name(int(val["masterId"]))

            if not ship_name:
                print("Invalid ship %s!", val["masterId"])
                continue

            ship_level = int(val["level"])

            if ship_name not in ship_levels or ship_levels[ship_name] < ship_level:
                ship_levels[ship_name] = ship_level
    except:
        return "Invalid K3Kai Profile!"

    return ship_levels


def render_profile(profile_contents, file_path=None):
    try:
        data = json.loads(profile_contents)
    except:
        return "Invalid KC3Kai profile!"

    if "ships" not in data:
        return "Ship list is missing; are you sure this is a valid K3Kai profile file?"

    ship_levels = parse_profile(profile_contents)
    image = Image.open(path.join("./static", "images", "base.png"))
    draw = ImageDraw.Draw(image, "RGBA")

    for key, val in FLEET_INFO.items():
        fleet_ships = val["ships"]

        for index in range(0, len(fleet_ships)):
            ship_name = fleet_ships[index].lower().strip()
            ship_level = -1 if ship_name not in ship_levels else ship_levels[ship_name]
            bounds = get_portrait_bounds(key, index)

            if bounds is None:
                continue

            draw.rectangle(bounds, fill=get_marker(ship_level))

            # Only draw ship level if the profile has the ship
            if ship_level > -1:
                draw.text((bounds[0] + 10, bounds[1] + 37), str(ship_level), font=FONT_SHIP_LEVEL, fill=(0, 0, 0, 255))

    if file_path is not None:
        image.save(file_path, "PNG")
        return True
    else:
        output_image = BytesIO()
        image.save(output_image, "PNG")

        # Need to seek back to the start of the stream to output the written contents
        output_image.seek(0)

        return output_image

def main():
    import sys

    if len(sys.argv) < 2:
        print("Invalid syntax; usage: event_prep.py path_to_kc3kai_profile.kc3")
        return

    kc3kai_profile = sys.argv[1]

    if not path.exists(kc3kai_profile):
        print("Profile file doesn't exist!")
        return

    try:
        with open(kc3kai_profile, encoding="utf-8") as reader:
            render_profile(reader.read(), path.join(path.dirname(kc3kai_profile), "event-prep-export.png"))
    except Exception as e:
        print("Exception while executing! " + str(e))


# Why did this get deleted?...
if __name__ == "__main__":
    main()
