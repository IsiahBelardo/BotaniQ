import os

# pygame is only used as an off-screen drawing library here (no pygame window),
# so the dummy video driver keeps it from ever opening anything.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame
from PIL import Image as PILImage

from ursina import *
from ursina.prefabs.input_field import InputField
from ursina.shaders import unlit_shader

# Imported AFTER the ursina star-import so ursina cannot shadow them.
import math
import random
import re
import types
import json
import threading
import time as _time          # NOT 'time' - ursina owns that name (time.dt)
import urllib.request
from pathlib import Path
from random import uniform


# ============================================================
# LANGUAGE / LOCALIZATION
# ============================================================

LANG = {"code": "en"}

TR = {
    "subtitle": (
        "Crop Recommendation & Growth Simulation",
        "Pagrekomenda ng Pananim at Simulasyon ng Paglaki",
    ),
    "waiting_params": (
        "Waiting for environmental parameters...",
        "Naghihintay ng mga parameter...",
    ),
    "missing_values_bar": (
        "Missing values \u2014 please fill in all fields.",
        "May kulang pang value \u2014 punan muna lahat ng field.",
    ),
    "what_generated": ("WHAT IS BEING GENERATED?", "ANO ANG GINAWA?"),
    "sim_info_default": (
        "Select a crop to watch its growth simulation. Changing the typed values updates it live.",
        "Pumili ng pananim para makita ang simulasyon. Live itong magbabago kapag binago ang mga value.",
    ),
    "sim_hint": (
        "Type your field values, press Recommend, then pick a crop to watch it grow.",
        "Ilagay ang mga value, pindutin ang I-recommend, at pumili ng pananim para makita itong lumago.",
    ),
    "crop_profile_default": (
        "Crop Profile\n\nSelect environmental parameters below\nand click 'Recommend Crops' to view details.",
        "Profile ng Pananim\n\nPunan ang mga parameter sa ibaba\nat pindutin ang 'I-recommend' para makita ang detalye.",
    ),
    "reset": ("Reset", "I-reset"),
    "recommend": ("Recommend", "I-recommend"),
    "missing_values_title": ("Missing Values", "May Kulang na Value"),
    "missing_values_prefix": ("Please input a value for:", "Lagyan muna ng value ang:"),
    "missing_values_fallback": (
        "Please input the values before recommending crops.",
        "Punan muna ang mga value bago mag-recommend ng pananim.",
    ),
    "ok": ("OK", "OK"),
    "suitability": ("Suitability", "Kaangkupan"),
    "moisture": ("Moisture", "Halumigmig"),
    "temp": ("Temp", "Temperatura"),
    "uses": ("Uses", "Gamit"),
    "vigor": ("Vigor", "Sigla"),
    "at_these_values": ("at these values", "sa kasalukuyang value"),
    "height": ("Height", "Taas"),
    "branching": ("Branching", "Pagsanga"),
    "stems": ("stems", "sanga"),
    "leaves": ("Leaves", "Dahon"),
    "leaves_unit": ("leaves", "dahon"),
    "fruit": ("Fruit", "Bunga"),
    "expected": ("expected", "ang inaasahan"),
    # --- simulation strip ---
    "play": ("Play", "Play"),
    "pause": ("Pause", "Pause"),
    "done": ("Done", "Tapos"),
    "sim_restart": ("Restart", "Ulitin"),
    "day": ("Day", "Araw"),
    "growth": ("Growth", "Paglaki"),
    "branches": ("Branches", "Sanga"),
    "stage_seed": ("Seed", "Binhi"),
    "stage_sprout": ("Sprout", "Usbong"),
    "stage_young": ("Young", "Bata"),
    "stage_mature": ("Mature", "Hinog"),
    "dead": ("Dead", "Patay"),
    "now_and_full": ("shown now / at full growth", "ngayon / sa ganap na paglaki"),
    "unbranched": ("none \u2014 single stem", "wala \u2014 iisang tangkay"),
    "leaf_clusters": ("leaf clusters", "kumpol ng dahon"),
    "range_guide": ("Range", "Saklaw"),
    # --- survival / no suitable crop ---
    "no_suitable_bar": (
        "No suitable crop \u2014 these values are too extreme for any crop.",
        "Walang angkop na pananim \u2014 sobrang labis ang mga value para sa kahit anong pananim.",
    ),
    "no_suitable_title": ("No Suitable Crop", "Walang Angkop na Pananim"),
    "no_suitable_body": (
        "None of the crops can survive these conditions.",
        "Walang pananim na makakaligtas sa mga kondisyong ito.",
    ),
    "no_suitable_sim": (
        "No crop can grow under these values, so there is nothing to simulate.\nAdjust the values and press Recommend again.",
        "Walang pananim na tutubo sa mga value na ito kaya walang masisimulate.\nAyusin ang mga value at pindutin ulit ang I-recommend.",
    ),
    "plant_died": ("Plant died", "Namatay ang halaman"),
    "seed_failed": ("Seed failed to sprout", "Hindi tumubo ang binhi"),
    "will_die": ("Will not survive these values", "Hindi makakaligtas sa mga value na ito"),
    "cause": ("Cause", "Dahilan"),
    "not_suitable_tag": ("not suitable", "hindi angkop"),
    "why_generic": ("conditions far outside this crop's range", "labas na labas sa saklaw ng pananim"),
    "why_temp_high": ("temperature too high", "sobrang taas ng temperatura"),
    "why_temp_low": ("temperature too low", "sobrang baba ng temperatura"),
    "why_moisture_high": ("soil too wet", "sobrang basa ng lupa"),
    "why_moisture_low": ("soil too dry", "sobrang tuyo ng lupa"),
    "why_ph_high": ("soil too alkaline (pH too high)", "sobrang alkaline ng lupa (mataas ang pH)"),
    "why_ph_low": ("soil too acidic (pH too low)", "sobrang asim ng lupa (mababa ang pH)"),
    "why_sunlight_high": ("too much sunlight", "sobrang daming sikat ng araw"),
    "why_sunlight_low": ("not enough sunlight", "kulang ang sikat ng araw"),
    "why_nutrients_high": ("too many nutrients (fertilizer burn)", "sobrang dami ng sustansya (nasusunog ang ugat)"),
    "why_nutrients_low": ("not enough nutrients", "kulang ang sustansya"),
    "loading_subtitle": (
        "Crop Recommendation & Growth Simulator",
        "Simulator ng Paglaki at Pagrekomenda ng Pananim",
    ),
    "loading_text": (
        "Preparing interactive botanical simulation...",
        "Inihahanda ang simulation...",
    ),
    "loading_step_1": (
        "Reading soil and climate data...",
        "Binabasa ang datos ng lupa at klima...",
    ),
    "loading_step_2": (
        "Building growth rules...",
        "Binubuo ang mga patakaran ng paglaki...",
    ),
    "loading_step_3": (
        "Growing crop models...",
        "Pinapalago ang mga modelo ng pananim...",
    ),
    "loading_step_4": (
        "Almost ready...",
        "Halos handa na...",
    ),
    "language_select_title": ("Select Language / Pumili ng Wika", "Select Language / Pumili ng Wika"),
    "language_select_subtitle": (
        "Choose your preferred language for the interface.",
        "Piliin ang gusto mong wika para sa interface.",
    ),
    # --- weather (Carmona, Cavite) ---
    "weather_label": ("Carmona, Cavite:", "Carmona, Cavite:"),
    "weather_rainy": ("Rainy Weather", "Tag-ulan"),
    "weather_dry": ("Dry Weather", "Tag-araw"),
    "weather_pick": (
        "Tap a season to load Carmona's real climate averages.",
        "Pumili ng panahon para ilagay ang tunay na klima ng Carmona.",
    ),
    "weather_short_rain": (
        "Jun-Aug average, ~{days} rainy days/month",
        "Karaniwan tuwing Hun-Ago, ~{days} araw ng ulan/buwan",
    ),
    "weather_short_dry": (
        "Feb-Apr average, ~{days} rainy days/month",
        "Karaniwan tuwing Peb-Abr, ~{days} araw ng ulan/buwan",
    ),
    "weather_line": (
        "Weather: {name} (Carmona avg) \u2022 {temp} C, {sun} h sun/day, {rain} mm rain/month, soil ~{moist}%",
        "Panahon: {name} (karaniwan sa Carmona) \u2022 {temp} C, {sun} oras ng araw, {rain} mm ulan/buwan, lupa ~{moist}%",
    ),
    "weather_btn_rain": ("Rainy", "Tag-ulan"),
    "weather_btn_dry": ("Dry", "Tag-araw"),
    "weather_btn_live": ("Live", "Live"),
    "weather_live": ("Live Weather", "Live na Panahon"),
    "weather_live_wait": (
        "Fetching live Carmona weather...",
        "Kinukuha ang live na panahon ng Carmona...",
    ),
    "weather_live_err": (
        "Live weather unavailable (no internet?) - retrying...",
        "Walang live na panahon (walang internet?) - susubukan ulit...",
    ),
    "weather_live_now": (
        "LIVE {time}: {temp} C, {cond} | RH {rh}% | {sun} h sun | soil ~{moist}%",
        "LIVE {time}: {temp} C, {cond} | RH {rh}% | {sun} oras araw | lupa ~{moist}%",
    ),
    "weather_live_stale": (
        "(offline - showing last reading)",
        "(offline - huling datos ang ipinapakita)",
    ),
    "weather_now_hint": (
        "Now in Carmona: {temp} C, {cond} - tap Live to use it",
        "Ngayon sa Carmona: {temp} C, {cond} - pindutin ang Live",
    ),
    "weather_line_live": (
        "Weather: LIVE Carmona {time} \u2022 {cond}, {temp} C, ~{sun} h sun today, soil ~{moist}% (est.), RH {rh}%",
        "Panahon: LIVE Carmona {time} \u2022 {cond}, {temp} C, ~{sun} oras ng araw, lupa ~{moist}% (tantya), RH {rh}%",
    ),
    "language_en": ("English", "English"),
    "language_fil": ("Filipino", "Filipino"),
}


def t(key):
    idx = 0 if LANG["code"] == "en" else 1
    return TR[key][idx]


SECTION_TITLES = {
    "Soil Nutrients": ("Soil Nutrients", "Sustansya ng Lupa"),
    "Soil Properties": ("Soil Properties", "Katangian ng Lupa"),
    "Climate": ("Climate", "Klima"),
    "Land / Space": ("Land / Space", "Lupa / Espasyo"),
}


def section_title(name):
    idx = 0 if LANG["code"] == "en" else 1
    return SECTION_TITLES.get(name, (name, name))[idx]


FIELD_LABELS_TR = {
    "n": ("Nitrogen (N):", "Nitrogen (N):"),
    "p": ("Phosphorus (P):", "Phosphorus (P):"),
    "k": ("Potassium (K):", "Potassium (K):"),
    "ph": ("Soil pH:", "pH ng Lupa:"),
    "moisture": ("Soil Moisture (%):", "Halumigmig ng Lupa (%):"),
    "temp": ("Temperature (C):", "Temperatura (C):"),
    "sunlight": ("Sunlight (hrs/day):", "Sikat ng Araw (oras/araw):"),
    "space": ("Planting Space (m2):", "Espasyo sa Pagtatanim (m2):"),
}


def field_label(key):
    idx = 0 if LANG["code"] == "en" else 1
    return FIELD_LABELS_TR.get(key, (key, key))[idx]


TIER_BRANCH_FIL = {
    "sparse branching": "kaunting sanga",
    "moderate branching": "katamtamang sanga",
    "dense branching": "siksik na sanga",
}
TIER_LEAF_FIL = {
    "sparse foliage": "kaunting dahon",
    "moderate foliage": "katamtamang dahon",
    "lush foliage": "masaganang dahon",
}
FRUIT_LABEL_FIL = {
    "ears": "uhay",
    "fruits": "bunga",
    "gourds": "bunga",
    "pods": "pod",
    "tomatoes": "kamatis",
    "fingers": "saging",
}
CROP_TYPE_FIL = {
    "Cereal Crop": "Butil na Pananim",
    "Fruit Vegetable": "Gulay na Namumunga",
    "Legume Vegetable": "Legumbreng Gulay",
    "Fruit Tree": "Punong Namumunga",
}


def fil_translate(phrase, mapping):
    if LANG["code"] == "en":
        return phrase
    return mapping.get(phrase, phrase)


CROP_SCORE_WEIGHTS = {
    "Green Corn (Sweet Corn)": {"temp": .16, "ph": .09, "moisture": .14, "n": .18, "p": .10, "k": .10, "sunlight": .14, "space": .09},
    "Eggplant (Talong)": {"temp": .15, "ph": .13, "moisture": .15, "n": .12, "p": .08, "k": .10, "sunlight": .17, "space": .10},
    "Tomato (Kamatis)": {"temp": .15, "ph": .13, "moisture": .16, "n": .13, "p": .09, "k": .10, "sunlight": .15, "space": .09},
    "Bitter Gourd (Ampalaya)": {"temp": .15, "ph": .10, "moisture": .16, "n": .10, "p": .10, "k": .10, "sunlight": .15, "space": .14},
    "Okra": {"temp": .16, "ph": .11, "moisture": .14, "n": .13, "p": .08, "k": .10, "sunlight": .17, "space": .11},
    "String Beans (Sitaw)": {"temp": .15, "ph": .10, "moisture": .15, "n": .08, "p": .10, "k": .10, "sunlight": .15, "space": .17},
    "Squash (Kalabasa)": {"temp": .14, "ph": .10, "moisture": .16, "n": .10, "p": .10, "k": .10, "sunlight": .15, "space": .15},
    "Bottle Gourd (Upo)": {"temp": .15, "ph": .10, "moisture": .16, "n": .10, "p": .10, "k": .10, "sunlight": .15, "space": .14},
    "Chili (Siling Panigang/Labuyo)": {"temp": .15, "ph": .13, "moisture": .13, "n": .12, "p": .09, "k": .11, "sunlight": .17, "space": .10},
    "Banana (Saging)": {"temp": .14, "ph": .08, "moisture": .20, "n": .10, "p": .06, "k": .20, "sunlight": .12, "space": .10},
    "Papaya": {"temp": .16, "ph": .13, "moisture": .14, "n": .13, "p": .07, "k": .14, "sunlight": .14, "space": .09},
    "Mango (Mangga)": {"temp": .15, "ph": .10, "moisture": .13, "n": .08, "p": .06, "k": .08, "sunlight": .16, "space": .24},
}


CROPS = {
    "Green Corn (Sweet Corn)": {
        "image": "images/corn.png",
        "ph": (5.8, 7.0),
        "temp": (20, 32),
        "moisture": (55, 75),
        "n": (120, 120),
        "p": (60, 60),
        "k": (40, 40),
        "sunlight": (6, 8),
        "space": 0.22,
        "description": "A staple grain crop characterized by a tall unbranched stalk and long arching leaves.",
        "type": "Cereal Crop",
        "growth": "65-90 days",
        "uses": "Food, animal feed, commercial grain production",
        "stages": ["Sprout (0-12d)", "Stalk Rise (13-40d)", "Tasseling (41-60d)", "Ear Formation (61-90d)"],
    },
    "Eggplant (Talong)": {
        "image": "images/eggplant.png",
        "ph": (5.5, 6.5),
        "temp": (25, 35),
        "moisture": (55, 75),
        "n": (100, 100),
        "p": (50, 50),
        "k": (50, 50),
        "sunlight": (6, 8),
        "space": 0.55,
        "description": "A warm-season fruiting vegetable grown for its glossy purple fruit, needing steady moisture and full sun.",
        "type": "Fruit Vegetable",
        "growth": "80-100 days",
        "uses": "Cooking, food production, home gardening",
        "stages": ["Seedling (0-20d)", "Branching (21-50d)", "Flowering (51-75d)", "Fruit Harvest (76-100d)"],
    },
    "Tomato (Kamatis)": {
        "image": "images/tomato.png",
        "ph": (5.5, 6.8),
        "temp": (22, 32),
        "moisture": (45, 65),
        "n": (120, 120),
        "p": (60, 60),
        "k": (60, 60),
        "sunlight": (6, 8),
        "space": 0.36,
        "description": "A warm-season crop requiring sufficient sunlight and well-drained soil for healthy fruit production.",
        "type": "Fruit Vegetable",
        "growth": "70-90 days",
        "uses": "Food production, cooking, commercial farming",
        "stages": ["Seedling (0-15d)", "Vine Growth (16-45d)", "Blossom (46-65d)", "Ripe Fruit (66-90d)"],
    },
    "Bitter Gourd (Ampalaya)": {
        "image": "images/ampalaya.png",
        "ph": (5.5, 6.7),
        "temp": (22, 32),
        "moisture": (50, 70),
        "n": (90, 90),
        "p": (60, 60),
        "k": (60, 60),
        "sunlight": (6, 8),
        "space": 1.25,
        "description": "A climbing tropical vine grown on a trellis for its bitter fruit, popular in local cuisine.",
        "type": "Fruit Vegetable",
        "growth": "55-65 days",
        "uses": "Soups, stir-fry dishes, vegetable production",
        "stages": ["Sprout (0-12d)", "Vining (13-30d)", "Flowering (31-45d)", "Harvest Ready (46-65d)"],
    },
    "Okra": {
        "image": "images/okra.png",
        "ph": (6.0, 6.8),
        "temp": (22, 32),
        "moisture": (50, 70),
        "n": (80, 80),
        "p": (40, 40),
        "k": (40, 40),
        "sunlight": (6, 8),
        "space": 0.26,
        "description": "A warm-season fruiting vegetable requiring full sun and consistent watering for good pod yield.",
        "type": "Fruit Vegetable",
        "growth": "55-65 days",
        "uses": "Salads, sauces, cooking, commercial farming",
        "stages": ["Seedling (0-15d)", "Stem Expansion (16-35d)", "Budding (36-50d)", "Pod Yield (51-65d)"],
    },
    "String Beans (Sitaw)": {
        "image": "images/sitaw.png",
        "ph": (5.5, 6.5),
        "temp": (22, 32),
        "moisture": (50, 70),
        "n": (60, 60),
        "p": (40, 40),
        "k": (40, 40),
        "sunlight": (6, 8),
        "space": 0.25,
        "description": "A fast-growing tropical legume vine valued for its long edible pods and nitrogen-fixing roots.",
        "type": "Legume Vegetable",
        "growth": "55-65 days",
        "uses": "Cooking, stir-fry, vegetable production",
        "stages": ["Sprout (0-10d)", "Climbing Vine (11-30d)", "Blooms (31-45d)", "Pod Harvest (46-65d)"],
    },
    "Squash (Kalabasa)": {
        "image": "images/squash.png",
        "ph": (5.5, 6.8),
        "temp": (22, 32),
        "moisture": (50, 70),
        "n": (90, 90),
        "p": (60, 60),
        "k": (60, 60),
        "sunlight": (6, 8),
        "space": 2.50,
        "description": "A sprawling vine crop grown for its large fruit, needing plenty of ground space and full sun.",
        "type": "Fruit Vegetable",
        "growth": "90-120 days",
        "uses": "Cooking, food production, commercial farming",
        "stages": ["Seedling (0-20d)", "Ground Spread (21-60d)", "Pollination (61-90d)", "Big Fruit (91-120d)"],
    },
    "Bottle Gourd (Upo)": {
        "image": "images/upo.png",
        "ph": (5.5, 6.5),
        "temp": (24, 32),
        "moisture": (50, 70),
        "n": (80, 80),
        "p": (40, 40),
        "k": (40, 40),
        "sunlight": (6, 8),
        "space": 1.00,
        "description": "A vigorous tropical vine grown on a trellis for its mild-flavored fruit.",
        "type": "Fruit Vegetable",
        "growth": "55-70 days",
        "uses": "Cooking, traditional use, vegetable production",
        "stages": ["Sprout (0-12d)", "Vining (13-35d)", "Flowering (36-50d)", "Gourd Harvest (51-70d)"],
    },
    "Chili (Siling Panigang/Labuyo)": {
        "image": "images/chili.png",
        "ph": (5.5, 6.8),
        "temp": (22, 32),
        "moisture": (50, 70),
        "n": (100, 100),
        "p": (50, 50),
        "k": (50, 50),
        "sunlight": (6, 8),
        "space": 0.36,
        "description": "A compact, high-yielding pepper shrub grown for its spicy fruit.",
        "type": "Fruit Vegetable",
        "growth": "90-120 days",
        "uses": "Cooking, condiments, commercial farming",
        "stages": ["Seedling (0-20d)", "Bush Growth (21-60d)", "White Blossoms (61-90d)", "Red Peppers (91-120d)"],
    },
    "Banana (Saging)": {
        "image": "images/banana.png",
        "ph": (5.5, 7.0),
        "temp": (22, 32),
        "moisture": (70, 90),
        "n": (200, 200),
        "p": (60, 60),
        "k": (200, 200),
        "sunlight": (6, 8),
        "space": 6.25,
        "description": "A fast-growing tropical herbaceous plant needing ample space, water, and potassium-rich soil.",
        "type": "Fruit Tree",
        "growth": "9-12 months to first harvest",
        "uses": "Fresh fruit, food production, commercial farming",
        "stages": ["Sucker (1-2mo)", "Pseudostem (3-6mo)", "Heart/Flower (7-9mo)", "Bunch Ripening (10-12mo)"],
    },
    "Papaya": {
        "image": "images/papaya.png",
        "ph": (6.0, 6.5),
        "temp": (24, 32),
        "moisture": (50, 70),
        "n": (150, 150),
        "p": (50, 50),
        "k": (100, 100),
        "sunlight": (6, 8),
        "space": 6.25,
        "description": "A fast-fruiting tropical tree that bears continuously once mature, needing full sun and good drainage.",
        "type": "Fruit Tree",
        "growth": "6-9 months to first fruit",
        "uses": "Fresh fruit, food production, commercial farming",
        "stages": ["Sapling (1-2mo)", "Trunk Formation (3-4mo)", "Blossoming (5-6mo)", "Fruit Bearing (7-9mo)"],
    },
    "Mango (Mangga)": {
        "image": "images/mango.png",
        "ph": (5.5, 7.5),
        "temp": (24, 35),
        "moisture": (40, 60),
        "n": (500, 500),
        "p": (200, 200),
        "k": (300, 300),
        "sunlight": (6, 8),
        "space": 81.0,
        "description": "A long-lived tropical fruit tree requiring a pronounced dry season and heavy sunlight exposure to flower well.",
        "type": "Fruit Tree",
        "growth": "3-5 years to first fruit",
        "uses": "Fresh fruit, export, commercial production",
        "stages": ["Sapling (Yr 1)", "Canopy Growth (Yr 2)", "Flowering Flush (Yr 3)", "Harvest Yield (Yr 4-5)"],
    },
}

CROP_KEY_MAP = {
    "Green Corn (Sweet Corn)": "corn",
    "Eggplant (Talong)": "egg",
    "Tomato (Kamatis)": "tomato",
    "Bitter Gourd (Ampalaya)": "bitter",
    "Okra": "okra",
    "String Beans (Sitaw)": "beans",
    "Squash (Kalabasa)": "squash",
    "Bottle Gourd (Upo)": "bottle",
    "Chili (Siling Panigang/Labuyo)": "chili",
    "Banana (Saging)": "banana",
    "Papaya": "papaya",
    "Mango (Mangga)": "mango",
}


BOTANICAL_FACTS = {
    "Green Corn (Sweet Corn)": {
        "height": "1.5-2.4 m tall, upright jointed stalk",
        "branching": "Single main stalk, essentially unbranched (may form 1-2 tillers at the base)",
        "leaves": "Long, narrow leaves alternating along the stalk, 50-100 cm long",
        "fruit": "Ears wrapped in husks, topped with silk; kernels in rows",
    },
    "Eggplant (Talong)": {
        "height": "0.6-1.5 m, bushy",
        "branching": "Sturdy, semi-woody, well-branched stems",
        "leaves": "Large, ovate, coarsely lobed, 10-20 cm long, velvety grey-green",
        "fruit": "Glossy purple berry, 12-30 cm long",
    },
    "Tomato (Kamatis)": {
        "height": "0.6-1.8 m, sprawling/trailing when fruiting",
        "branching": "Much-branched, spreading stems",
        "leaves": "Pinnately compound, hairy, up to 45 cm long",
        "fruit": "Round red berries, 4-7 cm diameter, in clusters",
    },
    "Bitter Gourd (Ampalaya)": {
        "height": "Climbing vine, shoots reaching up to 5 m",
        "branching": "Well-branched, slender ridged stems that climb via thin tendrils",
        "leaves": "Palmate, 5-10 cm across, 5-7 toothed lobes",
        "fruit": "Warty, ribbed oblong pods, 15-25 cm, green ripening to orange",
    },
    "Okra": {
        "height": "1.2-2.1 m tall",
        "branching": "Central main stem with minimal lateral branching (topping encourages bushier growth)",
        "leaves": "Large, heart-shaped, deeply lobed, up to 20 cm across",
        "fruit": "Ribbed, conical pod capsule, 7-25 cm long, held upright",
    },
    "String Beans (Sitaw)": {
        "height": "Climbing vine, 2-4 m on a trellis",
        "branching": "Vigorous twining stems that wrap around supports",
        "leaves": "Trifoliate (three leaflets per leaf)",
        "fruit": "Very long, slender pods, 30-75 cm",
    },
    "Squash (Kalabasa)": {
        "height": "Sprawling/climbing vine, 3-4 m Long",
        "branching": "Coarse, trailing, tendril-bearing vine",
        "leaves": "Large, rounded, heart-shaped base, 15-30 cm, shallowly 5-lobed",
        "fruit": "Large fleshy fruit, variable shape, several kilograms, yellow pulp",
    },
    "Bottle Gourd (Upo)": {
        "height": "Vigorous climbing vine, 3-16 m long",
        "branching": "Thick, furrowed stems with branched tendrils",
        "leaves": "Large, heart-shaped, soft-haired, up to 30 cm across",
        "fruit": "Elongated bottle- or club-shaped fruit, up to 1 m long",
    },
    "Chili (Siling Panigang/Labuyo)": {
        "height": "0.3-1.5 m, compact shrub",
        "branching": "Bushy with many branching stems",
        "leaves": "Smooth, ovate, pointed tip, about 6 cm long",
        "fruit": "Small tapering pods, 1-3 cm, pointing upward, very hot",
    },
    "Banana (Saging)": {
        "height": "2-9 m pseudostem (formed from tightly rolled leaf sheaths, not true wood)",
        "branching": "No true branches \u2014 a single unbranched pseudostem topped by a crown of leaves",
        "leaves": "Huge paddle-shaped leaves, up to 2-3 m long",
        "fruit": "Hanging bunch of fingers, can weigh 50 kg or more per bunch",
    },
    "Papaya": {
        "height": "2-9 m, single trunk",
        "branching": "Unbranched (occasional side shoots only after damage or topping)",
        "leaves": "Palmate, deeply lobed, up to 1 m wide, clustered at the crown",
        "fruit": "Large oblong berries growing directly on the trunk, up to 70 cm and several kg",
    },
    "Mango (Mangga)": {
        "height": "10-30 m at maturity (commonly kept 3-10 m when pruned/cultivated)",
        "branching": "Broad, dense, dome-shaped branching canopy, 10-35 m spread",
        "leaves": "Leathery, lance-shaped leaves, 15-30 cm long",
        "fruit": "Fleshy drupe, oval to kidney-shaped, 300 g-2 kg",
    },
}


CROP_STRUCTURE_RANGES = {
    "Green Corn (Sweet Corn)": {"branches": (1, 2), "leaves": (8, 14), "fruit": (1, 2), "fruit_label": "ears"},
    "Eggplant (Talong)": {"branches": (3, 9), "leaves": (25, 70), "fruit": (4, 14), "fruit_label": "fruits"},
    "Tomato (Kamatis)": {"branches": (4, 12), "leaves": (30, 90), "fruit": (15, 60), "fruit_label": "tomatoes"},
    "Bitter Gourd (Ampalaya)": {"branches": (5, 16), "leaves": (40, 110), "fruit": (6, 20), "fruit_label": "gourds"},
    "Okra": {"branches": (1, 3), "leaves": (15, 32), "fruit": (10, 28), "fruit_label": "pods"},
    "String Beans (Sitaw)": {"branches": (6, 18), "leaves": (50, 140), "fruit": (15, 40), "fruit_label": "pods"},
    "Squash (Kalabasa)": {"branches": (3, 9), "leaves": (20, 55), "fruit": (2, 6), "fruit_label": "fruits"},
    "Bottle Gourd (Upo)": {"branches": (3, 8), "leaves": (20, 50), "fruit": (3, 10), "fruit_label": "gourds"},
    "Chili (Siling Panigang/Labuyo)": {"branches": (6, 18), "leaves": (40, 110), "fruit": (20, 70), "fruit_label": "pods"},
    "Banana (Saging)": {"branches": (0, 1), "leaves": (8, 14), "fruit": (30, 180), "fruit_label": "fingers"},
    "Papaya": {"branches": (0, 2), "leaves": (15, 28), "fruit": (10, 35), "fruit_label": "fruits"},
    "Mango (Mangga)": {"branches": (15, 55), "leaves": (200, 700), "fruit": (50, 250), "fruit_label": "fruits"},
}

_DEFAULT_STRUCTURE_RANGE = {"branches": (2, 10), "leaves": (15, 60), "fruit": (2, 15), "fruit_label": "fruits"}


def _parse_measurement_range(text, fallback=(0.5, 1.5)):
    if not text:
        return fallback
    match = re.search(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", text)
    if match:
        return float(match.group(1)), float(match.group(2))
    single = re.search(r"(\d+(?:\.\d+)?)", text)
    if single:
        value = float(single.group(1))
        return value * 0.5, value
    return fallback


MAX_RECOMMENDATIONS = 5


def _fmt_guide(x):
    return f"{x:g}"


def _build_guide_ranges():
    guide = {}
    for key in ("n", "p", "k", "ph", "moisture", "temp", "sunlight", "space"):
        lows, highs = [], []
        for crop in CROPS.values():
            v = crop[key]
            lo, hi = (v[0], v[1]) if isinstance(v, (tuple, list)) else (v, v)
            lows.append(lo)
            highs.append(hi)
        guide[key] = (min(lows), max(highs))
    return guide


GUIDE_RANGES = _build_guide_ranges()


def field_guide(key):
    lo, hi = GUIDE_Ranges[key] if 'GUIDE_Ranges' in globals() else GUIDE_RANGES[key]
    return f"{t('range_guide')}: {_fmt_guide(lo)}\u2013{_fmt_guide(hi)}"


def _optimal_factor(value, low, high, floor=0.20):
    if low <= value <= high:
        return 1.0
    span = (high - low) * 0.75
    if span <= 1e-6:
        mid = (low + high) / 2.0
        span = max(abs(mid) * 0.35, 8.0)
    distance = (low - value) if value < low else (value - high)
    return max(floor, 1.0 - distance / span)


def get_growth_response(crop_name, values):
    crop = CROPS[crop_name]

    temp = _optimal_factor(values["temp"], *crop["temp"])
    moisture = _optimal_factor(values["moisture"], *crop["moisture"])
    ph = _optimal_factor(values["ph"], *crop["ph"])
    sunlight = _optimal_factor(values["sunlight"], *crop["sunlight"])

    nf = _optimal_factor(values["n"], *crop["n"])
    pf = _optimal_factor(values["p"], *crop["p"])
    kf = _optimal_factor(values["k"], *crop["k"])
    nutrients = (nf + pf + kf) / 3.0

    required_space = max(crop["space"], 0.01)
    space = max(0.25, min(1.0, values["space"] / required_space))

    height_factor = 0.45 + 0.55 * (0.32 * temp + 0.26 * sunlight + 0.22 * moisture + 0.20 * ph)
    branch_factor = 0.30 + 0.70 * (0.55 * nutrients + 0.25 * moisture + 0.20 * temp)
    leaf_factor = 0.30 + 0.70 * (0.42 * sunlight + 0.35 * nutrients + 0.23 * moisture)
    lateral_factor = 0.35 + 0.65 * space
    health = (temp + moisture + ph + sunlight + nutrients + space) / 6.0

    return {
        "temperature": temp,
        "moisture": moisture,
        "ph": ph,
        "sunlight": sunlight,
        "nutrients": nutrients,
        "space": space,
        "height_factor": height_factor,
        "branch_factor": branch_factor,
        "leaf_factor": leaf_factor,
        "lateral_factor": lateral_factor,
        "health": health,
    }


def describe_plant_growth(crop_name, values):
    facts = BOTANICAL_FACTS.get(crop_name, {})
    struct = CROP_STRUCTURE_RANGES.get(crop_name, _DEFAULT_STRUCTURE_RANGE)
    g = get_growth_response(crop_name, values)

    h_low, h_high = _parse_measurement_range(facts.get("height", ""))
    height_m = h_low + (h_high - h_low) * g["height_factor"]

    b_low, b_high = struct["branches"]
    branch_count = int(round(b_low + (b_high - b_low) * g["branch_factor"]))

    l_low, l_high = struct["leaves"]
    leaf_count = int(round(l_low + (l_high - l_low) * g["leaf_factor"]))

    f_low, f_high = struct["fruit"]
    fruit_factor = max(0.0, min(1.0, (g["nutrients"] + g["health"]) / 2.0))
    fruit_count = int(round(f_low + (f_high - f_low) * fruit_factor))

    def _tier(value, low, high, labels):
        span = max(high - low, 1e-6)
        pos = (value - low) / span
        if pos <= 0.33:
            return labels[0]
        if pos <= 0.66:
            return labels[1]
        return labels[2]

    branch_desc = _tier(branch_count, b_low, b_high, ("sparse branching", "moderate branching", "dense branching"))
    leaf_desc = _tier(leaf_count, l_low, l_high, ("sparse foliage", "moderate foliage", "lush foliage"))

    return {
        "height_m": height_m,
        "branch_count": branch_count,
        "branch_desc": branch_desc,
        "leaf_count": leaf_count,
        "leaf_desc": leaf_desc,
        "fruit_count": fruit_count,
        "fruit_label": struct.get("fruit_label", "fruits"),
        "vigor_pct": int(round(max(0.0, min(1.0, g["health"])) * 100)),
    }


def calculate_suitability_score(crop_name, values):
    crop = CROPS[crop_name]
    weights = CROP_SCORE_WEIGHTS[crop_name]
    factors = {
        "temp": _optimal_factor(values["temp"], *crop["temp"]),
        "ph": _optimal_factor(values["ph"], *crop["ph"]),
        "moisture": _optimal_factor(values["moisture"], *crop["moisture"]),
        "n": _optimal_factor(values["n"], *crop["n"]),
        "p": _optimal_factor(values["p"], *crop["p"]),
        "k": _optimal_factor(values["k"], *crop["k"]),
        "sunlight": _optimal_factor(values["sunlight"], *crop["sunlight"]),
    }
    required_space = max(crop["space"], 0.01)
    factors["space"] = max(0.20, min(1.0, values["space"] / required_space))
    score = 1.0
    for key, weight in weights.items():
        score *= max(0.0001, factors[key]) ** weight
    return max(0.0, min(100.0, score * 100.0))


NOT_SUITABLE_SCORE = 30.0
LETHAL_RAW = -0.25
MIN_LIGHT_HOURS = 2.0


def _raw_factor(value, low, high):
    if low <= value <= high:
        return 1.0
    span = (high - low) * 0.75
    if span <= 1e-6:
        mid = (low + high) / 2.0
        span = max(abs(mid) * 0.35, 8.0)
    distance = (low - value) if value < low else (value - high)
    return 1.0 - distance / span


def assess_viability(crop_name, values):
    crop = CROPS[crop_name]
    score = calculate_suitability_score(crop_name, values)
    raw = {k: _raw_factor(values[k], *crop[k]) for k in ("temp", "moisture", "ph", "sunlight", "n", "p", "k")}

    def side(key):
        return "low" if values[key] < crop[key][0] else "high"

    lethal, off = [], []
    for key in ("temp", "moisture", "ph"):
        if raw[key] <= LETHAL_RAW:
            lethal.append((key, side(key)))
        if raw[key] <= 0.2:
            off.append((key, side(key)))
    if values["sunlight"] < MIN_LIGHT_HOURS:
        lethal.append(("sunlight", "low"))
    if raw["sunlight"] <= 0.2:
        off.append(("sunlight", side("sunlight")))

    burn = sum(1 for k in ("n", "p", "k") if values[k] > crop[k][1] and raw[k] <= LETHAL_RAW)
    if burn >= 2:
        lethal.append(("nutrients", "high"))
    n_high = sum(1 for k in ("n", "p", "k") if values[k] > crop[k][1] and raw[k] <= 0.2)
    n_low = sum(1 for k in ("n", "p", "k") if values[k] < crop[k][0] and raw[k] <= 0.2)
    if n_high >= 2:
        off.append(("nutrients", "high"))
    elif n_low >= 2:
        off.append(("nutrients", "low"))

    viable = not lethal and score >= NOT_SUITABLE_SCORE
    reasons = []
    for r in lethal + off:
        if r not in reasons:
            reasons.append(r)

    if viable:
        die_g = 2.0
    elif len(lethal) >= 2 or score < 24.0:
        die_g = 0.08
    else:
        die_g = 0.08 + 0.30 * max(0.0, min(1.0, (score - 20.0) / 25.0))
    return {"viable": viable, "score": score, "reasons": reasons, "die_g": die_g}


def recommend_crops(values):
    scored = []
    for crop in CROPS:
        if assess_viability(crop, values)["viable"]:
            scored.append((crop, calculate_suitability_score(crop, values)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:MAX_RECOMMENDATIONS]


# >>> PYGAME-SIM-BEGIN
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def sm(x):
    x = clamp(x)
    return x * x * (3.0 - 2.0 * x)


def mixc(a, b, t_):
    t_ = clamp(t_)
    return [int(round(a[i] + (b[i] - a[i]) * t_)) for i in range(3)]


def deg_to_rad(s, a):
    angle_deg = -a if s > 0 else -(180.0 - a)
    return angle_deg * math.pi / 180.0


CROP_DATA = {
    'corn':   {'dur': 80,   'hmax': 0.9,  'cm': 210, 'wob': 0.2, 'hel': 0},
    'tomato': {'dur': 85,   'hmax': 0.62, 'cm': 120, 'wob': 1.2, 'hel': 0},
    'egg':    {'dur': 95,   'hmax': 0.58, 'cm': 90,  'wob': 0.6, 'hel': 0},
    'bitter': {'dur': 60,   'hmax': 0.92, 'cm': 250, 'wob': 0,   'hel': 9},
    'okra':   {'dur': 60,   'hmax': 0.72, 'cm': 150, 'wob': 0.3, 'hel': 0},
    'banana': {'dur': 120,  'hmax': 0.5,  'cm': 350, 'wob': 0,   'hel': 0},
    'beans':  {'dur': 60,   'hmax': 0.92, 'cm': 240, 'wob': 0,   'hel': 7},
    'squash': {'dur': 105,  'hmax': 0.28, 'cm': 40,  'wob': 0.3, 'hel': 0},
    'bottle': {'dur': 62,   'hmax': 0.92, 'cm': 300, 'wob': 0,   'hel': 8},
    'chili':  {'dur': 105,  'hmax': 0.5,  'cm': 70,  'wob': 0.8, 'hel': 0},
    'papaya': {'dur': 270,  'dps': 9,  'hmax': 0.62, 'cm': 300, 'wob': 0.2, 'hel': 0},
    'mango':  {'dur': 1095, 'dps': 40, 'hmax': 0.62, 'cm': 900, 'wob': 0.4, 'hel': 0},
}

def _parse_growth_days(text, fallback):
    """'65-90 days' -> (65, 90); '9-12 months ...' -> (270, 360); '3-5 years ...' -> (1095, 1825)."""
    nums = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text or "")]
    if not nums:
        return fallback
    low = nums[0]
    high = nums[1] if len(nums) > 1 else nums[0]
    low_text = (text or "").lower()
    unit = 365.0 if "year" in low_text else (30.0 if "month" in low_text else 1.0)
    return (low * unit, high * unit)


REAL_DAYS = {}
for _cname, _ckey in CROP_KEY_MAP.items():
    _dur = CROP_DATA[_ckey]['dur']
    REAL_DAYS[_ckey] = _parse_growth_days(CROPS.get(_cname, {}).get("growth"), (_dur, _dur))


# Carmona, Cavite monthly climate averages (WeatherAPI.com history, 2009-2021):
#   Rainy season Jun/Jul/Aug : avg temp 28/28/27 C, sunshine 115/72/68 h per month,
#                              rainfall 265.5/400.3/317.2 mm, 18/23/22 rain days
#   Dry season  Feb/Mar/Apr  : avg temp 26/27/29 C, sunshine 184/237/260 h per month,
#                              rainfall 25.5/18.7/34.1 mm, 2/3/3 rain days
# temp/sunlight/rain are the 3-month means (sunshine converted to hours per day).
# Soil moisture is NOT a measured value: it is an estimate from rainfall vs. evaporation
# (rainfall far above evaporation in the rainy season, far below it in the dry season).
WEATHER_PROFILES = {
    "rain": {"temp": 27.7, "sunlight": 2.8, "moisture": 85, "rain_mm": 328, "rain_days": 21},
    "dry":  {"temp": 27.3, "sunlight": 7.6, "moisture": 38, "rain_mm": 26,  "rain_days": 3},
    "live": {"temp": 28.0, "sunlight": 6.0, "moisture": 60, "rain_mm": 0,   "rain_days": 0},  # replaced by live data
}
WEATHER = {"mode": None}

# ============================================================
# LIVE WEATHER - Carmona, Cavite (Open-Meteo, free, no API key)
# ============================================================
CARMONA_LAT, CARMONA_LON = 14.3136, 121.0575
LIVE_URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={CARMONA_LAT}&longitude={CARMONA_LON}"
    "&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,cloud_cover,is_day"
    "&hourly=soil_moisture_0_to_7cm"
    "&daily=sunshine_duration,precipitation_sum"
    "&timezone=Asia%2FManila&forecast_days=1"
)
LIVE_REFRESH_S = 600       # auto-refresh every 10 minutes
LIVE_RETRY_S = 45          # retry interval while offline / no data yet
LIVE_MIN_MANUAL_S = 20     # don't hammer the API when the Live button is spammed
LIVE_SOIL_SATURATION = 0.45  # m3/m3 treated as 100% on the app's moisture scale
LIVE = {"data": None, "status": "idle", "stamp": 0, "pending": None, "last_try": -1e9, "thread": None}

# WMO weather codes -> (English, Filipino)
_WMO = {
    0: ("Clear", "Maaliwalas"), 1: ("Mostly clear", "Halos maaliwalas"),
    2: ("Partly cloudy", "Bahagyang maulap"), 3: ("Overcast", "Maulap"),
    45: ("Fog", "Mahamog"), 48: ("Fog", "Mahamog"),
    51: ("Light drizzle", "Mahinang ambon"), 53: ("Drizzle", "Ambon"), 55: ("Heavy drizzle", "Malakas na ambon"),
    56: ("Freezing drizzle", "Ambon"), 57: ("Freezing drizzle", "Ambon"),
    61: ("Light rain", "Mahinang ulan"), 63: ("Rain", "Ulan"), 65: ("Heavy rain", "Malakas na ulan"),
    66: ("Freezing rain", "Ulan"), 67: ("Freezing rain", "Ulan"),
    80: ("Rain showers", "Pag-ulan"), 81: ("Rain showers", "Pag-ulan"), 82: ("Violent showers", "Malakas na buhos"),
    95: ("Thunderstorm", "Kulog at kidlat"), 96: ("Thunderstorm", "Kulog at kidlat"), 99: ("Thunderstorm", "Kulog at kidlat"),
}
_RAIN_CODES = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99}


def _wmo_name(code):
    en, fil = _WMO.get(int(code), ("Unknown", "Hindi tiyak"))
    return en if LANG["code"] == "en" else fil


def _parse_live(raw):
    """Turn an Open-Meteo response into the numbers the app needs."""
    cur = raw["current"]
    temp = float(cur["temperature_2m"])
    rh = float(cur.get("relative_humidity_2m") or 0.0)
    precip = float(cur.get("precipitation") or 0.0)
    code = int(cur.get("weather_code") or 0)
    cloud = float(cur.get("cloud_cover") or 0.0)
    is_day = int(cur.get("is_day", 1))
    tstr = str(cur.get("time", ""))

    soil = None
    hourly = raw.get("hourly") or {}
    times = hourly.get("time") or []
    vals = hourly.get("soil_moisture_0_to_7cm") or []
    hour_key = tstr[:13]
    for i, tm in enumerate(times):
        if str(tm)[:13] == hour_key and i < len(vals) and vals[i] is not None:
            soil = float(vals[i])
            break

    daily = raw.get("daily") or {}
    ds = daily.get("sunshine_duration") or []
    sun_h = (float(ds[0]) / 3600.0) if ds and ds[0] is not None else None
    ps = daily.get("precipitation_sum") or []
    rain_day = float(ps[0]) if ps and ps[0] is not None else precip

    if sun_h is None:
        sun_h = max(0.0, 12.0 * (1.0 - cloud / 100.0))
    # Soil moisture: measured by the model (volumetric) -> mapped onto the app's 0-100 scale.
    # If missing, estimate from humidity + current rain.
    if soil is not None:
        moist = clamp(soil / LIVE_SOIL_SATURATION, 0.0, 1.0) * 100.0
    else:
        moist = clamp(25.0 + 0.45 * rh + 12.0 * min(precip, 3.0), 0.0, 100.0)

    raining = precip >= 0.1 or code in _RAIN_CODES
    if raining:
        visual = "rain"
    elif is_day and cloud < 35 and rh < 70:
        visual = "dry"
    else:
        visual = None

    return {
        "temp": round(temp, 1), "sunlight": round(min(sun_h, 14.0), 1), "moisture": int(round(moist)),
        "rain_mm": round(rain_day, 1), "rh": int(round(rh)), "cloud": int(round(cloud)),
        "code": code, "raining": raining, "visual": visual,
        "time": tstr[11:16] if len(tstr) >= 16 else "",
    }


def _live_worker():
    try:
        req = urllib.request.Request(LIVE_URL, headers={"User-Agent": "BotaniQ/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
        LIVE["pending"] = _parse_live(raw)
    except Exception as e:
        LIVE["pending"] = {"error": str(e)}


def _live_busy():
    th = LIVE["thread"]
    return th is not None and th.is_alive()


def _live_start_fetch():
    if _live_busy():
        return
    LIVE["last_try"] = _time.time()
    if LIVE["data"] is None:
        LIVE["status"] = "fetching"
        LIVE["stamp"] += 1
    th = threading.Thread(target=_live_worker, daemon=True)
    LIVE["thread"] = th
    th.start()


def _live_request_refresh():
    if _time.time() - LIVE["last_try"] >= LIVE_MIN_MANUAL_S:
        _live_start_fetch()


def _live_fill_fields():
    p = WEATHER_PROFILES["live"]
    for key in ("temp", "moisture", "sunlight"):
        input_fields[key].text = f"{p[key]:g}"


def _live_tick():
    """Called every frame from update(): applies finished fetches, schedules refreshes."""
    pend = LIVE["pending"]
    if pend is not None:
        LIVE["pending"] = None
        LIVE["stamp"] += 1
        if "error" in pend:
            LIVE["status"] = "error" if LIVE["data"] is None else "stale"
        else:
            LIVE["data"] = pend
            LIVE["status"] = "ok"
            WEATHER_PROFILES["live"] = {
                "temp": pend["temp"], "sunlight": pend["sunlight"], "moisture": pend["moisture"],
                "rain_mm": pend["rain_mm"], "rain_days": 0,
            }
            if WEATHER["mode"] == "live" and input_fields:
                _live_fill_fields()
                SIM.set_weather(pend["visual"])
                _refresh_after_weather()
    if _live_busy():
        return
    interval = LIVE_REFRESH_S if LIVE["status"] == "ok" else LIVE_RETRY_S
    if _time.time() - LIVE["last_try"] >= interval:
        _live_start_fetch()


SPROUT = {
    'corn':   {'leaves': [(1, 86, 60, 2.1, 0.17), (-1, 84, 46, 1.5, 0.15)], 'shape': (0.40, 1.00), 'col': (150, 205, 95),
               'size': 1.0, 'node': 0.04, 'seed': ((232, 200, 84), 5.0, 3.8), 'stem': (192, 226, 132), 'th0': 0.28, 'hook': 0.0, 'mound': 0.7},
    'tomato': {'leaves': [(1, 74, 10, 1.30, 0.26), (-1, 74, 10, 1.30, 0.26)], 'shape': (0.50, 0.60), 'col': (128, 190, 104),
               'size': 1.0, 'node': 0.12, 'seed': ((226, 206, 150), 3.0, 2.2), 'stem': (166, 206, 124), 'th0': 0.20, 'hook': 0.6, 'mound': 0.8},
    'egg':    {'leaves': [(1, 70, 18, 1.00, 0.46), (-1, 70, 18, 1.00, 0.46)], 'shape': (0.45, 0.50), 'col': (140, 196, 100),
               'size': 1.0, 'node': 0.12, 'seed': ((214, 190, 120), 3.2, 2.5), 'stem': (170, 186, 128), 'th0': 0.22, 'hook': 0.6, 'mound': 0.8},
    'bitter': {'leaves': [(1, 64, 6, 1.15, 0.50), (-1, 64, 6, 1.15, 0.50)], 'shape': (0.50, 0.42), 'col': (112, 182, 88),
               'size': 1.1, 'node': 0.10, 'seed': ((150, 112, 72), 6.0, 3.4), 'stem': (172, 216, 132), 'th0': 0.16, 'hook': 0.8, 'mound': 1.0},
    'okra':   {'leaves': [(1, 76, 24, 0.95, 0.54), (-1, 76, 24, 0.95, 0.54)], 'shape': (0.34, 0.50), 'col': (134, 190, 92),
               'size': 1.0, 'node': 0.12, 'seed': ((112, 102, 62), 3.6, 3.4), 'stem': (172, 206, 122), 'th0': 0.22, 'hook': 0.6, 'mound': 0.8},
    'banana': {'leaves': [(1, 92, 74, 2.9, 0.11), (-1, 84, 58, 1.7, 0.10)], 'shape': (0.35, 1.00), 'col': (160, 208, 104),
               'size': 1.0, 'node': 0.03, 'seed': ((204, 178, 132), 6.5, 5.0), 'stem': (190, 220, 140), 'th0': 0.20, 'hook': 0.0, 'mound': 1.1},
    'beans':  {'leaves': [(1, 60, 18, 1.15, 0.56), (-1, 60, 18, 1.15, 0.56)], 'shape': (0.50, 0.38), 'col': (150, 192, 100),
               'size': 1.0, 'node': 0.07, 'seed': ((172, 92, 62), 5.6, 3.2), 'stem': (200, 208, 148), 'th0': 0.34, 'hook': 0.95, 'mound': 1.0},
    'squash': {'leaves': [(1, 58, 4, 1.35, 0.54), (-1, 58, 4, 1.35, 0.54)], 'shape': (0.50, 0.42), 'col': (124, 190, 86),
               'size': 1.15, 'node': 0.06, 'seed': ((236, 226, 192), 6.6, 3.6), 'stem': (186, 216, 142), 'th0': 0.40, 'hook': 0.95, 'mound': 1.2},
    'bottle': {'leaves': [(1, 64, 10, 1.35, 0.42), (-1, 64, 10, 1.35, 0.42)], 'shape': (0.55, 0.50), 'col': (140, 196, 96),
               'size': 1.05, 'node': 0.10, 'seed': ((206, 186, 142), 6.0, 3.0), 'stem': (180, 216, 136), 'th0': 0.20, 'hook': 0.8, 'mound': 1.0},
    'chili':  {'leaves': [(1, 70, 20, 0.85, 0.20), (-1, 70, 20, 0.85, 0.20)], 'shape': (0.50, 0.70), 'col': (140, 202, 102),
               'size': 0.85, 'node': 0.10, 'seed': ((236, 216, 142), 3.0, 2.3), 'stem': (166, 206, 126), 'th0': 0.18, 'hook': 0.6, 'mound': 0.7},
    'papaya': {'leaves': [(1, 78, 36, 1.45, 0.20), (-1, 78, 36, 1.45, 0.20)], 'shape': (0.45, 0.90), 'col': (152, 202, 112),
               'size': 1.0, 'node': 0.10, 'seed': ((38, 32, 32), 3.2, 3.2), 'stem': (210, 168, 140), 'th0': 0.25, 'hook': 0.4, 'mound': 0.9},
    'mango':  {'leaves': [(1, 68, 28, 1.75, 0.20), (-1, 62, 20, 1.60, 0.19), (1, 84, 52, 1.3, 0.17)], 'shape': (0.42, 0.90), 'col': (178, 92, 62),
               'col_to': (104, 168, 72), 'size': 1.1, 'node': 0.20, 'life': (0.50, 0.20), 'seed': ((192, 172, 122), 8.0, 5.4),
               'stem': (176, 150, 112), 'th0': 0.30, 'hook': 0.25, 'mound': 1.3},
}
SPROUT_DEFAULT = {'leaves': [(1, 78, 16, 1.0, 0.5), (-1, 78, 16, 1.0, 0.5)], 'shape': (0.5, 0.65), 'col': (150, 205, 95),
                  'size': 1.0, 'node': 0.13, 'seed': ((198, 162, 102), 4.5, 3.0), 'stem': (176, 214, 128),
                  'th0': 0.18, 'hook': 0.7, 'mound': 1.0}

EARLY_STAGE_RATE = 0.7
DEATH_TIME = 3.5
DEAD_STEM = (104, 78, 46)
DEAD_LEAF = (112, 84, 46)
DEAD_RIB = (150, 118, 68)


class SimulationEngine:
    def __init__(self):
        self.crop_key = None
        self.crop_name = ""
        self.g = 0.0
        self.day = 0.0
        self.real_total = 0.0
        self.moist = 60.0
        self.moist_t = 60.0
        self.weather = None
        self.rain = self.dry = 0.0
        self.rain_t = self.dry_t = 0.0
        self.play = True
        self.speed = 1.0
        self.vs = 1.0
        self.target = 1.0
        self.tb = self.tl = self.tf = 1.0
        self.fb = self.fl = self.ff = 1.0
        self._clear_fate()

    def _clear_fate(self):
        self.viable = True
        self.die_g = 2.0
        self.reasons = []
        self.dead_t = 0.0

    @property
    def status(self):
        if self.dead_t >= 1.0:
            return "dead"
        if self.dead_t > 0.0:
            return "dying"
        if not self.viable:
            return "failing"
        return "ok"

    def _update_real_days(self):
        """Real-world day count = growth progress x real days this crop needs.
        Healthy conditions -> shorter end of the real range; poor -> longer end."""
        if self.crop_key is None:
            self.day = 0.0
            self.real_total = 0.0
            return
        d = CROP_DATA[self.crop_key]['dur']
        lo, hi = REAL_DAYS.get(self.crop_key, (d, d))
        self.real_total = hi - (hi - lo) * clamp(self.vs)
        self.day = self.g * self.real_total

    def clear(self):
        self.crop_key = None
        self.crop_name = ""
        self.g = 0.0
        self.day = 0.0
        self.real_total = 0.0
        self.play = True
        self._clear_fate()

    def reset(self):
        self.g = 0.0
        self.play = True
        self.dead_t = 0.0
        self._update_real_days()

    def set_environment(self, values):
        if self.crop_name:
            self.moist_t = float(values.get("moisture", 60.0))
            gr = get_growth_response(self.crop_name, values)
            self.target = clamp(gr["health"])
            self.tb = clamp((gr["branch_factor"] - 0.30) / 0.70)
            self.tl = clamp((gr["leaf_factor"] - 0.30) / 0.70)
            self.tf = clamp(((gr["nutrients"] + gr["health"]) / 2.0 - 0.20) / 0.80)
            a = assess_viability(self.crop_name, values)
            self.viable, self.die_g, self.reasons = a["viable"], a["die_g"], a["reasons"]

    def set_crop_and_environment(self, crop_name, values):
        key = CROP_KEY_MAP.get(crop_name)
        if key is None:
            self.clear()
            return
        self.crop_key = key
        self.crop_name = crop_name
        self.reset()
        self.set_environment(values)
        self.vs = self.target
        self.moist = self.moist_t
        self.fb, self.fl, self.ff = self.tb, self.tl, self.tf
        self._update_real_days()

    def set_weather(self, mode):
        self.weather = mode
        self.rain_t = 1.0 if mode == "rain" else 0.0
        self.dry_t = 1.0 if mode == "dry" else 0.0

    def toggle_play(self):
        if self.crop_key is not None and self.g < 1.0 and self.dead_t == 0.0:
            self.play = not self.play

    def update(self, dt):
        wk = min(1.0, dt * 1.5)
        self.rain += (self.rain_t - self.rain) * wk
        self.dry += (self.dry_t - self.dry) * wk
        if self.crop_key is None:
            return
        self.vs += (self.target - self.vs) * min(1.0, dt * 3.0)
        ek = min(1.0, dt * 3.0)
        self.moist += (self.moist_t - self.moist) * min(1.0, dt * 2.0)
        self.fb += (self.tb - self.fb) * ek
        self.fl += (self.tl - self.fl) * ek
        self.ff += (self.tf - self.ff) * ek
        if self.dead_t > 0.0:
            self.dead_t = min(1.0, self.dead_t + dt / DEATH_TIME)
            return
        c = CROP_DATA[self.crop_key]
        prev = self.g
        if self.play and self.g < 1.0:
            dd = dt * c.get('dps', 5.0) * self.speed
            early = EARLY_STAGE_RATE if self.g < 0.22 else 1.0
            self.g = min(1.0, self.g + (dd / c['dur']) * (0.3 + 0.7 * self.target) * early)
            if self.g >= 1.0:
                self.play = False
        if not self.viable and self.g >= self.die_g:
            self.g = max(prev, min(self.g, self.die_g))
            self.dead_t = 1e-4
            self.play = False
        self._update_real_days()


class GraphicsEngine:
    def __init__(self, surface, dots=None, k=1.0):
        self.surface = surface
        self.k = float(k)
        self.soil_col = (106, 74, 48)
        self._cache = {}
        self.dots = dots if dots is not None else [
            [random.random(), random.random(), random.random() * 2.2 + 0.6, random.random()] for _ in range(160)
        ]
        self.cnt = {'leaf': 0, 'br': 0, 'fr': 0}
        self.gy = 0
        self.cx = 0
        self.A = 0
        self.HF = 0
        self.sg = 0
        self.g = 0
        self.vs = 0
        self.LD = (0, 0, 0)
        self.LL = (0, 0, 0)
        self.sw = 0
        self.WOB = 0
        self.HEL = 0
        self.lg = 0
        self.th = 1.0
        self.hook = 0.0
        self.st = 0.0
        self.young = (176, 214, 128)
        self.yg = 0.0
        self.dead = 0.0
        self.fb = self.fl = self.ff = 1.0

    def _slots(self, lo, hi, f):
        return max(lo, min(hi, int(lo + (hi - lo) * clamp(f) + 0.5)))

    def _pq(self, q):
        x = self.cx + self.WOB * math.sin(q * 5.0 + 1.0) * self.HF * 0.025 + self.HEL * math.sin(q * 18.0) + self.sw * q * q * self.HF * 0.02
        if self.hook > 0.001:
            x += self.hook * self.HF * self.sg * min(1.0, q / max(self.sg, 1e-3)) ** 2
        y = self.gy - self.HF * q
        return (x, y)

    def _w(self, n):
        return max(1, int(round(n * self.k)))

    def _dc(self, color):
        if self.dead <= 0.0:
            return color
        return mixc(color, DEAD_STEM, self.dead * 0.9)

    def _seg(self, a, b, w, color):
        pygame.draw.line(self.surface, self._dc(color), a, b, int(max(1, round(w * self.k))))

    def _stem(self, w0, w1, color):
        a = self._pq(0)
        col = mixc(color, self.young, self.yg * 0.85)
        for i in range(1, 29):
            q = self.sg * i / 28.0
            b = self._pq(q)
            self._seg(a, b, max(1.8, (w0 + (w1 - w0) * q) * self.th), col)
            a = b

    def _leaf(self, x, y, ang, length, width, k, nc=False):
        if k <= 0.02 or length < 2:
            return
        length *= k
        width *= k
        if not nc:
            self.cnt['leaf'] += 1

        pts = []
        steps = 12
        for i in range(steps + 1):
            u = i / steps
            lx = 3*(1-u)**2*u*(length*0.25) + 3*(1-u)*u**2*(length*0.75) + u**3*length
            ly = 3*(1-u)**2*u*(-width) + 3*(1-u)*u**2*(-width*0.7)
            pts.append((lx, ly))
        for i in range(steps, -1, -1):
            u = i / steps
            lx = 3*(1-u)**2*u*(length*0.25) + 3*(1-u)*u**2*(length*0.75) + u**3*length
            ly = 3*(1-u)**2*u*(width) + 3*(1-u)*u**2*(width*0.7)
            pts.append((lx, ly))

        cos_a, sin_a = math.cos(ang), math.sin(ang)
        transformed = []
        for lx, ly in pts:
            transformed.append((lx * cos_a - ly * sin_a + x, lx * sin_a + ly * cos_a + y))

        if len(transformed) > 2:
            pygame.draw.polygon(self.surface, self.LD, transformed)

        ex = length * 0.9 * cos_a + x
        ey = length * 0.9 * sin_a + y
        pygame.draw.line(self.surface, self.LL, (x, y), (ex, ey), self._w(1))

    def _arch(self, x, y, s, length, width, k, up, dr):
        if k <= 0.02:
            return
        length *= k
        width *= k
        self.cnt['leaf'] += 1
        T, B = [], []
        steps = 14
        for i in range(steps + 1):
            u = i / float(steps)
            px = x + s * length * u
            py = y - length * (up * u - dr * u * u)
            w = width * math.pow(max(0.0, math.sin(math.pi * min(1.0, u * 0.98 + 0.02))), 0.7) * (1.0 - 0.35 * u) / 2.0
            T.append((px, py - w))
            B.append((px, py + w))

        poly = T + list(reversed(B))
        if len(poly) > 2:
            pygame.draw.polygon(self.surface, self.LD, poly)

        mid_pts = []
        for i in range(len(T)):
            b_pt = B[len(B) - 1 - i]
            mid_pts.append(((T[i][0] + b_pt[0]) / 2.0, (T[i][1] + b_pt[1]) / 2.0))
        if len(mid_pts) > 1:
            pygame.draw.lines(self.surface, self.LL, False, mid_pts, self._w(1))

    def _lobed(self, x, y, s, sz):
        if sz < 3:
            return
        self.cnt['leaf'] += 1
        b = -60.0 if s > 0 else -120.0
        for a in [-70, -35, 0, 35, 70]:
            ang = (b + a) * math.pi / 180.0
            l_sz = sz * (0.8 if a != 0 else 1.0)
            self._leaf(x, y, ang, l_sz, sz * 0.4, 1.0, nc=True)

    def _comp(self, x, y, s, Ln, a=None):
        if a is None:
            a = -50.0 if s > 0 else -130.0
        rad = a * math.pi / 180.0
        if Ln < 4:
            return
        ex = x + math.cos(rad) * Ln
        ey = y + math.sin(rad) * Ln
        self._seg((x, y), (ex, ey), 2, (111, 162, 74))
        for j in range(1, 4):
            u = j / 4.0
            px = x + math.cos(rad) * Ln * u
            py = y + math.sin(rad) * Ln * u
            self._leaf(px, py, rad - 1.1, Ln * 0.38, Ln * 0.2, 1.0)
            self._leaf(px, py, rad + 1.1, Ln * 0.38, Ln * 0.2, 1.0)
        self._leaf(ex, ey, rad, Ln * 0.4, Ln * 0.22, 1.0)

    def _flower(self, x, y, r, col, c2):
        if r < 1.5:
            return
        col, c2 = self._dc(col), self._dc(c2)
        for i in range(5):
            a = i * 1.2566
            px = x + math.cos(a) * r * 0.9
            py = y + math.sin(a) * r * 0.9
            pygame.draw.circle(self.surface, col, (int(px), int(py)), int(r * 0.6))
        pygame.draw.circle(self.surface, c2, (int(x), int(y)), int(r * 0.45))

    def _fruit(self, x, y, rx, ry, rot, col):
        self.cnt['fr'] += 1
        col = self._dc(col)
        rx, ry = max(1, int(rx)), max(1, int(ry))
        surf = pygame.Surface((rx * 2 + 4, ry * 2 + 4), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, col, (2, 2, rx * 2, ry * 2))

        hl = pygame.Surface((rx * 2 + 4, ry * 2 + 4), pygame.SRCALPHA)
        pygame.draw.ellipse(hl, (255, 255, 255, 56), (int(2 + rx*0.1), int(2 + ry*0.2), max(1, int(rx*0.5)), max(1, int(ry*0.6))))
        surf.blit(hl, (0, 0))

        if rot != 0:
            surf = pygame.transform.rotate(surf, math.degrees(-rot))
        rect = surf.get_rect(center=(int(x), int(y)))
        self.surface.blit(surf, rect)

    def _pod(self, x, y, length, rot):
        if length < 3:
            return
        self.cnt['fr'] += 1
        pts = [(0, 0), (5, -length*0.3), (4, -length*0.8), (0, -length), (-4, -length*0.8), (-5, -length*0.3)]
        cos_r, sin_r = math.cos(rot), math.sin(rot)
        t_pts = []
        for px, py in pts:
            t_pts.append((px * cos_r - py * sin_r + x, px * sin_r + py * cos_r + y))
        pygame.draw.polygon(self.surface, self._dc((95, 154, 60)), t_pts)

    def _tendril(self, x, y, s):
        pts = []
        a = 0.0
        while a < 8.0:
            r = 7.0 - a * 0.7
            px = x + s * (a * 2.0 + math.cos(a) * r)
            py = y - 6.0 + math.sin(a) * r
            pts.append((px, py))
            a += 0.3
        if len(pts) > 1:
            pygame.draw.lines(self.surface, self._dc((143, 181, 96)), False, pts, self._w(1))

    def _pole(self, h):
        self._seg((self.cx, self.gy), (self.cx, self.gy - h), 4, (150, 130, 95))

    def _trellis(self):
        tw = self.A * 0.2
        top = self.gy - self.A * 0.95
        lines = [
            [(self.cx - tw, self.gy), (self.cx - tw, top)],
            [(self.cx + tw, self.gy), (self.cx + tw, top)],
            [(self.cx - tw, top), (self.cx + tw, top)],
            [(self.cx - tw, self.gy - self.A * 0.5), (self.cx + tw, self.gy - self.A * 0.5)],
            [(self.cx - tw, self.gy - self.A * 0.72), (self.cx + tw, self.gy - self.A * 0.72)]
        ]
        for a, b in lines:
            self._seg(a, b, 3, (150, 130, 95))

    def _draw_seed(self, key):
        g = self.g
        if g > 0.30:
            return
        sp = SPROUT.get(key, SPROUT_DEFAULT)
        scol, srx, sry = sp['seed']
        scol = mixc(scol, (58, 44, 34), self.dead)
        fade = 1.0 - sm((g - 0.18) / 0.12)
        swell = 1.0 + 0.45 * sm(g / 0.06)
        rx, ry = srx * swell * fade * self.k, sry * swell * fade * self.k
        if rx >= 1.0:
            sx, sy = self.cx, self.gy + (6 + sry) * self.k
            box = (int(sx - rx), int(sy - ry), max(2, int(rx * 2)), max(2, int(ry * 2)))
            pygame.draw.ellipse(self.surface, scol, box)
            pygame.draw.ellipse(self.surface, mixc(scol, (60, 40, 20), 0.45), box, self._w(1))
            if g > 0.045:
                pygame.draw.line(self.surface, mixc(scol, (40, 25, 10), 0.6), (int(sx - rx * 0.6), int(sy)), (int(sx + rx * 0.6), int(sy - ry * 0.5)), self._w(1))

        m = sp['mound']
        mh = 5.0 * m * self.k * sm((g - 0.035) / 0.035) * (1.0 - sm((g - 0.085) / 0.05)) * (1.0 - self.dead)
        if mh > 0.6:
            hw = 9.0 * m * self.k
            pts = [(self.cx + hw * (i / 3.0 - 1.0), self.gy - 1 - mh * (1.0 - (i / 3.0 - 1.0) ** 2)) for i in range(7)]
            pygame.draw.polygon(self.surface, self.soil_col, [(self.cx - hw, self.gy)] + pts + [(self.cx + hw, self.gy)])

    def _cotyledon(self, x, y, s, length, width, up_deg, col, rib, peak=0.5, pw=0.65):
        if length < 1.5:
            return
        ang = deg_to_rad(s, up_deg)
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        n = 12
        warp = math.log(0.5) / math.log(clamp(peak, 0.1, 0.9))
        top = []
        for i in range(n + 1):
            u = (i / float(n)) ** warp
            hw = width * math.pow(max(0.0, math.sin(math.pi * min(1.0, u * 0.96 + 0.04))), pw)
            top.append((length * (i / float(n)), -hw))
        bot = [(lx, -ly) for lx, ly in top]
        poly = [(lx * cos_a - ly * sin_a + x, lx * sin_a + ly * cos_a + y) for lx, ly in top + bot[::-1]]
        pygame.draw.polygon(self.surface, col, poly)
        pygame.draw.line(self.surface, rib, (x, y), (length * 0.9 * cos_a + x, length * 0.9 * sin_a + y), self._w(1))

    def _draw_cotyledons(self, key):
        sp = SPROUT.get(key, SPROUT_DEFAULT)
        g = self.g
        life0, life_len = sp.get('life', (0.34, 0.22))
        k = sm((g - 0.085) / 0.12) * (1.0 - sm((g - life0) / life_len))
        if k < 0.04 or self.sg <= 0.004:
            return
        x, y = self._pq(min(self.sg, sp['node']))
        opened = sm((g - 0.10) / 0.12)
        withered = sm((g - life0) / life_len)
        base = sp['col']
        if 'col_to' in sp:
            base = mixc(base, sp['col_to'], sm((g - 0.18) / 0.25))
        col = mixc(mixc(base, [176, 160, 80], self.st), [196, 172, 96], withered)
        col = mixc(col, DEAD_LEAF, self.dead)
        rib = mixc(col, [90, 140, 60], 0.5)
        size = self.A * 0.06 * sp['size'] * k
        peak, pw = sp['shape']
        for side, u0, u1, lm, wm in sp['leaves']:
            self._cotyledon(x, y, side, size * lm, size * wm, u0 + (u1 - u0) * opened, col, rib, peak, pw)

    def _draw_corn(self):
        self._stem(12, 6, (120, 168, 69))
        n = self._slots(6, 11, self.fl)
        for i in range(n):
            q = 0.1 + i * 0.74 / max(1, n - 1)
            p = self._pq(q)
            self._arch(p[0], p[1], 1 if i % 2 else -1, self.A * 0.27 * (1.1 - 0.5 * q) * (0.6 + 0.4 * self.vs), self.A * 0.032, clamp((self.lg - q) / 0.22), 0.5, 0.55)
        if self.g > 0.55:
            kt = sm((self.g - 0.55) / 0.2)
            p = self._pq(self.sg)
            for j in range(-2, 3):
                pts = [p, (p[0] + j * 6 * kt, p[1] - self.A * 0.05 * kt), (p[0] + j * 13 * kt, p[1] - self.A * 0.08 * kt + abs(j) * 4)]
                pygame.draw.lines(self.surface, (216, 199, 122), False, pts, self._w(2))
        if self.g > 0.68:
            ke = sm((self.g - 0.68) / 0.25)
            y_val = sm((self.g - 0.85) / 0.15)
            for j in range(self._slots(1, 2, self.ff)):
                p = self._pq(0.42 + j * 0.14)
                sd = -1 if j else 1
                col = mixc([120, 170, 70], [236, 200, 70], y_val)
                self._fruit(p[0] + sd * 6, p[1], self.A * 0.013 * ke + 3, self.A * 0.045 * ke, sd * 0.35, col)

    def _draw_tomato(self):
        self._stem(7, 3, (111, 162, 74))
        nb = self._slots(3, 6, self.fb)
        fn = self._slots(2, 5, self.ff)
        for i in range(nb):
            q = 0.2 + i * 0.13
            p = self._pq(q)
            k = clamp((self.lg - q) / 0.22)
            s = 1 if i % 2 else -1
            if k < 0.02:
                continue
            bx = p[0] + s * self.A * 0.14 * k * (0.6 + 0.4 * self.vs)
            by = p[1] - self.A * 0.05 * k
            self._seg(p, (bx, by), 3, (111, 162, 74))
            self.cnt['br'] += 1
            self._comp(bx, by, s, self.A * 0.12 * k * (0.6 + 0.4 * self.vs))
            if 1 <= i <= fn:
                kf = sm((self.g - 0.5) / 0.12) * (1.0 - sm((self.g - 0.64) / 0.08))
                if kf > 0.05:
                    self._flower(bx - s * 5, by + 4, 5 * kf, (244, 208, 63), (224, 168, 0))
                kr = sm((self.g - 0.62) / 0.3)
                if kr > 0.05:
                    R = self.A * 0.028 * (0.7 + 0.3 * self.vs) * kr + 2
                    col = mixc([92, 160, 62], [214, 52, 40], sm((self.g - 0.72) / 0.25))
                    self._seg((bx - s * 6, by + 2), (bx - s * 6, by + 8), 2, (93, 143, 58))
                    self._fruit(bx - s * 6, by + 8 + R, R, R * 0.92, 0, col)
                    if self.ff > 0.5:
                        self._fruit(bx - s * 6 + s * R * 1.7, by + 10 + R * 1.3, R * 0.85, R * 0.8, 0, col)
        t_ = self._pq(self.sg)
        self._comp(t_[0], t_[1], 1, self.A * 0.1 * clamp(self.lg * 2), -90)

    def _draw_eggplant(self):
        self._stem(10, 5, (111, 143, 69))
        nb = self._slots(3, 5, self.fb)
        fn = self._slots(2, 4, self.ff)
        for i in range(nb):
            q = 0.22 + i * 0.13
            p = self._pq(q)
            k = clamp((self.lg - q) / 0.22)
            s = 1 if i % 2 else -1
            if k < 0.02:
                continue
            bx = p[0] + s * self.A * 0.12 * k
            by = p[1] - self.A * 0.04 * k
            self._seg(p, (bx, by), 4, (111, 143, 69))
            self.cnt['br'] += 1
            self._leaf(bx, by, deg_to_rad(s, 35), self.A * 0.16 * k * (0.6 + 0.4 * self.vs), self.A * 0.1 * k, 1)
            if 1 <= i <= fn:
                kf = sm((self.g - 0.5) / 0.12) * (1.0 - sm((self.g - 0.64) / 0.08))
                if kf > 0.05:
                    self._flower(bx - s * 8, by + 5, 6 * kf, (169, 138, 216), (242, 212, 80))
                kr = sm((self.g - 0.62) / 0.3)
                if kr > 0.05:
                    ry = self.A * 0.065 * kr + 2
                    rx = self.A * 0.024 * kr + 1.5
                    self._fruit(bx - s * 5, by + 6 + ry, rx, ry, 0, (86, 38, 120))
        t_ = self._pq(self.sg)
        self._leaf(t_[0], t_[1], deg_to_rad(1, 60), self.A * 0.14 * clamp(self.lg * 2), self.A * 0.09, 1)
        self._leaf(t_[0], t_[1], deg_to_rad(-1, 60), self.A * 0.14 * clamp(self.lg * 2), self.A * 0.09, 1)

    def _draw_bitter(self):
        self._trellis()
        self._stem(4, 2.5, (108, 154, 64))
        for i in range(self._slots(6, 11, self.fl)):
            q = 0.08 + i * 0.075
            p = self._pq(q)
            k = clamp((self.lg - q) / 0.2)
            s = 1 if i % 2 else -1
            if k < 0.02:
                continue
            self._seg(p, (p[0] + s * 8, p[1] - 6), 1.5, (108, 154, 64))
            self._lobed(p[0] + s * 8, p[1] - 6, s, self.A * 0.075 * k * (0.6 + 0.4 * self.vs))
            if i % 3 == 1:
                self._tendril(p[0] - s * 3, p[1], -s)
        for b in (0.5, 0.72)[:self._slots(1, 2, self.fb)]:
            if self.sg > b:
                self.cnt['br'] += 1
        for j, q in enumerate([0.4, 0.58, 0.76][:self._slots(1, 3, self.ff)]):
            p = self._pq(q)
            s = -1 if j % 2 else 1
            kf = sm((self.g - 0.5) / 0.12) * (1.0 - sm((self.g - 0.66) / 0.08))
            if kf > 0.05:
                self._flower(p[0] + s * 16, p[1] - 2, 5 * kf, (246, 211, 48), (201, 138, 0))
            kr = sm((self.g - 0.66 - j * 0.02) / 0.3)
            if kr > 0.05:
                ry = self.A * 0.085 * kr + 2
                x = p[0] + s * 14
                self._seg((x, p[1] - 4), (x, p[1] + 2), 1.5, (108, 154, 64))
                self._fruit(x, p[1] + 2 + ry, self.A * 0.016 * kr + 1.5, ry, 0, (106, 168, 79))

    def _draw_okra(self):
        self._stem(11, 6, (122, 156, 74))
        for i in range(self._slots(4, 7, self.fl)):
            q = 0.14 + i * 0.1
            p = self._pq(q)
            k = clamp((self.lg - q) / 0.22)
            s = 1 if i % 2 else -1
            if k < 0.02:
                continue
            bx = p[0] + s * self.A * 0.06 * k
            by = p[1] - self.A * 0.03 * k
            self._seg(p, (bx, by), 2.5, (122, 156, 74))
            self._lobed(bx, by, s, self.A * 0.13 * k * (0.6 + 0.4 * self.vs))
        for j, q in enumerate([0.62, 0.74, 0.86][:self._slots(1, 3, self.ff)]):
            p = self._pq(q)
            s = -1 if j % 2 else 1
            kf = sm((self.g - 0.5) / 0.12) * (1.0 - sm((self.g - 0.64) / 0.08))
            if kf > 0.05:
                self._flower(p[0] + s * 9, p[1], 7 * kf, (247, 236, 176), (138, 28, 43))
            kr = sm((self.g - 0.62 - j * 0.03) / 0.3)
            if kr > 0.05:
                self._pod(p[0] + s * 7, p[1], self.A * 0.11 * kr, s * 0.2)

    def _draw_banana(self):
        top = self._pq(self.sg)
        w0, w1 = self.A * 0.055 * self.th, self.A * 0.035 * self.th
        poly = [(self.cx - w0, self.gy), (top[0] - w1, top[1]), (top[0] + w1, top[1]), (self.cx + w0, self.gy)]
        pygame.draw.polygon(self.surface, self._dc((163, 184, 106)), poly)
        for i in range(self._slots(5, 8, self.fl)):
            k = clamp((self.g - 0.1 - i * 0.06) / 0.22) * clamp(self.lg * 3.0)
            s = 1 if i % 2 else -1
            self._arch(top[0], top[1], s, self.A * 0.38 * (0.6 + 0.4 * self.vs) * (1.0 - 0.04 * i), self.A * 0.075, k, 0.95 - (i >> 1) * 0.18, 0.7 + (i >> 1) * 0.22)
        if self.g > 0.76:
            kb = sm((self.g - 0.76) / 0.12)
            kf = sm((self.g - 0.86) / 0.14)
            ex, ey = top[0] + self.A * 0.04, top[1] + self.A * 0.12 * kb
            if kf > 0.05:
                for h in range(self._slots(1, 2, self.ff)):
                    for f in range(5):
                        col = mixc([150, 190, 70], [238, 206, 70], sm((self.g - 0.9) / 0.1))
                        self._fruit(ex + (f - 2) * self.A * 0.013 * kf - h * 3, ey + h * self.A * 0.04 * kf + self.A * 0.015 * kf + abs(f - 2) * 2, self.A * 0.007 * kf + 1, self.A * 0.026 * kf + 1, (f - 2) * 0.12, col)

    def _draw_beans(self):
        self._pole(self.A * 0.95)
        self._stem(3, 2, (108, 154, 64))
        fk = sm((self.g - 0.5) / 0.12) * (1.0 - sm((self.g - 0.64) / 0.08))
        fn = self._slots(2, 5, self.ff)
        nbr = self._slots(1, 2, self.fb)
        for i in range(self._slots(6, 10, self.fl)):
            q = 0.1 + i * 0.08
            p = self._pq(q)
            k = clamp((self.lg - q) / 0.2)
            s = 1 if i % 2 else -1
            if k < 0.02:
                continue
            bx, by = p[0] + s * 10, p[1] - 5
            z = self.A * 0.045 * k * (0.6 + 0.4 * self.vs)
            self._seg(p, (bx, by), 1.4, (108, 154, 64))
            self._leaf(bx, by, deg_to_rad(s, 50), z * 1.4, z * 0.9, 1.0)
            self._leaf(bx, by, deg_to_rad(s, 5), z * 1.2, z * 0.8, 1.0, True)
            self._leaf(bx, by, deg_to_rad(s, 95), z * 1.2, z * 0.8, 1.0, True)
            if i in (4, 6)[:nbr]:
                self.cnt['br'] += 1
            if 4 <= i < 4 + fn and fk > 0.05:
                self._flower(p[0] + s * 14, p[1], 4 * fk, (230, 216, 245), (183, 154, 214))
            kr = sm((self.g - 0.62 - (i - 4) * 0.015) / 0.3)
            if 4 <= i < 4 + fn and kr > 0.05:
                ry = self.A * 0.09 * kr + 2
                self._fruit(p[0] + s * 16, p[1] + ry, self.A * 0.006 * kr + 1, ry, s * 0.06, (125, 179, 90))

    def _draw_squash(self):
        self._stem(8, 5, (111, 154, 69))
        y0 = self.gy - 3
        for s in [-1, 1][:self._slots(1, 2, self.fb)]:
            if self.lg < 0.12:
                continue
            length = self.A * 0.55 * clamp((self.lg - 0.12) / 0.88)
            pts = [(self.cx + s * length * (i / 24.0), y0 - math.sin((i / 24.0) * 7.0) * 4.0 * (i / 24.0)) for i in range(25)]
            pygame.draw.lines(self.surface, self._dc((108, 154, 64)), False, pts, self._w(3))
            self.cnt['br'] += 1
            for j, u in enumerate([0.25, 0.5, 0.75, 0.95][:self._slots(2, 4, self.fl)]):
                k = clamp((self.lg - 0.1 - u * 0.6) / 0.2)
                if k < 0.02:
                    continue
                ex = self.cx + s * length * u + s * 6
                ey = y0 - math.sin(u * 7.0) * 4.0 * u - self.A * 0.1 * k * (0.8 if j % 2 else 1.0)
                self._lobed(ex, ey, s, self.A * 0.13 * k * (0.6 + 0.4 * self.vs))
            kf = sm((self.g - 0.5) / 0.12) * (1.0 - sm((self.g - 0.66) / 0.08))
            if kf > 0.05:
                self._flower(self.cx + s * length * 0.6, y0 - self.A * 0.1, 8 * kf, (245, 163, 26), (199, 106, 0))
            for j, u in enumerate([0.4, 0.7][:self._slots(1, 2, self.ff)]):
                kr = sm((self.g - 0.62 - j * 0.04) / 0.3)
                if kr >= 0.05:
                    R = self.A * 0.07 * kr + 3
                    col = mixc([90, 140, 70], [226, 140, 40], sm((self.g - 0.78) / 0.2))
                    self._fruit(self.cx + s * length * u, y0 - R * 0.9, R * 1.15, R, 0, col)

    def _draw_bottle(self):
        self._trellis()
        self._stem(5, 3, (108, 154, 64))
        top = self.gy - self.A * 0.95
        fk = sm((self.g - 0.5) / 0.12) * (1.0 - sm((self.g - 0.66) / 0.08))
        for i in range(self._slots(5, 9, self.fl)):
            q = 0.08 + i * 0.09
            p = self._pq(q)
            k = clamp((self.lg - q) / 0.2)
            s = 1 if i % 2 else -1
            if k < 0.02:
                continue
            bx, by = p[0] + s * 9, p[1] - 6
            z = self.A * 0.1 * k * (0.6 + 0.4 * self.vs)
            self._seg(p, (bx, by), 1.8, (108, 154, 64))
            self._leaf(bx, by, deg_to_rad(s, 40), z, z * 0.85, 1.0)
            if i % 3 == 1:
                self._tendril(p[0] - s * 3, p[1], -s)
            if i % 3 == 2 and fk > 0.05:
                self._flower(p[0] + s * 16, p[1] - 2, 5 * fk, (255, 255, 255), (233, 224, 160))
        kr = sm((self.g - 0.64) / 0.32)
        if kr > 0.05:
            for n, j in enumerate([0, -1, 1][:self._slots(1, 3, self.ff)]):
                x = self.cx + j * self.A * 0.13
                R = self.A * 0.045 * kr + 2
                nk = self.A * 0.05 * kr + 2
                y = top + 8
                self._fruit(x, y + nk * 0.5, R * 0.42, nk * 0.7, 0, (156, 194, 110))

    def _draw_chili(self):
        self._stem(5, 2.5, (122, 156, 74))
        fn = self._slots(2, 6, self.ff)
        for i in range(self._slots(4, 8, self.fb)):
            q = 0.16 + i * 0.1
            p = self._pq(q)
            k = clamp((self.lg - q) / 0.2)
            s = 1 if i % 2 else -1
            if k < 0.02:
                continue
            bx = p[0] + s * self.A * 0.1 * k * (0.6 + 0.4 * self.vs)
            by = p[1] - self.A * 0.06 * k
            z = self.A * 0.05 * (0.6 + 0.4 * self.vs) * k
            self._seg(p, (bx, by), 2.5, (122, 156, 74))
            self.cnt['br'] += 1
            self._leaf(bx, by, deg_to_rad(s, 70), z * 1.6, z * 0.7, 1.0)
            self._leaf(bx, by, deg_to_rad(s, 20), z * 1.4, z * 0.6, 1.0)
            if 2 <= i < 2 + fn:
                kf = sm((self.g - 0.5) / 0.12) * (1.0 - sm((self.g - 0.64) / 0.1))
                if kf > 0.05:
                    self._flower(bx - s * 3, by + 3, 3.5 * kf, (255, 255, 255), (232, 224, 160))
                kr = sm((self.g - 0.62) / 0.3)
                if kr > 0.05:
                    ry = self.A * 0.04 * kr + 1.5
                    col = mixc([84, 150, 56], [210, 36, 34], sm((self.g - 0.76) / 0.22))
                    self._fruit(bx - s * 4, by + 4 + ry, self.A * 0.008 * kr + 1, ry, s * 0.1, col)

    def _draw_papaya(self):
        top = self._pq(self.sg)
        m = 0.6 + 0.4 * self.vs
        pw = self.th
        poly = [(self.cx - self.A * 0.03 * pw, self.gy), (top[0] - self.A * 0.02 * pw, top[1]), (top[0] + self.A * 0.02 * pw, top[1]), (self.cx + self.A * 0.03 * pw, self.gy)]
        pygame.draw.polygon(self.surface, self._dc((155, 176, 122)), poly)
        for i in range(self._slots(5, 9, self.fl)):
            k = clamp((self.g - 0.1 - i * 0.045) / 0.22) * clamp(self.lg * 3.0)
            a = -(25.0 + i * 16.0) * math.pi / 180.0
            Lp = self.A * 0.16 * m * k
            ex = top[0] + math.cos(a) * Lp
            ey = top[1] + math.sin(a) * Lp
            if k < 0.02:
                continue
            self._seg(top, (ex, ey), 2.5, (138, 168, 96))
            self._lobed(ex, ey, 1 if math.cos(a) > 0 else -1, self.A * 0.1 * m * k)
        kr = sm((self.g - 0.62) / 0.3)
        if kr > 0.05:
            for j, (o, d) in enumerate([[-1, 0.5], [1, 0.7], [0, 1.3], [-0.5, 1.9], [0.7, 2]][:self._slots(2, 5, self.ff)]):
                col = mixc([120, 170, 70], [238, 150, 50], sm((self.g - 0.8) / 0.2))
                self._fruit(top[0] + o * self.A * 0.035, top[1] + self.A * 0.025 + d * self.A * 0.03 * kr, self.A * 0.026 * kr + 2, self.A * 0.04 * kr + 2, o * 0.2, col)

    def _draw_mango(self):
        top = self._pq(self.sg)
        m = 0.6 + 0.4 * self.vs
        tw = self.A * 0.032 * m * self.th
        poly = [(self.cx - tw * 1.4, self.gy), (top[0] - tw, top[1]), (top[0] + tw, top[1]), (self.cx + tw * 1.4, self.gy)]
        pygame.draw.polygon(self.surface, (107, 74, 48), poly)
        branches = [[0.45, -1, 40, 0.2], [0.55, 1, 40, 0.22], [0.68, -1, 28, 0.22], [0.74, 1, 26, 0.24], [0.88, -1, 14, 0.16], [0.9, 1, 14, 0.16], [0.95, 0, 0, 0.13]]
        keep = [6, 2, 3, 0, 1, 4, 5][:self._slots(4, 7, self.fb)]
        for i, (q, s, a, lf) in enumerate(branches):
            if i not in keep:
                continue
            k = clamp((self.lg - q + 0.05) / 0.2)
            if k < 0.02:
                continue
            p = self._pq(min(q, self.sg))
            r = a * math.pi / 180.0
            ex = p[0] + s * math.sin(r) * self.A * lf * k * m
            ey = p[1] - math.cos(r) * self.A * lf * k * m
            rc = self.A * 0.1 * k * m
            self._seg(p, (ex, ey), tw * 0.6 * k + 1, (107, 74, 48))
            self.cnt['br'] += 1
            self.cnt['leaf'] += 1
            pygame.draw.circle(self.surface, self.LD, (int(ex), int(ey)), int(rc))
            kr = sm((self.g - 0.64 - i * 0.01) / 0.3)
            if kr > 0.05 and (i % 2 == 0 or self.ff > 0.55):
                rx, ry = self.A * 0.025 * kr + 2, self.A * 0.035 * kr + 2
                col = mixc([96, 150, 60], [238, 160, 50], sm((self.g - 0.8) / 0.2))
                self._fruit(ex + s * rc * 0.4, ey + rc * 0.7 + 4 + ry, rx, ry, s * 0.25, col)

    def render(self, sim, time_val):
        self.cnt = {'leaf': 0, 'br': 0, 'fr': 0}
        key = sim.crop_key
        c = CROP_DATA.get(key)

        W, Hc = self.surface.get_size()

        self.g = sim.g if c else 0.0
        self.dead = sm(getattr(sim, 'dead_t', 0.0)) if c else 0.0
        self.vs = (sim.vs if c else 1.0) * (1.0 - 0.65 * self.dead)
        self.fb, self.fl, self.ff = (sim.fb, sim.fl, sim.ff) if c else (1.0, 1.0, 1.0)
        self.gy = Hc * 0.84
        self.cx = W / 2.0
        self.A = self.gy - 26 * self.k
        self.sw = math.sin(time_val * 1.4) * 2.2 * (1.0 - self.dead) + 10.0 * self.dead
        self.WOB = c['wob'] if c else 0
        self.HEL = c['hel'] if c else 0

        self.sg = sm((self.g - 0.07) / 0.61)
        self.lg = self.sg * sm((self.g - 0.20) / 0.12)
        sp = SPROUT.get(key, SPROUT_DEFAULT)
        grow_t = sm((self.g - 0.08) / 0.55)
        self.th = sp['th0'] + (1.0 - sp['th0']) * grow_t
        self.yg = 1.0 - grow_t
        self.young = sp['stem']
        self.hook = max(sp['hook'] * (1.0 - sm((self.g - 0.10) / 0.12)), 0.35 * self.dead)
        self.HF = (c['hmax'] if c else 0.5) * self.A * (0.55 + 0.45 * self.vs)
        st = 1.0 - clamp((self.vs - 0.3) / 0.45)
        self.st = st
        self.LD = mixc([40, 116, 48], [140, 120, 40], st)
        self.LL = mixc([110, 176, 74], [200, 170, 80], st)
        if self.dead > 0.0:
            self.LD = mixc(self.LD, DEAD_LEAF, self.dead)
            self.LL = mixc(self.LL, DEAD_RIB, self.dead)

        self.rain = clamp(getattr(sim, 'rain', 0.0))
        self.dry = clamp(getattr(sim, 'dry', 0.0))
        self._draw_scene(sim, W, Hc, time_val)

        if not c:
            return

        self._draw_shadow()

        if self.g > 0.03:
            R = self.A * 0.17 * sm(self.g * 1.6)
            kk = self.k
            pts = [(self.cx, self.gy + 8 * kk), (self.cx + 4 * kk, self.gy + R * 0.5), (self.cx - 2 * kk, self.gy + R)]
            pygame.draw.lines(self.surface, self._dc((225, 208, 170)), False, pts, self._w(2))

        draw_methods = {
            'corn': self._draw_corn, 'tomato': self._draw_tomato, 'egg': self._draw_eggplant,
            'bitter': self._draw_bitter, 'okra': self._draw_okra, 'banana': self._draw_banana,
            'beans': self._draw_beans, 'squash': self._draw_squash, 'bottle': self._draw_bottle,
            'chili': self._draw_chili, 'papaya': self._draw_papaya, 'mango': self._draw_mango
        }
        self._draw_seed(key)
        if self.sg > 0.004 and key in draw_methods:
            draw_methods[key]()
        self._draw_cotyledons(key)
        self._draw_day_badge(sim)


    # ------------------------------------------------------------------
    # Scene: sky, sun, clouds, hills, moisture-tinted soil, grass, weather
    # ------------------------------------------------------------------
    SKY_KEYS = (
        (0.00, (150, 200, 238), (255, 238, 206)),   # morning
        (0.45, (106, 178, 236), (208, 234, 248)),   # midday
        (0.80, (124, 170, 226), (250, 228, 192)),   # afternoon
        (1.00, (236, 164, 124), (255, 216, 152)),   # golden hour
    )

    def _sky_colors(self, g, dead, rain=0.0, dry=0.0):
        keys = self.SKY_KEYS
        top, hor = keys[-1][1], keys[-1][2]
        for i in range(len(keys) - 1):
            g0, t0, h0 = keys[i]
            g1, t1, h1 = keys[i + 1]
            if g <= g1:
                f = clamp((g - g0) / (g1 - g0))
                top, hor = mixc(t0, t1, f), mixc(h0, h1, f)
                break
        if dry > 0.0:
            top = mixc(top, (84, 160, 226), 0.55 * dry)      # deep clear blue
            hor = mixc(hor, (255, 230, 184), 0.55 * dry)     # hot, hazy horizon
        if rain > 0.0:
            top = mixc(top, (92, 104, 120), 0.88 * rain)     # heavy overcast
            hor = mixc(hor, (168, 176, 186), 0.88 * rain)
        if dead > 0.0:
            top = mixc(top, (150, 156, 162), 0.75 * dead)
            hor = mixc(hor, (196, 198, 198), 0.75 * dead)
        return top, hor

    def _soil_colors(self, moist, dead, rain=0.0):
        wet = clamp(moist / 100.0)
        top = mixc((156, 114, 70), (86, 60, 40), wet)
        if rain > 0.0:
            top = mixc(top, (62, 44, 30), 0.18 * rain)
        if dead > 0.0:
            top = mixc(top, (120, 100, 78), 0.35 * dead)
        return top, mixc(top, (30, 20, 12), 0.45)

    def _puddles(self, W, Hc):
        rng = random.Random(3)
        gy = self.gy
        depth = max(1.0, Hc - gy)
        return [(W * (0.06 + 0.88 * rng.random()), gy + (7 + 9 * rng.random()) * self.k,
                 (30 + 46 * rng.random()) * self.k) for _ in range(6)]

    def _build_background(self, W, Hc, g, dead, moist, rain=0.0, dry=0.0):
        k = self.k
        gy = int(self.gy)
        bg = pygame.Surface((W, Hc), 0, 32)
        top, hor = self._sky_colors(g, dead, rain, dry)
        for y in range(gy + 1):
            pygame.draw.line(bg, mixc(top, hor, (y / max(1, gy)) ** 1.4), (0, y), (W, y))

        far = mixc((150, 196, 164), hor, 0.35 + 0.4 * dead)
        near = mixc((112, 168, 96), (150, 150, 120), 0.6 * dead)
        far = mixc(far, (138, 152, 152), 0.65 * rain)
        near = mixc(near, (88, 126, 86), 0.55 * rain)
        far = mixc(far, (196, 200, 150), 0.35 * dry)
        near = mixc(near, (176, 164, 96), 0.5 * dry)
        for col, base, amp, ph, fr in ((far, 0.20, 0.07, 0.6, 2.1), (near, 0.10, 0.05, 2.4, 3.3)):
            pts = [(0, gy)]
            for x in range(0, W + 8, 8):
                u = x / float(W)
                h = base + amp * (0.55 * math.sin(u * fr * math.pi + ph) + 0.45 * math.sin(u * fr * 2.3 * math.pi + ph * 1.7))
                pts.append((x, gy - h * gy * 0.55))
            pts.append((W, gy))
            pygame.draw.polygon(bg, col, pts)

        if dry > 0.05:
            hh = max(4, int(Hc * 0.14))
            haze = pygame.Surface((W, hh), pygame.SRCALPHA)
            for y in range(hh):
                a = int(80 * dry * (y / float(hh)) ** 1.6)
                pygame.draw.line(haze, (255, 236, 190, a), (0, y), (W, y))
            bg.blit(haze, (0, gy - hh))

        st, sb = self._soil_colors(moist, dead, rain)
        self.soil_col = st
        depth = max(1, Hc - gy)
        for y in range(gy, Hc):
            pygame.draw.line(bg, mixc(st, sb, (y - gy) / float(depth)), (0, y), (W, y))
        for d in self.dots:
            col = mixc(st, (30, 18, 8), 0.75) if d[3] > 0.5 else mixc(st, (210, 170, 120), 0.55)
            pygame.draw.circle(bg, col, (int(d[0] * W), int(gy + 8 * k + d[1] * (Hc - gy - 10 * k))), max(1, int(d[2] * k)))

        if dry > 0.3 and moist < 55:
            crng = random.Random(5)
            ccol = mixc(st, (24, 14, 8), 0.7)
            for _ in range(int(18 * dry)):
                x = crng.random() * W
                y = gy + 3 * k
                pts = [(x, y)]
                for _s in range(crng.randint(3, 6)):
                    x += (crng.random() - 0.5) * 16 * k
                    y += (4 + crng.random() * 9) * k
                    if y > Hc:
                        break
                    pts.append((x, y))
                if len(pts) > 1:
                    pygame.draw.lines(bg, ccol, False, pts, self._w(1))

        if rain > 0.4:
            for px, py, pw in self._puddles(W, Hc):
                ph_ = max(2, int(pw * 0.14))
                pygame.draw.ellipse(bg, mixc((140, 172, 200), st, 0.3), (int(px - pw / 2), int(py - ph_ / 2), int(pw), ph_))
                pygame.draw.ellipse(bg, mixc((200, 220, 238), st, 0.15), (int(px - pw * 0.3), int(py - ph_ * 0.3), int(pw * 0.35), max(1, int(ph_ * 0.25))))

        grass = mixc((88, 166, 62), (150, 130, 70), 0.8 * dead)
        grass = mixc(grass, (62, 142, 62), 0.3 * rain)
        grass = mixc(grass, (156, 142, 74), 0.5 * dry)
        pygame.draw.rect(bg, grass, (0, gy - int(3 * k), W, max(2, int(5 * k))))
        rng = random.Random(11)
        x = 0.0
        while x < W:
            hgt = (3 + rng.random() * 8) * k
            lean = (rng.random() - 0.5) * 4 * k
            shade = mixc(grass, (60, 130, 50), rng.random() * 0.6)
            pygame.draw.polygon(bg, shade, [(x, gy - 2 * k), (x + 2.2 * k, gy - 2 * k), (x + 1.1 * k + lean, gy - 2 * k - hgt)])
            x += (4 + rng.random() * 6) * k
        return bg

    def _sprite(self, key, builder):
        spr = self._cache.get(key)
        if spr is None:
            if len(self._cache) > 120:
                self._cache.clear()
            spr = builder()
            self._cache[key] = spr
        return spr

    def _sun_sprite(self, r, warm):
        def build():
            s = pygame.Surface((r * 5, r * 5), pygame.SRCALPHA)
            c = (r * 5 // 2, r * 5 // 2)
            core = mixc((255, 247, 214), (255, 196, 120), warm)
            for i in range(14, 0, -1):
                rad = int(r * (1.0 + 1.5 * i / 14.0))
                pygame.draw.circle(s, (*core, 9), c, rad)
            pygame.draw.circle(s, (*core, 255), c, r)
            return s
        return self._sprite(('sun', r, round(warm, 1)), build)

    def _cloud_sprite(self, w, h, shade):
        def build():
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            col = mixc((255, 255, 255), (150, 154, 162), shade)
            for fx, fy, fw, fh in ((0.05, 0.45, 0.45, 0.50), (0.28, 0.12, 0.42, 0.62), (0.52, 0.30, 0.43, 0.55), (0.18, 0.55, 0.62, 0.42)):
                pygame.draw.ellipse(s, (*col, 225), (int(fx * w), int(fy * h), int(fw * w), int(fh * h)))
            return s
        return self._sprite(('cloud', w, h, round(shade, 1)), build)

    # (x offset, y, speed, scale, rain_only)
    CLOUDS = (
        (0.10, 0.12, 7.0, 1.00, False),
        (0.55, 0.26, 10.0, 0.75, False),
        (0.85, 0.19, 5.0, 0.90, False),
        (0.25, 0.04, 6.0, 1.70, True),
        (0.70, 0.10, 8.0, 1.60, True),
        (0.45, 0.17, 4.0, 1.50, True),
        (0.95, 0.02, 5.0, 1.90, True),
    )

    def _draw_scene(self, sim, W, Hc, time_val):
        k = self.k
        g = clamp(self.g)
        dead = self.dead
        rain = self.rain
        dry = self.dry
        moist = getattr(sim, 'moist', 60.0)
        key = (W, Hc, int(g * 30), int(dead * 10), int(moist / 4), int(rain * 10), int(dry * 10))
        bg = self._cache.get(('bg',) + key)
        if bg is None:
            old_keys = [ck for ck in self._cache if ck[0] == 'bg']
            if len(old_keys) >= 24:
                for ck in old_keys:
                    del self._cache[ck]
            bg = self._build_background(W, Hc, g, dead, moist, rain, dry)
            self._cache[('bg',) + key] = bg
        else:
            self.soil_col = self._soil_colors(moist, dead, rain)[0]
        self.surface.blit(bg, (0, 0))

        gy = self.gy
        warm = (abs(g - 0.5) * 2.0) ** 2
        r = int(max(8, int(Hc * 0.045)) * (1.0 + 0.35 * round(dry, 1)))
        spr = self._sun_sprite(r, warm)
        sx = W * (0.12 + 0.70 * g)
        sy = gy * (0.50 - 0.34 * math.sin(math.pi * g))
        sun_a = (1.0 - 0.75 * dead) * (1.0 - 0.92 * rain)
        if sun_a < 0.995:
            spr = spr.copy()
            spr.set_alpha(int(255 * max(0.0, sun_a)))
        if sun_a > 0.02:
            self.surface.blit(spr, (int(sx - spr.get_width() / 2), int(sy - spr.get_height() / 2)))

        cw, ch = int(Hc * 0.34), int(Hc * 0.12)
        for base, yy, speed, scale, rain_only in self.CLOUDS:
            if rain_only:
                vis = clamp(rain * 1.4)
                shade = 0.82
            else:
                vis = 1.0 - 0.85 * dry
                shade = min(0.9, 0.55 * dead + 0.75 * rain)
            if vis < 0.03:
                continue
            sp_ = self._cloud_sprite(int(cw * scale), int(ch * scale), shade)
            if vis < 0.98:
                sp_ = sp_.copy()
                sp_.set_alpha(int(255 * vis))
            span = W + sp_.get_width() * 2
            x = (base * span + time_val * speed * k) % span - sp_.get_width()
            self.surface.blit(sp_, (int(x), int(Hc * yy)))

        if rain > 0.03:
            self._draw_rain(W, Hc, time_val, rain)

    def _draw_rain(self, W, Hc, time_val, rain):
        k = self.k
        gy = self.gy
        seeds = self.__dict__.get("_rain_seeds")
        if seeds is None:
            rr = random.Random(21)
            seeds = self._rain_seeds = [(rr.random(), rr.random(), rr.random()) for _ in range(600)]
        n = min(len(seeds), int(rain * W / (6.5 * k)))
        col = (206, 220, 238)
        wd = self._w(1)
        for i in range(n):
            fx, sp, ph = seeds[i]
            yv = (time_val * (0.9 + 0.9 * sp) * 1.15 + ph) % 1.0
            y = yv * gy
            length = (11 + 9 * sp) * k
            x = (fx * W - yv * gy * 0.10) % W
            pygame.draw.line(self.surface, col, (x, y), (x - length * 0.16, min(gy + 4 * k, y + length)), wd)
        if rain > 0.4:
            ring = (214, 230, 244)
            for j, (px, py, pw) in enumerate(self._puddles(W, Hc)):
                for q in (0.0, 0.5):
                    ph = (time_val * 1.1 + j * 0.37 + q) % 1.0
                    rw, rh = pw * (0.15 + 0.85 * ph), max(2.0, pw * 0.14 * (0.15 + 0.85 * ph))
                    pygame.draw.ellipse(self.surface, mixc(ring, (140, 172, 200), ph), (int(px - rw / 2), int(py - rh / 2), int(rw), int(rh)), wd)

    def _draw_shadow(self):
        if self.g <= 0.07:
            return
        k = self.k
        rx = max(6.0, 8 * k + self.HF * 0.12 * self.sg)
        ry = max(2.0, rx * 0.16)
        s = pygame.Surface((int(rx * 2) + 4, int(ry * 2) + 4), pygame.SRCALPHA)
        pygame.draw.ellipse(s, (0, 0, 0, int(70 * (1.0 - 0.6 * self.dead) * (1.0 - 0.7 * self.rain))), (2, 2, int(rx * 2), int(ry * 2)))
        self.surface.blit(s, (int(self.cx - rx - 2), int(self.gy + 1.5 * k - ry)))

    def _font(self, size):
        cache = self.__dict__.setdefault("_fonts", {})
        f = cache.get(size)
        if f is None:
            if not pygame.font.get_init():
                pygame.font.init()
            f = pygame.font.SysFont("arial,helvetica,dejavusans", size, bold=True)
            cache[size] = f
        return f

    def _draw_day_badge(self, sim):
        day = getattr(sim, 'day', None)
        total = getattr(sim, 'real_total', None)
        if day is None or not total:
            return
        W, Hc = self.surface.get_size()
        big = self._font(max(14, int(Hc * 0.050)))
        small = self._font(max(11, int(Hc * 0.034)))

        done = sim.g >= 1.0
        d = int(round(total)) if done else int(day)
        tot = int(round(total))
        dead_t = getattr(sim, 'dead_t', 0.0)
        if dead_t > 0.0:
            stage = t("dead")
        elif sim.g < 0.07:
            stage = t("stage_seed")
        elif sim.g < 0.20:
            stage = t("stage_sprout")
        elif sim.g < 0.60:
            stage = t("stage_young")
        else:
            stage = t("stage_mature")
        line1 = f"{t('day')} {d:,} / {tot:,}"
        line2 = stage
        if tot >= 365:
            line2 += f"  -  {d / 365.0:.1f} yr"
        wmode = getattr(sim, 'weather', None)
        if wmode == "rain":
            line2 += "  |  " + t("weather_rainy")
        elif wmode == "dry":
            line2 += "  |  " + t("weather_dry")
        main_col = (255, 140, 130) if dead_t > 0.0 else (255, 255, 255)
        s1 = big.render(line1, True, main_col)
        s2 = small.render(line2, True, (190, 225, 185))

        pad = max(8, int(Hc * 0.022))
        bw = max(s1.get_width(), s2.get_width()) + pad * 2
        bh = s1.get_height() + s2.get_height() + pad * 2 - 2
        badge = pygame.Surface((bw, bh), pygame.SRCALPHA)
        rad = max(8, int(Hc * 0.022))
        pygame.draw.rect(badge, (22, 32, 26, 200), (0, 0, bw, bh), border_radius=rad)
        pygame.draw.rect(badge, (255, 255, 255, 46), (0, 0, bw, bh), width=max(1, int(Hc * 0.003)), border_radius=rad)
        badge.blit(s1, (bw - pad - s1.get_width(), pad))
        badge.blit(s2, (bw - pad - s2.get_width(), pad + s1.get_height() - 2))
        margin = max(8, int(Hc * 0.022))
        self.surface.blit(badge, (W - bw - margin, margin))
# <<< PYGAME-SIM-END


SIM = SimulationEngine()
SIM_VIEW = {}
SIM_UI = {}
_sim_clock = {"t": 0.0, "accum": 0.0, "warned": False}
_last_inputs = {"t": None}
SIM_FPS = 30.0
SIM_SUPERSAMPLE = 2   # draw at 2x then smooth-scale down -> anti-aliased edges
_SURF_BYTES = getattr(pygame.image, "tobytes", None) or pygame.image.tostring


# >>> PANEL-LINK-BEGIN
_PROBE = {"size": None, "gfx": None}
_PROJ_CACHE = {}


def _stem_height_m(crop_key, vs, sg):
    c = CROP_DATA.get(crop_key)
    if c is None:
        return 0.0
    return (c['cm'] / 100.0) * (0.55 + 0.45 * clamp(vs)) * clamp(sg)


def projected_structure(sim):
    surf = SIM_VIEW.get("surface")
    if surf is None or not sim.crop_key:
        return None
    size = surf.get_size()
    key = (sim.crop_key, size, round(sim.target, 2), round(sim.tb, 2), round(sim.tl, 2), round(sim.tf, 2))
    hit = _PROJ_CACHE.get(key)
    if hit is not None:
        return hit
    if _PROBE["size"] != size:
        _PROBE["size"] = size
        _PROBE["gfx"] = GraphicsEngine(pygame.Surface(size, 0, 32), dots=[], k=SIM_VIEW.get("k", 1))
    probe = _PROBE["gfx"]
    fake = types.SimpleNamespace(crop_key=sim.crop_key, g=1.0, dead_t=0.0, vs=sim.target,
                                 fb=sim.tb, fl=sim.tl, ff=sim.tf)
    probe.render(fake, 0.0)
    result = {"leaf": probe.cnt['leaf'], "br": probe.cnt['br'], "fr": probe.cnt['fr'],
              "height_m": _stem_height_m(sim.crop_key, sim.target, 1.0)}
    if len(_PROJ_CACHE) > 300:
        _PROJ_CACHE.clear()
    _PROJ_CACHE[key] = result
    return result
# <<< PANEL-LINK-END


# ============================================================
# URSINA APP SETUP
# ============================================================

app = Ursina(
    title="BotaniQ",
    borderless=False,
    development_mode=False
)

window.size = (1400, 850)
window.color = Color(0.10, 0.11, 0.13, 1)
window.exit_button.visible = False
window.fps_counter.enabled = False


# ============================================================
# UI SETUP & PALETTE
# ============================================================

FIELD_KEYS = ["n", "p", "k", "ph", "moisture", "temp", "sunlight", "space"]

FIELD_GROUPS = [
    ("Soil Nutrients", ["n", "p", "k"]),
    ("Soil Properties", ["ph", "moisture"]),
    ("Climate", ["temp", "sunlight"]),
    ("Land / Space", ["space"])
]

BG_DARK = Color(0.075, 0.078, 0.086, 1)
PANEL_BG = Color(0.114, 0.122, 0.137, 1)
CARD_BG = Color(0.145, 0.153, 0.173, 1)
FIELD_BG = Color(0.165, 0.176, 0.20, 1)
BORDER_COL = Color(0.22, 0.24, 0.27, 1)

GREEN = Color(0.26, 0.78, 0.35, 1)
GREEN_BTN = Color(0.22, 0.62, 0.34, 1)
RED = Color(0.86, 0.30, 0.30, 1)
RED_BTN = Color(0.70, 0.22, 0.22, 1)
TEXT_WHITE = Color(0.94, 0.95, 0.96, 1)
TEXT_MUTED = Color(0.62, 0.65, 0.70, 1)


selected_crop = {"name": None}
recommendations = []
no_suitable_state = {"on": False}
ui_root = Entity(parent=camera.ui)
input_fields = {}
field_labels_by_key = {}
recommendation_buttons = []
UI = {}
VIEWPORT = {}
_error_popup = {"root": None}


def panel(pos, scale, col=PANEL_BG, z=0.02, parent=None):
    return Entity(
        parent=parent or ui_root,
        model="quad",
        color=col,
        position=(pos[0], pos[1], z),
        scale=scale
    )


_CHAR_WIDTH_AT_SCALE1 = 1.0 / (78 * 0.58)


def _wordwrap_for(width, scale):
    if scale <= 0:
        scale = 0.5
    safe_width = max(0.01, width) * 0.95
    return max(8, int(safe_width / (_CHAR_WIDTH_AT_SCALE1 * scale)))


def fit_text(ent, max_w, max_h, base_ww=None, min_f=0.40):
    """Shrink / re-wrap a Text entity until its REAL rendered bounds fit max_w x max_h
    (ui units). Measures the actual geometry, so it works for any font or language.
    If it still cannot fit at the minimum size, trailing lines are dropped with '...'."""
    try:
        base = getattr(ent, "_fit_base", None)
        if base is None:
            base = Vec3(*ent.scale)
            ent._fit_base = base
        ww_mult, f = 1.0, 1.0

        def apply():
            ent.scale = base * f
            if base_ww:
                ent.wordwrap = max(6, int(base_ww * ww_mult / f))

        def measure():
            b = ent.getTightBounds(ui_root)
            if not b:
                return None
            lo, hi = b
            return hi.x - lo.x, hi.y - lo.y

        for _ in range(40):
            apply()
            m = measure()
            if m is None:
                return
            w, h = m
            if w <= max_w and h <= max_h:
                return
            if w > max_w:
                if base_ww and ww_mult > 0.3:
                    ww_mult *= max(0.5, max_w / w) * 0.97
                else:
                    f *= max(0.6, max_w / w) * 0.98
            else:
                f *= max(0.80, max_h / h) * 0.98
            if f < min_f:
                f = min_f
                apply()
                break

        # last resort: drop trailing lines
        lines = str(ent.text).split("\n")
        while len(lines) > 1:
            lines.pop()
            ent.text = "\n".join(lines).rstrip() + " ..."
            apply()
            m = measure()
            if m is None or (m[0] <= max_w and m[1] <= max_h):
                break
    except Exception as e:
        print("fit_text skipped:", e)


def _fit_crop_info():
    box, ent = UI.get("crop_fit"), UI.get("crop_info_text")
    if box and ent is not None:
        fit_text(ent, box[0], box[1], base_ww=UI.get("crop_info_wordwrap"))


def _fit_sim_info():
    box, ent = UI.get("sim_fit"), UI.get("sim_info_text")
    if box and ent is not None:
        fit_text(ent, box[0], box[1], base_ww=UI.get("sim_info_wordwrap"))


def _set_wx_info(text, col):
    info = SIM_UI.get("wx_info")
    if info is None:
        return
    info.text = text
    info.color = col
    box = SIM_UI.get("wx_info_max")
    if box:
        fit_text(info, box[0], box[1])


_FIELD_FIT = {}


def _field_text_entity(field):
    te = getattr(field, "text_entity", None)
    if te is None:
        te = getattr(getattr(field, "text_field", None), "text_entity", None)
    return te


def _fit_input_texts():
    """Keep the typed number inside its long input box (shrinks only as needed)."""
    for key, field in input_fields.items():
        try:
            te = _field_text_entity(field)
            if te is None:
                continue
            txt = str(field.text)
            sig = (txt, id(te))
            if _FIELD_FIT.get(key) == sig:
                continue
            _FIELD_FIT[key] = sig
            if not any(c.isdigit() for c in txt):
                continue
            base = getattr(te, "_fit_base", None)
            if base is None:
                base = Vec3(*te.scale)
                te._fit_base, te._fit_f = base, 1.0
            b = te.getTightBounds(ui_root)
            if not b:
                continue
            w, h = b[1].x - b[0].x, b[1].y - b[0].y
            if w <= 1e-6 or h <= 1e-6:
                continue
            target_h, target_w = field.scale_y * 0.58, field.scale_x * 0.86
            f_new = te._fit_f * min(target_h / h, target_w / w)
            te._fit_f = max(0.25, min(1.0, f_new))
            te.scale = base * te._fit_f
        except Exception as e:
            print("input fit skipped:", e)


def _style_input_fields():
    """Typing indicator (caret) in the same green as the rest of the app."""
    for field in input_fields.values():
        try:
            for owner in (getattr(field, "text_field", None), field):
                cur = getattr(owner, "cursor", None) if owner is not None else None
                if cur is not None:
                    cur.color = GREEN
        except Exception:
            pass


def border_rect(center, size, col=BORDER_COL, thickness=0.0035, z=0.02, parent=None):
    w_, h_ = size
    cx, cy = center
    panel((cx, cy + h_ / 2 - thickness / 2), (w_, thickness), col, z, parent)
    panel((cx, cy - h_ / 2 + thickness / 2), (w_, thickness), col, z, parent)
    panel((cx - w_ / 2 + thickness / 2, cy), (thickness, h_), col, z, parent)
    panel((cx + w_ / 2 - thickness / 2, cy), (thickness, h_), col, z, parent)


def _create_sim_view(cx, cy, w_ui, h_ui):
    px_h = max(1, int(window.size.y))
    w_px = int(w_ui * px_h)
    h_px = int(h_ui * px_h)
    if w_px > 1000:
        h_px = int(h_px * 1000 / w_px)
        w_px = 1000
    w_px = max(240, w_px)
    h_px = max(160, h_px)

    ss = SIM_SUPERSAMPLE
    surface = pygame.Surface((w_px * ss, h_px * ss), 0, 32)
    small = pygame.Surface((w_px, h_px), 0, 32)
    old = SIM_VIEW.get("gfx")
    gfx = GraphicsEngine(surface, old.dots if old is not None else None, k=ss)
    tex = Texture(PILImage.new("RGBA", (w_px, h_px), (250, 248, 240, 255)))
    ent = Entity(parent=ui_root, model="quad", texture=tex, color=Color(1, 1, 1, 1),
                 position=(cx, cy, 0.03), scale=(w_ui, h_ui))
    SIM_VIEW.update({"surface": surface, "small": small, "k": ss, "gfx": gfx, "tex": tex, "entity": ent})
    _render_sim_frame()


def _render_sim_frame():
    gfx = SIM_VIEW.get("gfx")
    if gfx is None:
        return
    gfx.render(SIM, _sim_clock["t"])
    try:
        small = SIM_VIEW["small"]
        pygame.transform.smoothscale(SIM_VIEW["surface"], small.get_size(), small)
        data = _SURF_BYTES(small, "RGBA", True)
        SIM_VIEW["tex"]._texture.setRamImageAs(data, "RGBA")
    except Exception as e:
        if not _sim_clock["warned"]:
            _sim_clock["warned"] = True
            print("Simulation texture update failed:", e)


def build_ui(preserved_values=None):
    global ui_root, crop_info_text, crop_image, rec_bar_placeholder
    global reset_btn, recommend_btn, sim_info_text, LEFT_X, RIGHT_X, MARGIN
    global rec_bar_y, rec_bar_height

    current_crop = selected_crop["name"]

    if ui_root is not None:
        destroy(ui_root)

    ui_root = Entity(parent=camera.ui)
    input_fields.clear()
    field_labels_by_key.clear()
    recommendation_buttons.clear()

    aspect = max(1.0, window.aspect_ratio)
    MARGIN = 0.014
    LEFT_X = -aspect / 2
    RIGHT_X = aspect / 2
    TOP_Y = 0.5
    BOTTOM_Y = -0.5
    total_width = RIGHT_X - LEFT_X
    cursor = {"y": TOP_Y}

    def next_row(height, gap=0.010):
        top = cursor["y"]
        center = top - height / 2
        cursor["y"] = top - height - gap
        return center

    title_bar_h = 0.052
    title_bar_y = next_row(title_bar_h, gap=0.008)
    panel((0, title_bar_y), (total_width, title_bar_h))

    Text("BOTANIQ", parent=ui_root, position=(LEFT_X + MARGIN, title_bar_y - 0.010), origin=(-0.5, 0), z=0.01, scale=0.95, color=GREEN)
    Text(t("subtitle"), parent=ui_root, position=(LEFT_X + MARGIN + 0.145, title_bar_y - 0.0105), origin=(-0.5, 0), z=0.01, scale=0.65, color=TEXT_MUTED)

    rec_bar_y = next_row(0.060, gap=0.010)
    rec_bar_height = 0.060
    panel((0, rec_bar_y), (total_width, rec_bar_height))

    rec_bar_placeholder = Text(
        t("waiting_params"),
        parent=ui_root, position=(0, rec_bar_y - 0.010), origin=(0, 0), z=0.01, scale=0.78, color=GREEN
    )

    body_top = cursor["y"]
    body_bottom = BOTTOM_Y + MARGIN
    body_height = body_top - body_bottom
    body_center_y = (body_top + body_bottom) / 2

    col_gap = 0.018
    left_col_width = (total_width * 0.365) - MARGIN
    left_x_min = LEFT_X + MARGIN
    left_x_max = left_x_min + left_col_width
    left_center_x = (left_x_min + left_x_max) / 2

    right_x_min = left_x_max + col_gap
    right_x_max = RIGHT_X - MARGIN
    right_center_x = (right_x_min + right_x_max) / 2
    right_col_width = right_x_max - right_x_min

    panel((left_center_x, body_center_y), (left_col_width, body_height), col=CARD_BG)

    viewport_height = body_height * 0.70
    info_height = body_height - viewport_height - 0.018
    viewport_center_y = body_top - viewport_height / 2
    info_center_y = viewport_center_y - viewport_height / 2 - 0.018 - info_height / 2

    border_rect((right_center_x, viewport_center_y), (right_col_width, viewport_height))

    VIEWPORT["x_min"] = right_center_x - right_col_width / 2
    VIEWPORT["x_max"] = right_center_x + right_col_width / 2
    VIEWPORT["y_min"] = viewport_center_y - viewport_height / 2
    VIEWPORT["y_max"] = viewport_center_y + viewport_height / 2

    strip_h = 0.130
    inner_w = right_col_width - 0.010
    img_h = viewport_height - strip_h - 0.008
    img_cy = viewport_center_y + viewport_height / 2 - 0.004 - img_h / 2
    strip_cy = viewport_center_y - viewport_height / 2 + 0.004 + strip_h / 2
    strip_top = strip_cy + strip_h / 2

    _create_sim_view(right_center_x, img_cy, inner_w, img_h)

    sim_hint = Text(
        t("sim_hint"), parent=ui_root, position=(right_center_x, img_cy + img_h * 0.18, -0.01),
        origin=(0, 0), scale=0.8, color=Color(0.22, 0.30, 0.22, 1),
        wordwrap=_wordwrap_for(inner_w - 0.08, 0.8)
    )
    sim_hint.enabled = SIM.crop_key is None

    panel((right_center_x, strip_cy), (inner_w, strip_h), col=CARD_BG, z=0.03)

    bar_w = inner_w - 0.028
    bar_x0 = right_center_x - bar_w / 2
    bar_y = strip_top - 0.014
    panel((right_center_x, bar_y), (bar_w, 0.008), col=FIELD_BG, z=0.01)
    bar_fill = Entity(parent=ui_root, model="quad", color=GREEN, origin=(-0.5, 0),
                      position=(bar_x0, bar_y, 0.005), scale=(0.0001, 0.008))

    btn_y = strip_top - 0.044
    btn_h = 0.032
    btn_gap = 0.010
    bx = {"x": bar_x0}

    def add_btn(label, wfrac, col, callback):
        w = bar_w * wfrac
        b = Button(text=label, parent=ui_root, position=(bx["x"] + w / 2, btn_y, -0.005),
                   scale=(w, btn_h), color=col, text_size=0.55, radius=0.25,
                   highlight_scale=1.04, pressed_scale=0.96)
        b.on_click = callback
        bx["x"] += w + btn_gap
        return b

    play_btn = add_btn(t("pause"), 0.16, FIELD_BG, SIM.toggle_play)
    restart_btn = add_btn(t("sim_restart"), 0.16, FIELD_BG, SIM.reset)

    speed_btns = {}
    for spd in (0.5, 1.0, 2.0, 4.0):
        speed_btns[spd] = add_btn(f"{spd:g}x", 0.10, FIELD_BG, (lambda s=spd: setattr(SIM, "speed", s)))

    # ---- weather row (Carmona, Cavite) ----
    wx_y = btn_y - btn_h - 0.014
    Text(t("weather_label"), parent=ui_root, position=(bar_x0 + 0.002, wx_y, -0.005),
         origin=(-0.5, 0), scale=0.6, color=TEXT_MUTED)
    wx_x = bar_x0 + 0.215
    wx_w = max(0.07, bar_w * 0.13)
    wx_btns = {}
    for mode, label_key in (("rain", "weather_btn_rain"), ("dry", "weather_btn_dry"), ("live", "weather_btn_live")):
        wb = Button(text=t(label_key), parent=ui_root, position=(wx_x + wx_w / 2, wx_y, -0.005),
                    scale=(wx_w, btn_h), color=FIELD_BG, text_size=0.55, radius=0.25,
                    highlight_scale=1.04, pressed_scale=0.96)
        wb.on_click = (lambda m=mode: toggle_weather(m))
        wx_btns[mode] = wb
        wx_x += wx_w + btn_gap
    wx_info_w = max(0.10, bar_x0 + bar_w - wx_x - 0.004)
    wx_info = Text(t("weather_pick"), parent=ui_root, position=(wx_x + 0.004, wx_y, -0.005),
                   origin=(-0.5, 0), scale=0.52, color=TEXT_MUTED)

    SIM_UI.clear()
    SIM_UI.update({"play": play_btn, "restart": restart_btn, "speeds": speed_btns,
                   "bar": bar_fill, "bar_w": bar_w, "hint": sim_hint,
                   "wx_btns": wx_btns, "wx_info": wx_info, "wx_info_max": (wx_info_w, btn_h), "last_wx": "unset",
                   "last_play": None})

    panel((right_center_x, info_center_y), (right_col_width, info_height), col=CARD_BG)

    Text(t("what_generated"), parent=ui_root, position=(right_x_min + 0.014, info_center_y + info_height / 2 - 0.018), origin=(-0.5, 0), z=0.01, scale=0.95, color=GREEN)

    sim_info_scale = 0.68
    sim_info_width = right_col_width - 0.028 - MARGIN
    sim_info_wordwrap = _wordwrap_for(sim_info_width, sim_info_scale)
    sim_info_text = Text(
        t("sim_info_default"),
        parent=ui_root, position=(right_x_min + 0.014, info_center_y + info_height / 2 - 0.050),
        origin=(-0.5, 0.5), z=0.01, scale=sim_info_scale, color=TEXT_MUTED,
        wordwrap=sim_info_wordwrap
    )
    UI["sim_info_text"] = sim_info_text
    UI["sim_info_wordwrap"] = sim_info_wordwrap
    UI["sim_fit"] = (sim_info_width, info_height - 0.050 - 0.012)

    lcursor = {"y": body_top - MARGIN}

    def next_left_row(height, gap=0.010):
        top = lcursor["y"]
        center = top - height / 2
        lcursor["y"] = top - height - gap
        return center

    card_height = 0.255
    card_y = next_left_row(card_height, gap=0.012)
    panel((left_center_x, card_y), (left_col_width - 2 * MARGIN, card_height), col=PANEL_BG, z=0.015)

    image_size = card_height - 0.02
    image_x = left_x_min + MARGIN + image_size / 2 + 0.01

    crop_image = Entity(parent=ui_root, model="quad", texture="white_cube", color=Color(0.3, 0.32, 0.36, 1), position=(image_x, card_y, 0.01), scale=image_size)

    text_x = image_x + image_size / 2 + 0.02

    crop_info_scale = 0.62
    crop_info_right_edge = left_x_min + left_col_width - MARGIN - 0.012
    crop_info_width = crop_info_right_edge - text_x
    crop_info_text = Text(
        t("crop_profile_default"),
        parent=ui_root,
        position=(text_x, card_y + card_height / 2 - 0.020),
        z=0.005,
        scale=crop_info_scale,
        color=GREEN,
        wordwrap=_wordwrap_for(crop_info_width, crop_info_scale)
    )
    UI["crop_info_scale"] = crop_info_scale
    UI["crop_info_wordwrap"] = _wordwrap_for(crop_info_width, crop_info_scale)
    UI["crop_fit"] = (crop_info_width, card_height - 0.036)

    label_x = left_x_min + MARGIN
    field_x = left_x_min + left_col_width * 0.52
    field_width = left_col_width * 0.48 - MARGIN * 2

    for sec_name, keys in FIELD_GROUPS:
        header_y = next_left_row(0.026, gap=0.003)
        Text(section_title(sec_name), parent=ui_root, position=(label_x, header_y), z=0.005, scale=0.85, color=GREEN)

        for key in keys:
            row_y = next_left_row(0.038, gap=0.010)
            lbl = Text(field_label(key), parent=ui_root, position=(label_x, row_y + 0.004), z=0.005, scale=0.72, color=TEXT_WHITE)
            field_labels_by_key[key] = lbl
            guide_txt = Text(field_guide(key), parent=ui_root, position=(label_x, row_y - 0.0165), z=0.005,
                             origin=(-0.5, 0.5), scale=0.50, color=TEXT_MUTED)
            fit_text(lbl, field_x - label_x - 0.014, 0.026)
            fit_text(guide_txt, field_x - label_x - 0.014, 0.016)

            field = InputField(
                parent=ui_root, position=(field_x + field_width / 2, row_y), z=0.003,
                scale=(field_width, 0.038), limit_content_to="0123456789.", default_value=""
            )
            field.color = FIELD_BG
            field.text_color = TEXT_WHITE

            try:
                field.text_entity.scale = 0.85
                field.text_entity.origin = (0, 0)
            except Exception:
                pass

            if preserved_values and key in preserved_values:
                field.text = preserved_values[key]

            input_fields[key] = field

    buttons_y = body_bottom + 0.030
    available_btn_width = left_col_width - 2 * MARGIN - 0.015
    reset_width = available_btn_width * 0.32
    recommend_width = available_btn_width * 0.68

    current_bx = left_x_min + MARGIN

    reset_btn = Button(
        text=t("reset"), parent=ui_root, position=(current_bx + reset_width / 2, buttons_y),
        z=0.005, scale=(reset_width, 0.052), color=FIELD_BG, text_size=0.70,
        radius=0.25, highlight_scale=1.03, pressed_scale=0.97
    )
    reset_btn.on_click = reset_fields
    current_bx += reset_width + 0.015

    recommend_btn = Button(
        text=t("recommend"), parent=ui_root, position=(current_bx + recommend_width / 2, buttons_y),
        z=0.005, scale=(recommend_width, 0.052), color=GREEN_BTN, text_size=0.70,
        radius=0.25, highlight_scale=1.03, pressed_scale=0.97
    )
    recommend_btn.on_click = on_recommend_pressed

    UI["crop_info_text"] = crop_info_text
    UI["crop_image"] = crop_image
    UI["rec_bar_placeholder"] = rec_bar_placeholder
    _fit_crop_info()
    _fit_sim_info()
    _FIELD_FIT.clear()

    if recommendations:
        update_recommendations_bar()
    if current_crop:
        selected_crop["name"] = current_crop
        refresh_crop_display(current_crop)
        update_sim_info(current_crop, get_current_parameters())
    elif no_suitable_state["on"]:
        show_no_suitable(get_current_parameters())


def get_current_parameters():
    defaults = {
        "n": 100.0, "p": 50.0, "k": 50.0, "ph": 6.5,
        "moisture": 60.0, "temp": 28.0, "sunlight": 7.0, "space": 1.0
    }

    values = {}
    for key in FIELD_KEYS:
        text = input_fields[key].text.strip()
        try:
            values[key] = float(text) if text else defaults[key]
        except ValueError:
            values[key] = defaults[key]
    return values


def set_bar_message(msg):
    UI["rec_bar_placeholder"].enabled = True
    UI["rec_bar_placeholder"].text = msg


def clear_recommendation_buttons():
    for b in recommendation_buttons:
        destroy(b)
    recommendation_buttons.clear()


def update_recommendations_bar():
    clear_recommendation_buttons()
    UI["rec_bar_placeholder"].enabled = False

    n = len(recommendations)
    if n == 0:
        set_bar_message(t("no_suitable_bar") if no_suitable_state["on"] else t("waiting_params"))
        return

    gap = 0.012
    chip_width = ((RIGHT_X - LEFT_X) - 2 * MARGIN - (n - 1) * gap) / n
    x = LEFT_X + MARGIN + chip_width / 2

    for rank, (crop_name, pct) in enumerate(recommendations):
        if rank == 0: col = Color(0.42, 0.33, 0.08, 1)
        elif rank == 1: col = Color(0.30, 0.31, 0.33, 1)
        elif rank == 2: col = Color(0.35, 0.20, 0.10, 1)
        elif pct < 50: col = Color(0.30, 0.18, 0.18, 1)
        elif pct < 75: col = Color(0.30, 0.26, 0.16, 1)
        else: col = Color(0.17, 0.28, 0.19, 1)

        btn = Button(
            text=f"#{rank + 1} {crop_name} \u2022 {pct:.1f}%",
            parent=ui_root, position=(x, rec_bar_y), z=0.01,
            scale=(chip_width, rec_bar_height - 0.015), color=col, text_size=0.65
        )
        btn.on_click = Func(select_crop, crop_name)
        recommendation_buttons.append(btn)
        x += chip_width + gap


def resolve_crop_image_path(image_path):
    if not image_path:
        return None

    raw = Path(str(image_path))
    script_dir = Path(__file__).resolve().parent
    search_dirs = [Path.cwd(), script_dir, script_dir / 'assets']

    candidates = [raw, *(d / raw for d in search_dirs)]
    for candidate in candidates:
        try:
            if candidate.is_file():
                return candidate.resolve()
        except OSError:
            pass

    stem = raw.stem.lower()
    target_dirs = {(d / raw.parent) for d in search_dirs}
    target_dirs.add(script_dir / 'images')
    for folder in target_dirs:
        try:
            if not folder.is_dir():
                continue
            for f in folder.iterdir():
                if f.is_file() and f.stem.lower() == stem and f.suffix.lower() in (
                    '.png', '.jpg', '.jpeg', '.webp'
                ):
                    return f.resolve()
        except OSError:
            pass

    return None


_missing_image_warned = set()


def refresh_crop_display(crop_name):
    data = CROPS.get(crop_name)
    if not data:
        return

    description_bullets = "\n".join(
        f"\u2022 {line}" for line in (data["description"], f"{t('uses')}: {data['uses']}")
    )
    current_values = get_current_parameters()
    suitability = calculate_suitability_score(crop_name, current_values)
    unsuitable_tag = "" if assess_viability(crop_name, current_values)["viable"] else f" \u2022 {t('not_suitable_tag')}"

    crop_type_display = fil_translate(data['type'], CROP_TYPE_FIL)
    info_text = (
        f"{crop_name}\n"
        f"{crop_type_display} \u2022 {data['growth']}\n"
        f"{t('suitability')}: {suitability:.1f}%{unsuitable_tag}\n"
        f"N:{data['n'][0]} P:{data['p'][0]} K:{data['k'][0]}  pH {data['ph'][0]}-{data['ph'][1]}\n"
        f"{t('moisture')} {data['moisture'][0]}-{data['moisture'][1]}%  {t('temp')} {data['temp'][0]}-{data['temp'][1]}C\n\n"
        f"{description_bullets}"
    )

    UI["crop_info_text"].text = info_text
    ww = UI.get("crop_info_wordwrap")
    if ww:
        UI["crop_info_text"].wordwrap = ww
    _fit_crop_info()

    image_path = resolve_crop_image_path(data.get("image"))
    if image_path is not None:
        try:
            UI["crop_image"].texture = load_texture(str(image_path))
            UI["crop_image"].color = color.white
        except Exception as e:
            print(f"Could not load crop image '{image_path}':", e)
            UI["crop_image"].texture = None
            UI["crop_image"].color = Color(0.3, 0.3, 0.3, 1)
    else:
        if crop_name not in _missing_image_warned:
            _missing_image_warned.add(crop_name)
            script_dir = Path(__file__).resolve().parent
            print(
                f"[BotaniQ] No image found for '{crop_name}'. "
                f"Looked for '{data.get('image')}' next to the script "
                f"({script_dir}) and in {script_dir / 'images'} / "
                f"{script_dir / 'assets'} (case-insensitive, "
                f".png/.jpg/.jpeg/.webp). Add a matching file there."
            )
        UI["crop_image"].texture = None
        UI["crop_image"].color = Color(0.3, 0.3, 0.3, 1)


def conditions_text(reasons):
    return ", ".join(t(f"why_{k}_{d}") for k, d in reasons[:3])


def show_no_suitable(values):
    no_suitable_state["on"] = True
    best = max(CROPS, key=lambda c: calculate_suitability_score(c, values))
    reasons = assess_viability(best, values)["reasons"]
    selected_crop["name"] = None
    SIM.clear()

    set_bar_message(t("no_suitable_bar"))
    lines = [t("no_suitable_title"), "", t("no_suitable_body")]
    if reasons:
        lines += ["", f"{t('cause')}: {conditions_text(reasons)}"]
    UI["crop_info_text"].text = "\n".join(lines)
    ww = UI.get("crop_info_wordwrap")
    if ww:
        UI["crop_info_text"].wordwrap = ww
    _fit_crop_info()
    UI["crop_image"].texture = None
    UI["crop_image"].color = Color(0.3, 0.32, 0.36, 1)

    sim_info_text.text = t("no_suitable_sim")
    sim_ww = UI.get("sim_info_wordwrap")
    if sim_ww:
        sim_info_text.wordwrap = sim_ww
    _fit_sim_info()
    if SIM_UI.get("hint") is not None:
        SIM_UI["hint"].enabled = True


def _tier3(f, labels):
    return labels[0] if f <= 0.33 else (labels[1] if f <= 0.66 else labels[2])


def _sim_info_lines(crop_name, gfx, proj):
    key = SIM.crop_key
    now = gfx.cnt
    vigor = int(round(clamp(SIM.target) * 100))
    h_now = _stem_height_m(key, gfx.vs, gfx.sg)
    struct = CROP_STRUCTURE_RANGES.get(crop_name, _DEFAULT_STRUCTURE_RANGE)
    fruit_unit = fil_translate(struct["fruit_label"], FRUIT_LABEL_FIL)
    leaf_unit = t("leaf_clusters") if key == "mango" else t("leaves_unit")
    leaf_tier = fil_translate(_tier3(SIM.tl, ("sparse foliage", "moderate foliage", "lush foliage")), TIER_LEAF_FIL)
    if proj["br"] > 0:
        br_tier = fil_translate(_tier3(SIM.tb, ("sparse branching", "moderate branching", "dense branching")), TIER_BRANCH_FIL)
        branch_line = f"{t('branching')}: {now['br']} / {proj['br']} {t('stems')} ({br_tier})"
    else:
        branch_line = f"{t('branching')}: {t('unbranched')}"
    return (
        f"{crop_name} \u2022 {t('vigor')} {vigor}% {t('at_these_values')}\n"
        f"({t('now_and_full')})\n"
        f"{t('height')}: {h_now:.2f} m / {proj['height_m']:.2f} m\n"
        f"{branch_line}\n"
        f"{t('leaves')}: {now['leaf']} / {proj['leaf']} {leaf_unit} ({leaf_tier})\n"
        f"{t('fruit')}: {now['fr']} / {proj['fr']} {fruit_unit}"
    )


def update_sim_info(crop_name, values):
    _update_sim_info_core(crop_name, values)
    mode = WEATHER["mode"]
    if mode:
        try:
            sim_info_text.text = sim_info_text.text + "\n" + weather_summary_line(mode)
            sim_ww = UI.get("sim_info_wordwrap")
            if sim_ww:
                sim_info_text.wordwrap = sim_ww
        except Exception:
            pass
    _fit_sim_info()


def _update_sim_info_core(crop_name, values):
    try:
        a = assess_viability(crop_name, values)
        if not a["viable"]:
            if SIM.status in ("dying", "dead"):
                head = t("seed_failed") if a["die_g"] <= 0.09 else t("plant_died")
            else:
                head = t("will_die")
            cause = conditions_text(a["reasons"]) or t("why_generic")
            sim_info_text.text = (
                f"{crop_name} \u2022 {head}\n"
                f"{t('cause')}: {cause}\n"
                f"{t('suitability')}: {a['score']:.1f}% ({t('not_suitable_tag')})"
            )
            sim_ww = UI.get("sim_info_wordwrap")
            if sim_ww:
                sim_info_text.wordwrap = sim_ww
            return
        gfx = SIM_VIEW.get("gfx")
        proj = projected_structure(SIM) if (gfx is not None and SIM.crop_name == crop_name) else None
        if proj is not None:
            sim_info_text.text = _sim_info_lines(crop_name, gfx, proj)
        else:
            d = describe_plant_growth(crop_name, values)
            branch_desc_disp = fil_translate(d['branch_desc'], TIER_BRANCH_FIL)
            leaf_desc_disp = fil_translate(d['leaf_desc'], TIER_LEAF_FIL)
            fruit_label_disp = fil_translate(d['fruit_label'], FRUIT_LABEL_FIL)
            sim_info_text.text = (
                f"{crop_name} \u2022 {t('vigor')} {d['vigor_pct']}% {t('at_these_values')}\n"
                f"{t('height')}: ~{d['height_m']:.1f} m\n"
                f"{t('branching')}: ~{d['branch_count']} {t('stems')} ({branch_desc_disp})\n"
                f"{t('leaves')}: ~{d['leaf_count']} {t('leaves_unit')} ({leaf_desc_disp})\n"
                f"{t('fruit')}: ~{d['fruit_count']} {fruit_label_disp} {t('expected')}"
            )
        sim_ww = UI.get("sim_info_wordwrap")
        if sim_ww:
            sim_info_text.wordwrap = sim_ww
    except Exception:
        pass


WEATHER_BTN_COL = {"rain": Color(0.20, 0.45, 0.78, 1), "dry": Color(0.86, 0.56, 0.16, 1),
                   "live": Color(0.22, 0.62, 0.34, 1)}


def _fmt_num(x):
    return f"{x:g}"


def weather_name(mode):
    if mode == "live":
        return t("weather_live")
    return t("weather_rainy") if mode == "rain" else t("weather_dry")


def weather_summary_line(mode):
    if mode == "live":
        d = LIVE["data"]
        if d is None:
            return t("weather_live_wait")
        return t("weather_line_live").format(
            time=d["time"], cond=_wmo_name(d["code"]), temp=_fmt_num(d["temp"]),
            sun=_fmt_num(d["sunlight"]), moist=d["moisture"], rh=d["rh"])
    p = WEATHER_PROFILES[mode]
    return t("weather_line").format(
        name=weather_name(mode), temp=_fmt_num(p["temp"]), sun=_fmt_num(p["sunlight"]),
        rain=p["rain_mm"], moist=p["moisture"])


def weather_info_for_row(mode):
    """(text, colour) for the one-line status next to the weather buttons."""
    d = LIVE["data"]
    if mode == "live":
        if d is None:
            if LIVE["status"] == "error":
                return t("weather_live_err"), RED
            return t("weather_live_wait"), TEXT_MUTED
        line = t("weather_live_now").format(
            time=d["time"], temp=_fmt_num(d["temp"]), cond=_wmo_name(d["code"]),
            rh=d["rh"], sun=_fmt_num(d["sunlight"]), moist=d["moisture"])
        if LIVE["status"] == "stale":
            line += " " + t("weather_live_stale")
        return line, TEXT_WHITE
    if mode in ("rain", "dry"):
        return t("weather_short_" + mode).format(days=WEATHER_PROFILES[mode]["rain_days"]), TEXT_WHITE
    if d is not None:
        return t("weather_now_hint").format(temp=_fmt_num(d["temp"]), cond=_wmo_name(d["code"])), TEXT_MUTED
    return t("weather_pick"), TEXT_MUTED


def _visual_for(mode):
    if mode == "live":
        d = LIVE["data"]
        return d["visual"] if d else None
    return mode


def toggle_weather(mode):
    """Rainy / Dry = Carmona seasonal averages. Live = real current conditions in Carmona."""
    if WEATHER["mode"] == mode:
        WEATHER["mode"] = None
        SIM.set_weather(None)
        _refresh_after_weather()
        return
    WEATHER["mode"] = mode
    SIM.set_weather(_visual_for(mode))
    if mode == "live":
        _live_request_refresh()
        if LIVE["data"] is not None:
            _live_fill_fields()
    else:
        p = WEATHER_PROFILES[mode]
        for key in ("temp", "moisture", "sunlight"):
            input_fields[key].text = _fmt_num(p[key])
    _refresh_after_weather()


def _refresh_after_weather():
    crop = selected_crop["name"]
    if crop:
        values = get_current_parameters()
        SIM.set_environment(values)
        update_sim_info(crop, values)
        refresh_crop_display(crop)
        _last_inputs["t"] = tuple(input_fields[k].text for k in FIELD_KEYS)
    elif WEATHER["mode"]:
        sim_info_text.text = weather_summary_line(WEATHER["mode"])
        sim_ww = UI.get("sim_info_wordwrap")
        if sim_ww:
            sim_info_text.wordwrap = sim_ww
        _fit_sim_info()
    else:
        sim_info_text.text = t("sim_info_default")
        _fit_sim_info()


def select_crop(crop_name):
    selected_crop["name"] = crop_name
    if crop_name not in CROPS:
        return

    refresh_crop_display(crop_name)
    values = get_current_parameters()
    SIM.set_crop_and_environment(crop_name, values)
    SIM_UI.pop("live_sig", None)
    _render_sim_frame()
    update_sim_info(crop_name, values)
    if SIM_UI.get("hint") is not None:
        SIM_UI["hint"].enabled = False


def _poll_inputs():
    if not input_fields:
        return
    texts = tuple(input_fields[k].text for k in FIELD_KEYS)
    if texts == _last_inputs["t"]:
        return
    _last_inputs["t"] = texts
    mode = WEATHER["mode"]
    if mode:
        p = WEATHER_PROFILES[mode]
        try:
            same = all(abs(float(input_fields[k].text) - p[k]) < 0.05 for k in ("temp", "moisture", "sunlight"))
        except ValueError:
            same = False
        if mode == "live" and LIVE["data"] is None:
            same = True          # still waiting for the first live reading
        if not same:
            WEATHER["mode"] = None
            SIM.set_weather(None)
    crop = selected_crop["name"]
    if crop:
        values = get_current_parameters()
        SIM.set_environment(values)
        update_sim_info(crop, values)
        refresh_crop_display(crop)


def hide_missing_values_popup():
    root = _error_popup.get("root")
    if root is not None:
        destroy(root)
    _error_popup["root"] = None


def show_missing_values_popup(missing_labels):
    hide_missing_values_popup()

    root = Entity(parent=camera.ui, z=-0.6)
    _error_popup["root"] = root

    overlay = Button(
        parent=root, model="quad", color=Color(0, 0, 0, 0.55),
        scale=(window.aspect_ratio * 1.2, 1.2), z=0.01, highlight_color=Color(0, 0, 0, 0.55)
    )
    overlay.on_click = hide_missing_values_popup

    Entity(parent=root, model="quad", color=FIELD_BG, position=(0, 0.03, 0), scale=(0.62, 0.30))
    border_rect((0, 0.03), (0.62, 0.30), col=RED, thickness=0.004, z=-0.01, parent=root)

    Text(
        t("missing_values_title"), parent=root, position=(0, 0.115), origin=(0, 0),
        z=-0.02, scale=1.05, color=RED
    )

    if missing_labels:
        detail = t("missing_values_prefix") + "\n" + ", ".join(missing_labels)
    else:
        detail = t("missing_values_fallback")

    Text(
        detail, parent=root, position=(0, 0.045), origin=(0, 0), z=-0.02,
        scale=0.72, color=TEXT_WHITE, wordwrap=32, line_height=1.3
    )

    ok_btn = Button(
        text=t("ok"), parent=root, position=(0, -0.11), z=-0.02,
        scale=(0.18, 0.05), color=RED_BTN, text_size=0.75
    )
    ok_btn.on_click = hide_missing_values_popup


def on_recommend_pressed():
    missing_keys = [key for key in FIELD_KEYS if not input_fields[key].text.strip()]

    for key in FIELD_KEYS:
        label = field_labels_by_key.get(key)
        if label is not None:
            label.color = RED if key in missing_keys else TEXT_WHITE

    if missing_keys:
        missing_labels = [field_label(key) for key in missing_keys]
        show_missing_values_popup(missing_labels)
        set_bar_message(t("missing_values_bar"))
        return

    values = get_current_parameters()
    recs = recommend_crops(values)

    recommendations.clear()
    recommendations.extend(recs)
    no_suitable_state["on"] = False
    update_recommendations_bar()

    if recommendations:
        select_crop(recommendations[0][0])
    else:
        show_no_suitable(values)


def reset_fields():
    hide_missing_values_popup()

    for key in FIELD_KEYS:
        input_fields[key].text = ""
        label = field_labels_by_key.get(key)
        if label is not None:
            label.color = TEXT_WHITE

    recommendations.clear()
    clear_recommendation_buttons()
    no_suitable_state["on"] = False
    selected_crop["name"] = None
    WEATHER["mode"] = None
    SIM.set_weather(None)
    SIM.clear()

    UI["crop_info_text"].text = t("crop_profile_default")
    _fit_crop_info()
    UI["crop_image"].texture = None
    UI["crop_image"].color = Color(0.3, 0.32, 0.36, 1)
    sim_info_text.text = t("sim_info_default")
    _fit_sim_info()
    if SIM_UI.get("hint") is not None:
        SIM_UI["hint"].enabled = True

    set_bar_message(t("waiting_params"))


window.color = BG_DARK
build_ui()
set_bar_message(t("waiting_params"))

_last_window_size = [window.size.x, window.size.y]


def rebuild_ui_safely():
    try:
        values = {field_key: field.text for field_key, field in input_fields.items()}
        build_ui(preserved_values=values)
    except Exception as e:
        print("UI rebuild error:", e)


def _sim_ui_update():
    play_btn = SIM_UI.get("play")
    if play_btn is None:
        return

    if SIM.dead_t > 0.0:
        label = t("dead")
    else:
        label = t("pause") if SIM.play else (t("play") if SIM.g < 1.0 else t("done"))
    if label != SIM_UI.get("last_play"):
        SIM_UI["last_play"] = label
        play_btn.text = label

    for spd, b in SIM_UI.get("speeds", {}).items():
        want = GREEN_BTN if SIM.speed == spd else FIELD_BG
        if b.color != want:
            b.color = want
            b.highlight_color = want.tint(0.2)
            b.pressed_color = want.tint(-0.2)

    bar = SIM_UI.get("bar")
    if bar is not None:
        bar.scale_x = max(0.0001, SIM_UI["bar_w"] * SIM.g)
        want = RED if SIM.status in ("dying", "dead") else GREEN
        if bar.color != want:
            bar.color = want

    mode = WEATHER["mode"]
    wx_btns = SIM_UI.get("wx_btns")
    wx_key = (mode, LIVE["stamp"], LIVE["status"], LANG["code"])
    if wx_btns and wx_key != SIM_UI.get("last_wx"):
        SIM_UI["last_wx"] = wx_key
        for m, b in wx_btns.items():
            want = WEATHER_BTN_COL[m] if m == mode else FIELD_BG
            b.color = want
            b.highlight_color = want.tint(0.2)
            b.pressed_color = want.tint(-0.2)
        _set_wx_info(*weather_info_for_row(mode))

    status = SIM.status
    if status != SIM_UI.get("last_status"):
        SIM_UI["last_status"] = status
        crop = selected_crop["name"]
        if crop:
            update_sim_info(crop, get_current_parameters())

    gfx = SIM_VIEW.get("gfx")
    crop = selected_crop["name"]
    if gfx is not None and crop and SIM.crop_key and SIM.viable and SIM.crop_name == crop:
        sig = (gfx.cnt['leaf'], gfx.cnt['br'], gfx.cnt['fr'],
               round(_stem_height_m(SIM.crop_key, gfx.vs, gfx.sg), 2))
        now_t = _sim_clock["t"]
        if sig != SIM_UI.get("live_sig") and now_t - SIM_UI.get("live_t", -1.0) >= 0.2:
            SIM_UI["live_sig"] = sig
            SIM_UI["live_t"] = now_t
            update_sim_info(crop, get_current_parameters())


def _fade_register(bucket, entity):
    try:
        a = entity.color[3]
    except Exception:
        a = 1.0
    bucket.append((entity, a))
    return entity


def _fade_apply(bucket, k):
    k = max(0.0, min(1.0, k))
    for ent, a in bucket:
        try:
            c = ent.color
            ent.color = Color(c[0], c[1], c[2], a * k)
        except Exception:
            pass


def _smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def _mix(a, b, amt, alpha=1.0):
    return Color(a[0] + (b[0] - a[0]) * amt,
                 a[1] + (b[1] - a[1]) * amt,
                 a[2] + (b[2] - a[2]) * amt, alpha)


# ============================================================
# PROCEDURAL SOFT RADIAL GLOW GENERATOR FOR SMOOTH EDGE FADING
# ============================================================
def _create_radial_glow_texture(size=256, base_color=(66, 199, 89)):
    img = PILImage.new("RGBA", (size, size), (0, 0, 0, 0))
    pixels = img.load()
    center = size / 2.0
    max_radius = size / 2.0
    for y in range(size):
        for x in range(size):
            dx = x - center
            dy = y - center
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > max_radius:
                alpha = 0
            else:
                factor = 1.0 - (dist / max_radius)
                alpha = int(255 * (factor * factor * (3.0 - 2.0 * factor)))
            pixels[x, y] = (base_color[0], base_color[1], base_color[2], alpha)
    return Texture(img)


RADIAL_GLOW_TEX = _create_radial_glow_texture(256, (66, 199, 89))


# ============================================================
# WEATHER SCENE ART (shared by the language + loading screens)
# ============================================================
from PIL import ImageDraw, ImageFilter


def _gradient_image(stops, h=256):
    img = PILImage.new("RGBA", (4, h))
    px = img.load()
    for y in range(h):
        f = y / (h - 1)
        col = stops[-1][1]
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if f <= p1 or i == len(stops) - 2:
                u = 0.0 if p1 == p0 else max(0.0, min(1.0, (f - p0) / (p1 - p0)))
                col = tuple(int(c0[j] + (c1[j] - c0[j]) * u) for j in range(3))
                break
        for x in range(4):
            px[x, y] = col + (255,)
    return img


def _make_hills_image(W=2000, H=230):
    """Far ridge + mango trees + mid ridge + a ploughed field with rows running to the horizon."""
    img = PILImage.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def ridge(base, amp, waves, col):
        def yf(x):
            y = base * H
            for f, a, ph in waves:
                y += math.sin(x / W * f * 6.2832 + ph) * a * amp * H
            return y
        pts = [(0, H)] + [(x, yf(x)) for x in range(0, W + 1, 10)] + [(W, H)]
        d.polygon(pts, fill=col)
        return yf

    far = ridge(0.30, 0.16, [(2.2, 1.0, 0.4), (5.1, 0.35, 1.7)], (27, 58, 58, 255))
    mid = ridge(0.42, 0.12, [(3.4, 1.0, 2.0), (7.3, 0.30, 0.2)], (30, 84, 60, 255))
    for tx in (160, 470, 860, 1290, 1650, 1900):          # round-crowned fruit trees
        base_y = mid(tx) + 2
        d.rectangle((tx - 3, base_y - 20, tx + 3, base_y + 4), fill=(58, 44, 30, 255))
        for dx, dy, r in ((0, -34, 20), (-15, -26, 14), (15, -26, 14)):
            d.ellipse((tx + dx - r, base_y + dy - r, tx + dx + r, base_y + dy + r), fill=(22, 72, 46, 255))
    horizon = int(H * 0.56)
    d.rectangle((0, horizon, W, H), fill=(38, 108, 58, 255))
    vx, n = W / 2, 17
    for i in range(-n, n):
        shade = (46, 126, 64, 255) if i % 2 == 0 else (33, 94, 52, 255)
        d.polygon([(vx + i * 8, horizon), (vx + (i + 1) * 8, horizon),
                   (vx + (i + 1) * (W / 9), H), (vx + i * (W / 9), H)], fill=shade)
    return img.filter(ImageFilter.GaussianBlur(0.7))


def _make_cloud_image(seed, W=512, H=256):
    rr = random.Random(seed)
    layer = PILImage.new("L", (W, H), 0)
    d = ImageDraw.Draw(layer)
    for _ in range(11):
        rx = rr.uniform(0.10, 0.19) * W
        cx = rr.uniform(0.08 + rx / W + 0.04, 0.92 - rx / W - 0.04) * W      # keep blobs (and blur) inside the sprite
        cy = rr.uniform(0.46, 0.68) * H
        ry = rx * rr.uniform(0.45, 0.72)
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    d.rectangle((0, int(H * 0.70), W, H), fill=0)               # flat-ish underside
    layer = layer.filter(ImageFilter.GaussianBlur(9)).point(lambda v: int(v * 0.92))
    img = PILImage.new("RGBA", (W, H), (255, 255, 255, 255))
    img.putalpha(layer)
    return img



def _ui_tex(img):
    tx = Texture(img)
    try:
        tx.filtering = "bilinear"
    except Exception:
        pass
    return tx


SKY_STORM_TEX = _ui_tex(_gradient_image([(0, (12, 17, 24)), (0.5, (40, 52, 62)), (0.7, (92, 104, 112)), (1, (70, 80, 86))]))
SKY_CLEAR_TEX = _ui_tex(_gradient_image([(0, (14, 40, 70)), (0.40, (40, 106, 128)), (0.68, (255, 208, 140)), (1, (255, 190, 110))]))
HILLS_TEX = _ui_tex(_make_hills_image())
CLOUD_TEXS = [_ui_tex(_make_cloud_image(s)) for s in (11, 23, 37)]
SUN_GLOW_TEX = _create_radial_glow_texture(256, (255, 214, 120))
PLATE_TEX = _create_radial_glow_texture(256, (4, 9, 11))


class WeatherScene:
    """Animated painted-sky backdrop: storm <-> clear, rain, drifting clouds, sunrise,
    and (optionally) crop sprouts that grow. Everything lives under `parent`; call update() each frame.
    z0 pushes the whole scene backwards so the screen's own widgets stay in front."""

    HILLS_H = 0.30

    def __init__(self, parent, z0=0.0, n_clouds=7, n_rain=80, n_sprouts=9,
                 sun_x=-0.50, rainbow_x=0.30, plate=(0.0, -0.02, 1.15, 0.95), seed=1):
        rr = random.Random(seed)
        self.z0, self.sun_x, self.n_rain, self.n_sprouts = z0, sun_x, n_rain, n_sprouts
        E = lambda **kw: Entity(parent=parent, **kw)

        self.sky_storm = E(model="quad", texture=SKY_STORM_TEX, position=(0, 0, z0 + 0.045), scale=(4, 1.02))
        self.sky_clear = E(model="quad", texture=SKY_CLEAR_TEX, color=Color(1, 1, 1, 0),
                           position=(0, 0, z0 + 0.044), scale=(4, 1.02))
        self.sun_glow = E(model="quad", texture=SUN_GLOW_TEX, color=Color(1, 0.84, 0.47, 0),
                          position=(sun_x, 0, z0 + 0.042), scale=(0.95, 0.95))
        self.rays = [E(model="quad", origin=(0, -0.5), color=Color(1, 0.92, 0.62, 0),
                       position=(sun_x, 0, z0 + 0.041), scale=(0.018, 0.62), rotation_z=i * 30)
                     for i in range(12)]
        self.sun_core = E(model="circle", color=Color(1, 0.93, 0.68, 0),
                          position=(sun_x, 0, z0 + 0.040), scale=0.085)

        self.clouds = []
        for i in range(n_clouds):
            w = rr.uniform(0.55, 1.0)
            e = E(model="quad", texture=rr.choice(CLOUD_TEXS), color=Color(1, 1, 1, 0),
                  position=(0, 0, z0 + 0.035 - 0.001 * i), scale=(w, w * 0.5))
            self.clouds.append({"e": e, "x": rr.uniform(0, 3.2), "y": rr.uniform(0.10, 0.44), "w": w,
                                "v": rr.uniform(0.008, 0.022), "storm_only": i >= n_clouds - 3})

        self.drops = []
        for _ in range(n_rain):
            e = E(model="quad", color=Color(0.75, 0.85, 0.96, 0), scale=(0.0013, 0.03), rotation_z=10,
                  position=(0, 0, z0 + 0.025))
            e.enabled = False
            self.drops.append({"e": e, "fx": rr.random(), "sp": rr.uniform(0.9, 1.7), "ph": rr.random(), "on": False})

        self.hills = E(model="quad", texture=HILLS_TEX, position=(0, -0.5 + self.HILLS_H / 2, z0 + 0.020),
                       scale=(2.6, self.HILLS_H))

        self.sprouts = []
        for i in range(n_sprouts):
            x = -0.78 + i * (1.56 / max(1, n_sprouts - 1)) + rr.uniform(-0.02, 0.02)
            stem = E(model="quad", origin=(0, -0.5), color=Color(0.40, 0.78, 0.36, 0),
                     position=(x, -0.455 + rr.uniform(-0.012, 0.012), z0 + 0.015), scale=(0.0045, 0.0001))
            leaf_a = E(model="circle", color=Color(0.50, 0.90, 0.42, 0), position=(x, -0.45, z0 + 0.014), scale=(0.001, 0.001))
            leaf_b = E(model="circle", color=Color(0.50, 0.90, 0.42, 0), position=(x, -0.45, z0 + 0.014), scale=(0.001, 0.001))
            self.sprouts.append({"stem": stem, "a": leaf_a, "b": leaf_b, "x": x, "y": stem.y, "ph": rr.uniform(0, 6.28)})

        self.plate = E(model="quad", texture=PLATE_TEX, color=Color(1, 1, 1, 0),
                       position=(plate[0], plate[1], z0 + 0.008), scale=(plate[2], plate[3]))
        self.flash = E(model="quad", color=Color(0.85, 0.92, 1.0, 0), position=(0, 0, z0 - 0.002), scale=(4, 2))

    def update(self, clock, storm, rain, clear, rainbow, sun_h, growth, k, wind=1.0, plate_a=0.62):
        z0 = self.z0
        self.sky_storm.color = Color(1, 1, 1, k)
        self.sky_clear.color = Color(1, 1, 1, clear * k)
        self.hills.color = _mix((0.40, 0.46, 0.50), (1, 1, 1), clear, k)
        self.plate.color = Color(1, 1, 1, plate_a * k)

        # --- sun: rises from behind the hills as the sky clears ---
        sun_a = clear * _smooth(sun_h * 1.6) * k
        sy = -0.20 + sun_h * 0.50
        pulse = 0.5 + 0.5 * math.sin(clock * 1.7)
        self.sun_glow.position = (self.sun_x, sy, z0 + 0.042)
        self.sun_glow.scale = (0.95 + 0.06 * pulse, 0.95 + 0.06 * pulse)
        self.sun_glow.color = Color(1, 0.84, 0.47, 0.50 * sun_a)
        self.sun_core.position = (self.sun_x, sy, z0 + 0.040)
        self.sun_core.color = Color(1, 0.93, 0.68, sun_a)
        for i, r in enumerate(self.rays):
            r.position = (self.sun_x, sy, z0 + 0.041)
            r.rotation_z = i * 30 + clock * 4.0
            r.color = Color(1, 0.92, 0.62, (0.05 + 0.03 * math.sin(clock * 1.3 + i)) * sun_a)

        # --- clouds: drift, darken in a storm ---
        for c in self.clouds:
            a = k * (0.0 if c["storm_only"] and storm < 0.05 else 1.0)
            a *= (0.50 + 0.45 * storm) * (1.0 if not c["storm_only"] else storm)
            x = ((c["x"] + clock * c["v"] * wind) % 3.2) - 1.6
            sc = c["w"] * (1.0 + 0.30 * storm)
            c["e"].position = (x, c["y"] - 0.04 * storm, c["e"].z)
            c["e"].scale = (sc, sc * 0.5)
            c["e"].color = _mix((0.30, 0.34, 0.40), (0.97, 0.97, 1.0), 1.0 - storm, a)

        # --- rain ---
        n_on = int(rain * self.n_rain)
        for i, d in enumerate(self.drops):
            vis = i < n_on and k > 0.0
            if vis != d["on"]:
                d["on"] = vis
                d["e"].enabled = vis
            if vis:
                yv = (clock * 0.9 * d["sp"] + d["ph"]) % 1.0
                d["e"].position = (d["fx"] * 2.4 - 1.2 - yv * 0.05, 0.52 - yv * 0.80, z0 + 0.025)
                d["e"].color = Color(0.75, 0.85, 0.96, (0.22 + 0.28 * d["sp"] / 1.7) * k)

        # --- lightning: a rare, soft flash only while it is properly stormy ---
        ph = clock % 6.1
        fl = 0.0
        if storm > 0.55:
            if ph < 0.16:
                fl = 1.0 - ph / 0.16
            elif 0.26 < ph < 0.36:
                fl = 0.6 * (1.0 - (ph - 0.26) / 0.10)
        self.flash.color = Color(0.85, 0.92, 1.0, 0.10 * fl * storm * k)

        # --- sprouts grow with `growth` (0..1) and sway in the wind ---
        n = max(1, self.n_sprouts)
        for i, s in enumerate(self.sprouts):
            g = _smooth((growth - (i / n) * 0.55) / 0.35)
            vis = g > 0.01
            h = 0.010 + 0.075 * g
            ang = math.sin(clock * 1.4 * wind + s["ph"]) * 4.0 * g
            rad = math.radians(ang)
            tx, ty = s["x"] - h * math.sin(rad), s["y"] + h * math.cos(rad)
            a = (1.0 if vis else 0.0) * k
            s["stem"].rotation_z = ang
            s["stem"].scale = (0.0045, h)
            s["stem"].color = Color(0.40, 0.78, 0.36, a)
            lw, lh = 0.030 * g, 0.012 * g
            for leaf, sign in ((s["a"], -1), (s["b"], 1)):
                leaf.position = (tx + sign * lw * 0.45, ty, z0 + 0.014)
                leaf.scale = (max(0.0005, lw), max(0.0005, lh))
                leaf.rotation_z = sign * 25 + ang
                leaf.color = Color(0.50, 0.90, 0.42, a)


def _trap(x, a, b, c, d):
    """0 -> 1 between a..b, hold to c, 1 -> 0 between c..d (smooth)."""
    if x <= a or x >= d:
        return 0.0
    if x < b:
        return _smooth((x - a) / (b - a))
    if x <= c:
        return 1.0
    return 1.0 - _smooth((x - c) / (d - c))


def _calm_weather_cycle(clock, period=26.0):
    """Language screen: mostly sunny, a passing shower. Returns
    (storm, rain, clear, rainbow, sun_h)."""
    ph = (clock % period) / period
    storm = 0.65 * _trap(ph, 0.38, 0.52, 0.70, 0.84)
    rain = 0.75 * _trap(ph, 0.46, 0.56, 0.66, 0.76)
    rainbow = 0.9 * _trap(ph, 0.72, 0.82, 0.92, 1.0)
    sun_h = min(1.0 - 0.55 * (storm / 0.65), _smooth(clock / 1.6))
    return storm, rain, 1.0 - storm, rainbow, sun_h


# ============================================================
# LOADING SCREEN
# ============================================================

LOGO_PNG_B64 = ""
LOGO_FILE = "botaniq_logo.png"


def _load_logo_texture():
    if LOGO_PNG_B64:
        try:
            import base64, io
            img = PILImage.open(io.BytesIO(base64.b64decode("".join(LOGO_PNG_B64)))).convert("RGBA")
            return Texture(img)
        except Exception as e:
            print("Embedded logo failed:", e)
    here = os.path.dirname(os.path.abspath(__file__))
    for candidate in (LOGO_FILE, os.path.join(here, LOGO_FILE)):
        try:
            tex = load_texture(candidate)
            if tex is not None:
                return tex
        except Exception:
            pass
    return None


LOGO_TEX = _load_logo_texture()

LOADING_DURATION = 4.8
LOADING_FADE_TIME = 0.45
LOAD_BAR_W = 0.50
LOAD_BAR_Y = -0.235
LOAD_BAR_H = 0.012
LOGO_LOAD_Y = 0.085
LOGO_LOAD_SIZE = 0.25
LOAD_GREEN = Color(0.26, 0.78, 0.35, 1)
LOAD_GREEN_LIGHT = Color(0.62, 0.95, 0.55, 1)
LOAD_DIM = Color(0.14, 0.17, 0.15, 1)

loading_state = {"t": 0.0, "done": False, "active": False,
                 "fade_t": None, "clock": 0.0, "step": None, "pct": -1}
loading_root = Entity(parent=camera.ui, z=-0.20)
_load_fade = []

_fade_register(_load_fade, Entity(parent=loading_root, model="quad",
               color=Color(0.030, 0.042, 0.036, 1), scale=(4, 2), z=0.05))

# Animated weather backdrop: storm -> rain -> clearing -> sunrise, sprouts grow with progress
_load_scene = WeatherScene(loading_root, z0=0.0, n_clouds=7, n_rain=80, n_sprouts=9,
                           sun_x=-0.50, rainbow_x=0.30, plate=(0.0, -0.03, 1.10, 0.95), seed=3)

_load_motes = []
for _i in range(24):
    _sz = uniform(0.004, 0.011)
    _m = Entity(parent=loading_root, model="circle", color=Color(0.55, 0.95, 0.60, 0.0),
                scale=_sz, position=(0, 0, 0.012))
    _load_motes.append({"e": _m, "x": uniform(-0.8, 0.8), "y": uniform(0, 1.1),
                        "speed": uniform(0.02, 0.055), "phase": uniform(0, 6.28),
                        "sway": uniform(0.01, 0.035)})

loading_logo = None
if LOGO_TEX is not None:
    loading_logo = Entity(parent=loading_root, model="quad", texture=LOGO_TEX,
                          color=Color(1, 1, 1, 0), position=(0, LOGO_LOAD_Y, -0.005),
                          scale=LOGO_LOAD_SIZE)

_fade_register(_load_fade, Text("B O T A N I Q", parent=loading_root, position=(0, -0.115),
               origin=(0, 0), scale=2.0, color=GREEN))
loading_subtitle_text = _fade_register(_load_fade, Text(t("loading_subtitle"), parent=loading_root,
               position=(0, -0.165), origin=(0, 0), scale=0.75, color=TEXT_WHITE))

_bar_bg = Color(0.11, 0.14, 0.12, 1)
_fade_register(_load_fade, Entity(parent=loading_root, model="quad", color=_bar_bg,
               position=(0, LOAD_BAR_Y, 0), scale=(LOAD_BAR_W, LOAD_BAR_H)))
for _sx in (-1, 1):
    _fade_register(_load_fade, Entity(parent=loading_root, model="circle", color=_bar_bg,
                   position=(_sx * LOAD_BAR_W / 2, LOAD_BAR_Y, 0), scale=LOAD_BAR_H))
loading_bar = _fade_register(_load_fade, Entity(parent=loading_root, model="quad", color=LOAD_GREEN,
              origin=(-0.5, 0), position=(-LOAD_BAR_W / 2, LOAD_BAR_Y, -0.01),
              scale=(0.0001, LOAD_BAR_H)))
_fade_register(_load_fade, Entity(parent=loading_root, model="circle", color=LOAD_GREEN,
               position=(-LOAD_BAR_W / 2, LOAD_BAR_Y, -0.01), scale=LOAD_BAR_H))
loading_bar_head = _fade_register(_load_fade, Entity(parent=loading_root, model="circle",
                   color=LOAD_GREEN_LIGHT, position=(-LOAD_BAR_W / 2, LOAD_BAR_Y, -0.012),
                   scale=LOAD_BAR_H * 1.25))
loading_bar_glow = Entity(parent=loading_root, model="circle", color=Color(0.4, 0.95, 0.5, 0.0),
                          position=(-LOAD_BAR_W / 2, LOAD_BAR_Y, -0.011), scale=0.045)

loading_text = _fade_register(_load_fade, Text(t("loading_step_1"), parent=loading_root,
               position=(-LOAD_BAR_W / 2, LOAD_BAR_Y - 0.035), origin=(-0.5, 0),
               scale=0.62, color=TEXT_MUTED))
loading_percent_text = _fade_register(_load_fade, Text("0%", parent=loading_root,
               position=(LOAD_BAR_W / 2, LOAD_BAR_Y - 0.035), origin=(0.5, 0),
               scale=0.62, color=TEXT_WHITE))
_load_dots = []
for _i in range(4):
    _dot = Entity(parent=loading_root, model="circle", color=LOAD_DIM,
                  position=((_i - 1.5) * 0.028, LOAD_BAR_Y - 0.082, 0), scale=0.009)
    _fade_register(_load_fade, _dot)
    _load_dots.append(_dot)


def _loading_update(dt):
    st = loading_state
    dt = min(dt, 0.05)
    st["clock"] += dt
    clock = st["clock"]
    fading = st["fade_t"] is not None
    k = 1.0
    if fading:
        st["fade_t"] += dt
        k = 1.0 - st["fade_t"] / LOADING_FADE_TIME
    elif st["active"]:
        st["t"] += dt

    raw = min(1.0, st["t"] / LOADING_DURATION)
    p = _smooth(raw)
    pulse = 0.5 + 0.5 * math.sin(clock * 3.2)

    storm = 1.0 - _smooth((p - 0.20) / 0.55)
    clear = _smooth((p - 0.30) / 0.55)
    rain_amt = 0.95 * (1.0 - _smooth((p - 0.35) / 0.40))
    _load_scene.update(clock, storm, rain_amt, clear, _smooth((p - 0.72) / 0.22),
                       _smooth((p - 0.40) / 0.50), p, k, wind=1.0 + 1.5 * storm)

    if loading_logo is not None:
        intro = _smooth(clock / 0.7)
        size = LOGO_LOAD_SIZE * (0.86 + 0.14 * intro) * (1.0 + 0.012 * math.sin(clock * 2.0))
        loading_logo.scale = (size, size)
        v = 0.55 + 0.45 * p
        loading_logo.color = Color(v, v, v, intro * k)

    for m in _load_motes:
        y = -0.55 + ((m["y"] + clock * m["speed"]) % 1.1)
        x = m["x"] + math.sin(clock * 0.7 + m["phase"]) * m["sway"]
        edge = max(0.0, min(1.0, (y + 0.55) / 0.15, (0.55 - y) / 0.15))
        tw = 0.5 + 0.5 * math.sin(clock * 2.1 + m["phase"])
        m["e"].position = (x, y, 0.012)
        m["e"].color = Color(0.55, 0.95, 0.60, (0.05 + 0.30 * tw) * edge * k * (0.25 + 0.75 * clear))

    w = LOAD_BAR_W * p
    loading_bar.scale_x = max(0.0001, w)
    head_x = -LOAD_BAR_W / 2 + w
    loading_bar_head.x = head_x
    loading_bar_glow.x = head_x
    loading_bar_glow.color = Color(0.4, 0.95, 0.5, (0.10 + 0.12 * pulse) * k * (1.0 if p > 0.01 else 0.0))

    pct = int(p * 100)
    if pct != st["pct"]:
        st["pct"] = pct
        loading_percent_text.text = f"{pct}%"

    step = 0 if p < 0.25 else 1 if p < 0.55 else 2 if p < 0.85 else 3
    if step != st["step"]:
        st["step"] = step
        loading_text.text = t(f"loading_step_{step + 1}")
        for i, d in enumerate(_load_dots):
            d.color = LOAD_GREEN if i <= step else LOAD_DIM

    if fading:
        _fade_apply(_load_fade, k)
        if k <= 0.0:
            st["done"] = True
            destroy(loading_root)
    elif st["active"] and raw >= 1.0:
        st["fade_t"] = 0.0


# ============================================================
# LANGUAGE SELECTION SCREEN (FIXED LAYOUT & SMOOTH RADIAL GLOW)
# ============================================================

LANG_OPTIONS = (
    {"code": "en",  "badge": "EN",  "name": "English", "desc": "Use the app in English", "key": "1"},
    {"code": "fil", "badge": "FIL", "name": "Filipino", "desc": "Gamitin sa Filipino",   "key": "2"},
)
LANG_CARD_W, LANG_CARD_H, LANG_CARD_Y, LANG_CARD_GAP = 0.36, 0.32, -0.07, 0.44
LANG_FADE_TIME = 0.30

LANG_CARD_BG = Color(0.12, 0.14, 0.15, 1)
LANG_CARD_HOVER = Color(0.16, 0.20, 0.18, 1)
OVERLAY_BG = Color(0.05, 0.06, 0.07, 1.0)

lang_state = {"open": True, "closing": None, "picked": None, "intro": 0.0}
language_root = Entity(parent=camera.ui, z=-0.9)
_lang_fade = []
_lang_cards = []

_fade_register(_lang_fade, Entity(parent=language_root, model="quad",
               color=OVERLAY_BG, scale=(4, 2), z=0.1, collider="box"))

# Living weather backdrop (sunny, with a passing shower every ~26 s)
_lang_scene = WeatherScene(language_root, z0=0.05, n_clouds=6, n_rain=70, n_sprouts=9,
                           sun_x=-0.52, rainbow_x=0.32, plate=(0.0, 0.10, 1.15, 0.80), seed=7)

if LOGO_TEX is not None:
    _fade_register(_lang_fade, Entity(parent=language_root, model="quad", texture=LOGO_TEX,
                   color=Color(1, 1, 1, 1), position=(0, 0.29, -0.02), scale=0.14))
else:
    # Title: no letter-spacing, larger, bright green with a dark outline + drop shadow so it stays crisp on the sky
    _TITLE_Y, _TITLE_SCALE = 0.298, 2.5
    for _dx, _dy in ((-0.0028, 0), (0.0028, 0), (0, 0.0028), (0, -0.0028),
                     (-0.002, 0.002), (0.002, 0.002), (-0.002, -0.002), (0.002, -0.002)):
        _fade_register(_lang_fade, Text("BOTANIQ", parent=language_root, position=(_dx, _TITLE_Y + _dy, -0.015),
                       origin=(0, 0), scale=_TITLE_SCALE, color=Color(0.02, 0.07, 0.06, 1)))
    _fade_register(_lang_fade, Text("BOTANIQ", parent=language_root, position=(0.005, _TITLE_Y - 0.007, -0.016),
                   origin=(0, 0), scale=_TITLE_SCALE, color=Color(0, 0, 0, 0.45)))
    _fade_register(_lang_fade, Text("BOTANIQ", parent=language_root, position=(0, _TITLE_Y, -0.02),
                   origin=(0, 0), scale=_TITLE_SCALE, color=Color(0.40, 0.92, 0.50, 1)))

# Fixed non-overlapping text positions
_fade_register(_lang_fade, Text("Select Language / Pumili ng Wika", parent=language_root, position=(0, 0.175, -0.02),
               origin=(0, 0), scale=1.2, color=TEXT_WHITE))
_fade_register(_lang_fade, Text("Choose your preferred language for the interface", parent=language_root, position=(0, 0.132, -0.02),
               origin=(0, 0), scale=0.7, color=Color(0.82, 0.88, 0.88, 1)))
_fade_register(_lang_fade, Text("Press 1 or 2 to quickly select", parent=language_root,
               position=(0, -0.34, -0.02), origin=(0, 0), scale=0.6, color=Color(0.85, 0.90, 0.88, 1)))


def _make_hover(entry, state):
    def _handler():
        entry["hover"] = state
    return _handler


def _build_lang_card(opt, cx):
    cy = LANG_CARD_Y
    W, H = LANG_CARD_W, LANG_CARD_H

    shadow = Entity(parent=language_root, model="quad", color=Color(0, 0, 0, 0.45),
                    position=(cx + 0.008, cy - 0.008, 0.03), scale=(W + 0.01, H + 0.01))
    border = Entity(parent=language_root, model="quad", color=BORDER_COL,
                    position=(cx, cy, 0.02), scale=(W + 0.005, H + 0.005))
    card = Entity(parent=language_root, model="quad", color=LANG_CARD_BG,
                  position=(cx, cy, 0.01), scale=(W, H), collider="box")
    
    badge_bg = Entity(parent=language_root, model="quad", color=Color(0.16, 0.22, 0.18, 1),
                      position=(cx, cy + 0.065, -0.005), scale=(0.11, 0.06))
    _fade_register(_lang_fade, badge_bg)
    _fade_register(_lang_fade, Text(opt["badge"], parent=language_root, position=(cx, cy + 0.065, -0.01),
                   origin=(0, 0), scale=1.1, color=GREEN))

    _fade_register(_lang_fade, Text(opt["name"], parent=language_root, position=(cx, cy - 0.015, -0.01),
                   origin=(0, 0), scale=1.2, color=TEXT_WHITE))
    _fade_register(_lang_fade, Text(opt["desc"], parent=language_root, position=(cx, cy - 0.060, -0.01),
                   origin=(0, 0), scale=0.62, color=TEXT_MUTED))

    key_badge = Entity(parent=language_root, model="quad", color=Color(0.20, 0.22, 0.24, 1),
                       position=(cx, cy - 0.108, -0.005), scale=(0.035, 0.028))
    _fade_register(_lang_fade, key_badge)
    _fade_register(_lang_fade, Text(opt["key"], parent=language_root, position=(cx, cy - 0.108, -0.01),
                   origin=(0, 0), scale=0.7, color=TEXT_WHITE))

    entry = {
        "code": opt["code"], "card": card, "border": border, "shadow": shadow,
        "hover": False, "amt": 0.0
    }
    card.on_mouse_enter = _make_hover(entry, True)
    card.on_mouse_exit = _make_hover(entry, False)
    card.on_click = Func(_pick_language, opt["code"])
    _lang_cards.append(entry)


def _pick_language(code):
    if lang_state["closing"] is not None:
        return
    lang_state["picked"] = code
    lang_state["closing"] = 0.0
    for c in _lang_cards:
        try:
            c["card"].collider = None
        except Exception:
            pass


def _choose_language(code):
    LANG["code"] = code
    lang_state["open"] = False
    destroy(language_root)
    loading_state["active"] = True
    loading_state["step"] = None
    loading_subtitle_text.text = t("loading_subtitle")
    rebuild_ui_safely()
    set_bar_message(t("waiting_params"))


def _lang_update(dt):
    if not lang_state["open"]:
        return
    dt = min(dt, 0.05)
    lang_state["intro"] += dt
    k = _smooth(lang_state["intro"] / 0.5)
    closing = lang_state["closing"]
    if closing is not None:
        lang_state["closing"] += dt
        k = min(k, 1.0 - lang_state["closing"] / LANG_FADE_TIME)
    picked = lang_state["picked"]

    for c in _lang_cards:
        target = 1.0 if (c["hover"] or picked == c["code"]) else 0.0
        c["amt"] += (target - c["amt"]) * min(1.0, dt * 12)
        a = c["amt"]
        kk = k * (0.35 if (picked is not None and picked != c["code"]) else 1.0)
        c["border"].color = _mix(BORDER_COL, GREEN, a, kk)
        c["card"].color = _mix(LANG_CARD_BG, LANG_CARD_HOVER, a, kk)
    _fade_apply(_lang_fade, k)
    _s, _r, _c, _rb, _sh = _calm_weather_cycle(lang_state["intro"])
    _lang_scene.update(lang_state["intro"], _s, _r, _c, _rb, _sh, 1.0, k, wind=1.0 + _r, plate_a=0.55)

    if closing is not None and k <= 0.0:
        _choose_language(picked)


for _n, _opt in enumerate(LANG_OPTIONS):
    _build_lang_card(_opt, (_n - 0.5) * LANG_CARD_GAP)


# ============================================================
# MAIN LOOP HOOKS
# ============================================================

def input(key):
    global _last_window_size
    if key == "window_resize":
        _last_window_size = [window.size.x, window.size.y]
        rebuild_ui_safely()
        return
    if lang_state["open"]:
        if lang_state["closing"] is None:
            if key in ("1", "e"):
                _pick_language("en")
            elif key in ("2", "f"):
                _pick_language("fil")
        return


def update():
    global _last_window_size
    dt = min(time.dt, 0.05)

    _lang_update(time.dt)
    if not loading_state["done"]:
        _loading_update(time.dt)

    current_size = [window.size.x, window.size.y]
    if current_size != _last_window_size:
        _last_window_size = current_size
        rebuild_ui_safely()

    if lang_state["open"]:
        return

    SIM.update(dt)
    _live_tick()
    _poll_inputs()
    _style_input_fields()
    _fit_input_texts()

    _sim_clock["t"] += dt
    _sim_clock["accum"] += dt
    if _sim_clock["accum"] >= 1.0 / SIM_FPS:
        _sim_clock["accum"] = 0.0
        _render_sim_frame()

    _sim_ui_update()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    app.run()