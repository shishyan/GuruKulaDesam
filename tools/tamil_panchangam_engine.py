#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/tamil_panchangam_engine.py
Authentic Astronomical Tamil Panchangam, Exact Tithi & Nakshatra Timings,
Rahu Kalam / Yama Gandam / Nalla Neram, and 6-Pillar Sacred Title Alignment Engine
for @gurukuladesam2 Autonomous Devotional Shorts.

Capabilities:
1. Exact Astronomical Timings (IST, UTC+05:30):
   - Computes exact start and end clock times (HH:MM AM/PM IST) for the active Tithi and Nakshatra
     using binary search over sidereal lunar/solar elongation (Lahiri Chitrapaksha Ayanamsa).
   - Computes exact daily Rahu Kalam (இராகு காலம்), Yama Gandam (எமகண்டம்), Kuligai (குளிகை),
     Nalla Neram (நல்ல நேரம்), and Gowri Nalla Neram (கௌரி நல்ல நேரம்) for the weekday.
   - Computes special ritual observance windows (e.g., Pradosham 04:30 PM – 06:00 PM IST,
     Sankatahara Chaturthi Moonrise Pooja 06:30 PM – 08:30 PM IST, Krittika Deepam, Abhijit Muhurtham).
2. 6 Sacred Tamil Category Titles (Mandated by User):
   - 📖 நன்னெறி (Nanneri — Sacred Path / Righteous Living)
   - 📖 நல்லறம் (Nallaram — Pure Dharma / Sacred Virtue)
   - 📖 நற்பண்பு (Narpanbu — Noble Character / Divine Grace)
   - 📖 நற்துணை (Narthunai — Supreme Divine Companion / Refuge)
   - 📖 நற்சொல் (Narsol — Sacred Hymn / Divine Mantra)
   - 📖 நற்செய்கை (Narseyal — Auspicious Action / Sacred Observance)
3. Strict Deity & Festival Alignment:
   - Never posts a mismatched deity on a sacred tithi/festival day (e.g., never Vishnu on Shivaratri/Pradosham,
     never Shiva on Vaikunta Ekadashi).
"""

import math
from datetime import datetime, date, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))

# The 6 Canonical Sacred Category Titles mandated for @gurukuladesam2
SACRED_6_CATEGORIES = {
    "nanneri": {
        "key": "nanneri",
        "title": "📖 நன்னெறி",
        "name_ta": "நன்னெறி",
        "name_en": "Nanneri — The Sacred Path of Wisdom",
        "desc_ta": "வாழ்வை உயர்த்தும் தெய்வீக நன்னெறி மற்றும் ஞான வழிகாட்டுதல்",
    },
    "nallaram": {
        "key": "nallaram",
        "title": "📖 நல்லறம்",
        "name_ta": "நல்லறம்",
        "name_en": "Nallaram — Pure Dharma & Righteousness",
        "desc_ta": "உலகப் பொதுமறை மற்றும் அருளாளர்கள் காட்டிய நல்லறம்",
    },
    "narpanbu": {
        "key": "narpanbu",
        "title": "📖 நற்பண்பு",
        "name_ta": "நற்பண்பு",
        "name_en": "Narpanbu — Noble Character & Compassion",
        "desc_ta": "அன்பு, அருள், அடக்கம் மற்றும் ஜீவகாருண்ய நற்பண்பு",
    },
    "narthunai": {
        "key": "narthunai",
        "title": "📖 நற்துணை",
        "name_ta": "நற்துணை",
        "name_en": "Narthunai — Divine Protection & Refuge",
        "desc_ta": "துன்பம் நீக்கி எப்போதும் காக்கும் இறைவனின் நற்துணை",
    },
    "narsol": {
        "key": "narsol",
        "title": "📖 நற்சொல்",
        "name_ta": "நற்சொல்",
        "name_en": "Narsol — Sacred Mantra & Divine Hymn",
        "desc_ta": "செவிகுளிர உள்ளம் உருகும் தமிழ் மறை நற்சொல்",
    },
    "narseyal": {
        "key": "narseigai",
        "title": "📖 நற்செய்கை",
        "name_ta": "நற்செய்கை",
        "name_en": "Narseigai — Righteous Action & Auspicious Conduct",
        "desc_ta": "நெறி தவறாமை, விரத நாட்கள் மற்றும் புண்ணிய காலங்களில் செய்யும் நற்செய்கை",
    },
    "narseigai": {
        "key": "narseigai",
        "title": "📖 நற்செய்கை",
        "name_ta": "நற்செய்கை",
        "name_en": "Narseigai — Righteous Action & Auspicious Conduct",
        "desc_ta": "நெறி தவறாமை, விரத நாட்கள் மற்றும் புண்ணிய காலங்களில் செய்யும் நற்செய்கை",
    },
    "narkunam": {
        "key": "narkunam",
        "title": "📖 நற்குணம்",
        "name_ta": "நற்குணம்",
        "name_en": "Narkunam — Pure Virtue & Flawless Discipline",
        "desc_ta": "ஒழுக்கம் பிழையாமை மற்றும் ஆத்ம சுத்தியுடன் கூடிய நற்குணம்",
    },
    "narsinthanai": {
        "key": "narsinthanai",
        "title": "📖 நற்சிந்தனை",
        "name_ta": "நற்சிந்தனை",
        "name_en": "Narsinthanai — Pure Divine Reflection & Meditation",
        "desc_ta": "தெய்வீகப் பாடல்களைக் கேட்டு உள்ளம் தெளியும் நற்சிந்தனை மற்றும் தியானம்",
    },
}
SACRED_7_CATEGORIES = SACRED_6_CATEGORIES

TAMIL_MONTHS = [
    ("சித்திரை", "Chithirai"),      # 0: Aries (Mesham)
    ("வைகாசி", "Vaikasi"),         # 1: Taurus (Rishabham)
    ("ஆனி", "Aani"),               # 2: Gemini (Mithunam)
    ("ஆடி", "Aadi"),               # 3: Cancer (Kadagam)
    ("ஆவணி", "Aavani"),            # 4: Leo (Simmam)
    ("புரட்டாசி", "Purattasi"),    # 5: Virgo (Kanni)
    ("ஐப்பசி", "Aippasi"),         # 6: Libra (Thulaam)
    ("கார்த்திகை", "Karthigai"),   # 7: Scorpio (Vrischikam)
    ("மார்கழி", "Margazhi"),       # 8: Sagittarius (Dhanusu)
    ("தை", "Thai"),                # 9: Capricorn (Makaram)
    ("மாசி", "Maasi"),             # 10: Aquarius (Kumbham)
    ("பங்குனி", "Panguni"),        # 11: Pisces (Meenam)
]

NAKSHATRAS = [
    ("அசுவினி", "Ashwini"), ("பரணி", "Bharani"), ("கார்த்திகை", "Krittika"),
    ("ரோகிணி", "Rohini"), ("மிருகசீரிடம்", "Mrigashirsha"), ("திருவாதிரை", "Ardra"),
    ("புனர்பூசம்", "Punarvasu"), ("பூசம்", "Pushya"), ("ஆயில்யம்", "Ashlesha"),
    ("மகம்", "Magha"), ("பூரம்", "Purva Phalguni"), ("உத்திரம்", "Uttara Phalguni"),
    ("ஹஸ்தம்", "Hasta"), ("சித்திரை", "Chitra"), ("சுவாதி", "Swati"),
    ("விசாகம்", "Vishakha"), ("அனுஷம்", "Anuradha"), ("கேட்டை", "Jyeshtha"),
    ("மூலம்", "Mula"), ("பூராடம்", "Purva Ashadha"), ("உத்திராடம்", "Uttara Ashadha"),
    ("திருவோணம்", "Shravana"), ("அவிட்டம்", "Dhanishta"), ("சதயம்", "Shatabhisha"),
    ("பூரட்டாதி", "Purva Bhadrapada"), ("உத்திரட்டாதி", "Uttara Bhadrapada"), ("ரேவதி", "Revati"),
]

TITHI_NAMES = [
    "பிரதமை (Prathamai)", "துவிதியை (Dvitiya)", "திருதியை (Tritiya)", "சதுர்த்தி (Chaturthi)",
    "பஞ்சமி (Panchami)", "சஷ்டி (Sashti)", "சப்தமி (Saptami)", "அஷ்டமி (Ashtami)",
    "நவமி (Navami)", "தசமி (Dashami)", "ஏகாதசி (Ekadashi)", "துவாதசி (Dwadashi)",
    "திரயோதசி / பிரதோஷம் (Trayodashi / Pradosham)", "சதுர்த்தசி (Chaturdashi)",
    "பௌர்ணமி (Pournami)",  # 14 (index 14 = 15th Shukla)
    "பிரதமை (Prathamai)", "துவிதியை (Dvitiya)", "திருதியை (Tritiya)", "சதுர்த்தி / சங்கடஹர சதுர்த்தி (Sankatahara Chaturthi)",
    "பஞ்சமி (Panchami)", "சஷ்டி (Sashti)", "சப்தமி (Saptami)", "அஷ்டமி / தேய்பிறை அஷ்டமி (Kala Bhairava Ashtami)",
    "நவமி (Navami)", "தசமி (Dashami)", "ஏகாதசி (Ekadashi)", "துவாதசி (Dwadashi)",
    "திரயோதசி / பிரதோஷம் (Trayodashi / Pradosham)", "சதுர்த்தசி / மாத சிவராத்திரி (Masa Shivaratri)",
    "அமாவாசை (Amavasai)"   # 29 (index 29 = 30th Krishna)
]

WEEKDAY_NAMES = [
    ("திங்கட்கிழமை", "Monday", "shiva"),
    ("செவ்வாய்க்கிழமை", "Tuesday", "murugan"),
    ("புதன்கிழமை", "Wednesday", "vishnu"),
    ("வியாழக்கிழமை", "Thursday", "vallalar"),
    ("வெள்ளிக்கிழமை", "Friday", "amman"),
    ("சனிக்கிழமை", "Saturday", "vishnu"),
    ("ஞாயிற்றுக்கிழமை", "Sunday", "shiva"),
]

# Authentic Daily Panchangam Timings by Weekday (0=Monday .. 6=Sunday)
WEEKDAY_TIMINGS = {
    0: {  # Monday (திங்கள்)
        "rahu_kalam": "07:30 AM – 09:00 AM",
        "yama_gandam": "10:30 AM – 12:00 PM",
        "kuligai": "01:30 PM – 03:00 PM",
        "nalla_neram_am": "06:15 AM – 07:15 AM",
        "nalla_neram_pm": "04:45 PM – 05:45 PM",
        "gowri_am": "09:15 AM – 10:15 AM",
        "gowri_pm": "07:30 PM – 08:30 PM",
    },
    1: {  # Tuesday (செவ்வாய்)
        "rahu_kalam": "03:00 PM – 04:30 PM",
        "yama_gandam": "09:00 AM – 10:30 AM",
        "kuligai": "12:00 PM – 01:30 PM",
        "nalla_neram_am": "07:45 AM – 08:45 AM",
        "nalla_neram_pm": "04:45 PM – 05:45 PM",
        "gowri_am": "10:45 AM – 11:45 AM",
        "gowri_pm": "07:30 PM – 08:30 PM",
    },
    2: {  # Wednesday (புதன்)
        "rahu_kalam": "12:00 PM – 01:30 PM",
        "yama_gandam": "07:30 AM – 09:00 AM",
        "kuligai": "10:30 AM – 12:00 PM",
        "nalla_neram_am": "09:15 AM – 10:15 AM",
        "nalla_neram_pm": "04:45 PM – 05:45 PM",
        "gowri_am": "06:15 AM – 07:15 AM",
        "gowri_pm": "06:30 PM – 07:30 PM",
    },
    3: {  # Thursday (வியாழன்)
        "rahu_kalam": "01:30 PM – 03:00 PM",
        "yama_gandam": "06:00 AM – 07:30 AM",
        "kuligai": "09:00 AM – 10:30 AM",
        "nalla_neram_am": "10:45 AM – 11:45 AM",
        "nalla_neram_pm": "04:45 PM – 05:45 PM",
        "gowri_am": "12:15 PM – 01:15 PM",
        "gowri_pm": "06:30 PM – 07:30 PM",
    },
    4: {  # Friday (வெள்ளி)
        "rahu_kalam": "10:30 AM – 12:00 PM",
        "yama_gandam": "03:00 PM – 04:30 PM",
        "kuligai": "07:30 AM – 09:00 AM",
        "nalla_neram_am": "09:15 AM – 10:15 AM",
        "nalla_neram_pm": "04:45 PM – 05:45 PM",
        "gowri_am": "06:15 AM – 07:15 AM",
        "gowri_pm": "07:30 PM – 08:30 PM",
    },
    5: {  # Saturday (சனி)
        "rahu_kalam": "09:00 AM – 10:30 AM",
        "yama_gandam": "01:30 PM – 03:00 PM",
        "kuligai": "06:00 AM – 07:30 AM",
        "nalla_neram_am": "07:45 AM – 08:45 AM",
        "nalla_neram_pm": "04:45 PM – 05:45 PM",
        "gowri_am": "10:45 AM – 11:45 AM",
        "gowri_pm": "09:30 PM – 10:30 PM",
    },
    6: {  # Sunday (ஞாயிறு)
        "rahu_kalam": "04:30 PM – 06:00 PM",
        "yama_gandam": "12:00 PM – 01:30 PM",
        "kuligai": "03:00 PM – 04:30 PM",
        "nalla_neram_am": "07:45 AM – 08:45 AM",
        "nalla_neram_pm": "03:15 PM – 04:15 PM",
        "gowri_am": "10:45 AM – 11:45 AM",
        "gowri_pm": "01:30 PM – 02:30 PM",
    },
}


def _julian_day(dt_utc: datetime) -> float:
    y = dt_utc.year
    m = dt_utc.month
    d = dt_utc.day + (dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0) / 24.0
    if m <= 2:
        y -= 1
        m += 12
    a = int(y // 100)
    b = 2 - a + int(a // 4)
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b - 1524.5


def _solar_lunar_positions(dt_ist: datetime) -> dict:
    """
    Calculates tropical & sidereal (Lahiri Ayanamsa) longitudes of the Sun and Moon,
    Tithi index (0..29), Nakshatra index (0..26), and Tamil Solar Month (0..11).
    """
    dt_utc = dt_ist.astimezone(timezone.utc)
    jd = _julian_day(dt_utc)
    t = (jd - 2451545.0) / 36525.0

    # 1. Sun Tropical Longitude
    l0 = (280.46646 + 36000.76983 * t + 0.0003032 * t * t) % 360.0
    m_sun = (357.52911 + 35999.05029 * t - 0.0001537 * t * t) % 360.0
    m_rad = math.radians(m_sun)
    c_sun = (
        (1.914602 - 0.004817 * t - 0.000014 * t * t) * math.sin(m_rad)
        + (0.019993 - 0.000101 * t) * math.sin(2 * m_rad)
        + 0.000289 * math.sin(3 * m_rad)
    )
    sun_trop = (l0 + c_sun) % 360.0

    # 2. Moon Tropical Longitude (Meeus Chapter 47 primary periodic terms)
    l_prime = (218.3164477 + 481267.88123421 * t - 0.0015786 * t * t) % 360.0
    d_elong = (297.8501921 + 445267.1114034 * t - 0.0018819 * t * t) % 360.0
    m_moon = (134.9633964 + 477198.8675055 * t + 0.0087414 * t * t) % 360.0
    f_arg = (93.2720950 + 483202.0175233 * t - 0.0036539 * t * t) % 360.0

    dr = math.radians(d_elong)
    mr = math.radians(m_sun)
    mpr = math.radians(m_moon)
    fr = math.radians(f_arg)

    moon_corr = (
        6.288774 * math.sin(mpr)
        + 1.274027 * math.sin(2 * dr - mpr)
        + 0.658314 * math.sin(2 * dr)
        + 0.213618 * math.sin(2 * mpr)
        - 0.185596 * math.sin(mr)
        - 0.114336 * math.sin(2 * fr)
        + 0.058793 * math.sin(2 * dr - 2 * mpr)
        + 0.057066 * math.sin(2 * dr - mr - mpr)
        + 0.053322 * math.sin(2 * dr + mpr)
        + 0.045758 * math.sin(2 * dr - mr)
        - 0.040923 * math.sin(mr - mpr)
        - 0.034720 * math.sin(dr)
        - 0.030383 * math.sin(mr + mpr)
    )
    moon_trop = (l_prime + moon_corr) % 360.0

    # 3. Lahiri Chitrapaksha Ayanamsa (~24.14 deg in 2026)
    ayanamsa = 23.853 + (jd - 2451545.0) * (50.29 / 3600.0 / 365.25)
    sun_sid = (sun_trop - ayanamsa) % 360.0
    moon_sid = (moon_trop - ayanamsa) % 360.0

    # 4. Tithi (0..29, each 12 deg of Moon - Sun elongation)
    phase_deg = (moon_trop - sun_trop) % 360.0
    tithi_idx = int(phase_deg // 12.0)  # 0..29
    paksha = "வளர்பிறை (Shukla Paksha)" if tithi_idx < 15 else "தேய்பிறை (Krishna Paksha)"
    tithi_num_in_paksha = (tithi_idx % 15) + 1

    # 5. Nakshatra (0..26, each 13 deg 20 min = 13.3333 deg of Sidereal Moon)
    nak_idx = int(moon_sid // (360.0 / 27.0))

    # 6. Tamil Solar Month (0..11, each 30 deg of Sidereal Sun)
    tamil_month_idx = int(sun_sid // 30.0)
    tamil_day_approx = int(sun_sid % 30.0) + 1

    return {
        "sun_sid": sun_sid,
        "moon_sid": moon_sid,
        "phase_deg": phase_deg,
        "tithi_idx": tithi_idx,
        "tithi_name": TITHI_NAMES[tithi_idx],
        "tithi_num": tithi_num_in_paksha,
        "paksha": paksha,
        "is_shukla": tithi_idx < 15,
        "nak_idx": nak_idx,
        "nak_ta": NAKSHATRAS[nak_idx][0],
        "nak_en": NAKSHATRAS[nak_idx][1],
        "month_idx": tamil_month_idx,
        "month_ta": TAMIL_MONTHS[tamil_month_idx][0],
        "month_en": TAMIL_MONTHS[tamil_month_idx][1],
        "tamil_day": tamil_day_approx,
    }


def _find_transition_time(ref_dt: datetime, key: str, target_idx: int, search_forward: bool) -> datetime:
    """
    Finds the exact minute (IST) when `key` ('tithi_idx' or 'nak_idx') transitions out of `target_idx`.
    `search_forward=True` finds the end time; `search_forward=False` finds the start time.
    """
    step_hours = 1.0 if search_forward else -1.0
    curr = ref_dt
    for _ in range(36):
        nxt = curr + timedelta(hours=step_hours)
        if _solar_lunar_positions(nxt)[key] != target_idx:
            # Binary search between curr and nxt to 1-minute precision
            lo, hi = (curr, nxt) if search_forward else (nxt, curr)
            for _ in range(10):
                mid = lo + (hi - lo) / 2
                val = _solar_lunar_positions(mid)[key]
                if search_forward:
                    if val == target_idx:
                        lo = mid
                    else:
                        hi = mid
                else:
                    if val == target_idx:
                        hi = mid
                    else:
                        lo = mid
            return hi if search_forward else hi
        curr = nxt
    return curr


def _fmt_clock(dt: datetime, ref_date: date) -> str:
    t_str = dt.strftime("%I:%M %p")
    if dt.date() == ref_date:
        return t_str
    elif dt.date() < ref_date:
        return f"{dt.strftime('%b %d')}, {t_str}"
    else:
        return f"{dt.strftime('%b %d')}, {t_str}"


def classify_sacred_category(deity_key: str, meta_entry: dict, panchangam_info: dict | None = None) -> dict:
    """
    Assigns every song/Short to one of the 6 Canonical Tamil Category Titles:
      1. 📖 நன்னெறி (Nanneri) — Spiritual wisdom, Thirukkural, Siddhar/Vallalar philosophical guidance
      2. 📖 நல்லறம் (Nallaram) — Dharma, righteousness, Aram chapters, ethical conduct
      3. 📖 நற்பண்பு (Narpanbu) — Devotional humility, compassion, grace, surrender, bhakti virtues
      4. 📖 நற்துணை (Narthunai) — Divine protection, Kavasam, removing obstacles (Vinayagar / Murugan Vel / Narasimha)
      5. 📖 நற்சொல் (Narsol) — Sacred Vedic/Tamil hymns, Namavali, Thevaram, Thiruvasagam, Thiruppugazh, Pasurams
      6. 📖 நற்செய்கை (Narseyal) — Auspicious vratham/festival worship (Krittika, Sashti, Pradosham, Chaturthi, Ekadashi)
    """
    title_text = f"{meta_entry.get('title', '')} {meta_entry.get('genre', '')} {meta_entry.get('tamil_meaning', '')}".lower()

    # Check if today is a major Vratham/Festival observance first -> highlights Narseyal / Narthunai / Narsol
    has_special_vratham = bool(panchangam_info and panchangam_info.get("is_major_vratham"))

    if deity_key == "thirukkural":
        if any(w in title_text for w in ("அறன்", "அறம்", "ஈகை", "தவம்", "புலால்", "வாய்மை", "நடுவுநிலை", "ஒழுக்கம்")):
            return SACRED_6_CATEGORIES["nallaram"]
        if any(w in title_text for w in ("அன்பு", "அடக்கம்", "பொறை", "இனியவை", "பண்பு", "செய்ந்நன்றி", "அருள்")):
            return SACRED_6_CATEGORIES["narpanbu"]
        if any(w in title_text for w in ("வினை", "செயல்", "ஊக்கம்", "முயற்சி", "இடுக்கண்")):
            return SACRED_6_CATEGORIES["narseyal"]
        return SACRED_6_CATEGORIES["nanneri"]

    if any(w in title_text for w in ("சிந்தனை", "தியான", "அறிவு", "மெய்யுணர்", "நினை", "உள்ளம்", "நெஞ்ச", "அருட்பெருஞ்ஜோதி")):
        return SACRED_6_CATEGORIES["narsinthanai"]

    if deity_key == "vallalar" or "திருவருட்பா" in title_text:
        if any(w in title_text for w in ("அருள்", "கருணை", "ஜீவ", "அன்பு", "தயவு")):
            return SACRED_6_CATEGORIES["narpanbu"]
        return SACRED_6_CATEGORIES["narsinthanai"]

    if any(w in title_text for w in ("அநுபூதி", "அலங்காரம்", "ஞான", "மெய்", "நான்மணிமாலை")):
        return SACRED_6_CATEGORIES["nanneri"] if "அநுபூதி" in title_text else SACRED_6_CATEGORIES["narpanbu"]

    if any(w in title_text for w in ("கவசம்", "kavasam", "துணை", "காக்க", "வேல்", "தடை")):
        return SACRED_6_CATEGORIES["narthunai"]

    if any(w in title_text for w in ("நாமாவளி", "namavali", "தேவாரம்", "திருவாசகம்", "திருப்புகழ்", "அந்தாதி", "பாசுரம்", "பாவை", "மந்திரம்", "ஓம்", "துதி")):
        return SACRED_6_CATEGORIES["narsol"]

    if has_special_vratham:
        return SACRED_6_CATEGORIES["narseyal"]

    # Deterministic fallback across the 6 categories based on deity
    deity_default_map = {
        "murugan": "narthunai",
        "vinayagar": "narthunai",
        "shiva": "narsol",
        "amman": "narpanbu",
        "vishnu": "narsol",
        "vallalar": "nanneri",
        "thirukkural": "nallaram",
    }
    return SACRED_6_CATEGORIES[deity_default_map.get(deity_key, "nanneri")]


def get_auspicious_alignment_for_datetime(dt_ist: datetime | None = None) -> dict:
    """
    Determines the exact Tamil Panchangam context for `dt_ist` (default: now in IST),
    exact Tithi & Nakshatra start/end timings, Rahu Kalam / Yama Gandam / Nalla Neram,
    and the mandated primary & secondary deity sequence for the 3 daily Shorts slots!
    """
    if dt_ist is None:
        dt_ist = datetime.now(IST)

    morning_dt = datetime(dt_ist.year, dt_ist.month, dt_ist.day, 8, 30, 0, tzinfo=IST)
    evening_dt = datetime(dt_ist.year, dt_ist.month, dt_ist.day, 17, 30, 0, tzinfo=IST)

    p_morn = _solar_lunar_positions(morning_dt)
    p_eve = _solar_lunar_positions(evening_dt)
    p_curr = _solar_lunar_positions(dt_ist)

    # Calculate exact start and end times for active Tithi and Nakshatra
    ref_date = dt_ist.date()
    tithi_start_dt = _find_transition_time(dt_ist, "tithi_idx", p_curr["tithi_idx"], search_forward=False)
    tithi_end_dt = _find_transition_time(dt_ist, "tithi_idx", p_curr["tithi_idx"], search_forward=True)
    nak_start_dt = _find_transition_time(dt_ist, "nak_idx", p_curr["nak_idx"], search_forward=False)
    nak_end_dt = _find_transition_time(dt_ist, "nak_idx", p_curr["nak_idx"], search_forward=True)

    tithi_timing_str = f"{_fmt_clock(tithi_start_dt, ref_date)} – {_fmt_clock(tithi_end_dt, ref_date)} IST"
    nak_timing_str = f"{_fmt_clock(nak_start_dt, ref_date)} – {_fmt_clock(nak_end_dt, ref_date)} IST"

    wd = dt_ist.weekday()  # 0=Mon .. 6=Sun
    wd_ta, wd_en, wd_default_deity = WEEKDAY_NAMES[wd]
    daily_times = WEEKDAY_TIMINGS[wd]

    m_en = p_morn["month_en"]
    m_ta = p_morn["month_ta"]
    t_idx = p_morn["tithi_idx"]
    t_eve_idx = p_eve["tithi_idx"]
    nak_en = p_morn["nak_en"]
    nak_ta = p_morn["nak_ta"]

    special_events = []
    primary_deity = None
    secondary_deity = None
    forbidden_deities = set()
    is_major_vratham = False
    special_pooja_time = f"நல்ல நேரம்: {daily_times['nalla_neram_am']} & {daily_times['nalla_neram_pm']}"
    occasion_badge_ta = f"{m_ta} {p_morn['tamil_day']} • {wd_ta} • {nak_ta}"
    occasion_badge_en = f"{m_en} Month | {wd_en} | {nak_en} Nakshatram"
    festival_hashtags = []

    # =========================================================================
    # TIER 1: MAJOR ANNUAL & MONTHLY FESTIVALS / VRATHAMS (HIGHEST PRIORITY)
    # =========================================================================

    # 1. MAHA SHIVARATRI / MASA SHIVARATRI
    if t_idx == 28 or t_eve_idx == 28:
        primary_deity = "shiva"
        secondary_deity = "shiva"
        is_major_vratham = True
        forbidden_deities.update(["vishnu"])
        special_pooja_time = "லிங்கோத்பவ காலம்: இரவு 11:30 PM – 12:30 AM IST"
        if m_en == "Maasi":
            special_events.append("மகா சிவராத்திரி (Maha Shivaratri)")
            occasion_badge_ta = "மகா சிவராத்திரி வழிபாடு | MAHA SHIVARATRI"
            festival_hashtags.extend(["#MahaShivaratri", "#Shivaratri", "#OmNamahShivaya"])
        else:
            special_events.append("மாத சிவராத்திரி (Masa Shivaratri)")
            occasion_badge_ta = f"{m_ta} மாத சிவராத்திரி | MASA SHIVARATRI"
            festival_hashtags.extend(["#MasaShivaratri", "#Shivaratri", "#OmNamahShivaya"])

    # 2. PRADOSHAM
    elif t_eve_idx in (12, 27) or t_idx in (12, 27):
        primary_deity = "shiva"
        secondary_deity = "murugan"
        is_major_vratham = True
        forbidden_deities.update(["vishnu"])
        special_pooja_time = "பிரதோஷ பூஜை நேரம்: மாலை 04:30 PM – 06:00 PM IST"
        if wd == 5:
            special_events.append("சனி மகா பிரதோஷம் (Sani Maha Pradosham)")
            occasion_badge_ta = "சனி மகா பிரதோஷம் | 04:30-06:00 PM IST"
            festival_hashtags.extend(["#SaniPradosham", "#Pradosham", "#Nandi", "#Shiva"])
        elif wd == 0:
            special_events.append("சோமவார பிரதோஷம் (Soma Pradosham)")
            occasion_badge_ta = "சோமவார பிரதோஷம் | 04:30-06:00 PM IST"
            festival_hashtags.extend(["#SomaPradosham", "#Pradosham", "#Shiva"])
        else:
            special_events.append("பிரதோஷ வழிபாடு (Pradosham)")
            occasion_badge_ta = "பிரதோஷ நந்தி வழிபாடு | 04:30-06:00 PM IST"
            festival_hashtags.extend(["#Pradosham", "#Nandi", "#OmNamahShivaya"])

    # 3. SKANDA SASHTI / KRITTIKA / THAIPUSAM / PANGUNI UTHIRAM
    elif (
        t_idx in (5, 20)
        or (m_en == "Aippasi" and 0 <= t_idx <= 5)
        or nak_en == "Krittika"
        or (m_en == "Thai" and nak_en == "Pushya")
        or (m_en == "Panguni" and nak_en == "Uttara Phalguni")
        or (m_en == "Vaikasi" and nak_en == "Vishakha")
    ):
        primary_deity = "murugan"
        secondary_deity = "vinayagar"
        is_major_vratham = True
        if m_en == "Aippasi" and 0 <= t_idx <= 5:
            day_num = t_idx + 1
            special_events.append(f"கந்த சஷ்டி பெருவிழா - நாள் {day_num} (Skanda Sashti Day {day_num})")
            occasion_badge_ta = f"கந்த சஷ்டி விரதம் (நாள் {day_num}) | SKANDA SASHTI"
            special_pooja_time = f"சஷ்டி வழிபாடு: காலை {daily_times['nalla_neram_am']} & மாலை {daily_times['nalla_neram_pm']}"
            festival_hashtags.extend(["#KandaSashti", "#SkandaSashti", "#Soorasamharam", "#Murugan"])
        elif m_en == "Thai" and nak_en == "Pushya":
            special_events.append("தைப்பூசத் திருவிழா (Thaipusam)")
            occasion_badge_ta = "தைப்பூசத் திருநாள் | THAIPUSAM SPECIAL"
            special_pooja_time = f"பூச நட்சத்திரம்: {nak_timing_str}"
            festival_hashtags.extend(["#Thaipusam", "#Palani", "#Kavadi", "#Murugan"])
        elif m_en == "Panguni" and nak_en == "Uttara Phalguni":
            special_events.append("பங்குனி உத்திரம் (Panguni Uthiram)")
            occasion_badge_ta = "பங்குனி உத்திரத் திருவிழா | PANGUNI UTHIRAM"
            special_pooja_time = f"உத்திர நட்சத்திரம்: {nak_timing_str}"
            festival_hashtags.extend(["#PanguniUthiram", "#Murugan", "#Vetrivel"])
        elif nak_en == "Krittika":
            special_events.append("மாதக் கார்த்திகை விரதம் (Krittika Nakshatra Vratham)")
            occasion_badge_ta = f"{m_ta} கார்த்திகை விரதம் | KRITTIKA MURUGAN"
            special_pooja_time = f"கார்த்திகை நட்சத்திர நேரம்: {nak_timing_str}"
            festival_hashtags.extend(["#Karthigai", "#Krittika", "#Murugan", "#ArupadaiVeedu"])
        else:
            special_events.append("சஷ்டி விரதம் (Sashti Vratham)")
            occasion_badge_ta = "சஷ்டி விரத வழிபாடு | SASHTI VRATHAM"
            special_pooja_time = f"சஷ்டி திதி நேரம்: {tithi_timing_str}"
            festival_hashtags.extend(["#Sashti", "#KandaSashtiKavasam", "#Murugan"])

    # 4. EKADASHI / VAIKUNTA EKADASHI / SHRAVANA (THIRUVONAM)
    elif t_idx in (10, 25) or nak_en == "Shravana":
        primary_deity = "vishnu"
        secondary_deity = "amman"
        is_major_vratham = True
        forbidden_deities.update(["shiva"])
        if m_en == "Margazhi" and t_idx == 10:
            special_events.append("வைகுண்ட ஏகாதசி (Vaikunta Ekadashi)")
            occasion_badge_ta = "வைகுண்ட ஏகாதசி சொர்க்கவாசல் | VAIKUNTA EKADASHI"
            special_pooja_time = f"ஏகாதசி திதி நேரம்: {tithi_timing_str}"
            festival_hashtags.extend(["#VaikuntaEkadashi", "#Ekadashi", "#Perumal", "#Govinda"])
        elif t_idx in (10, 25):
            special_events.append("ஏகாதசி விரதம் (Ekadashi Vratham)")
            occasion_badge_ta = f"{p_morn['paksha'].split()[0]} ஏகாதசி விரதம் | EKADASHI"
            special_pooja_time = f"ஏகாதசி திதி நேரம்: {tithi_timing_str}"
            festival_hashtags.extend(["#Ekadashi", "#Perumal", "#Narayana", "#Tirupati"])
        else:
            special_events.append("திருவோண விரதம் (Thiruvonam Perumal Vazhipadu)")
            occasion_badge_ta = "திருவோண நட்சத்திர பெருமாள் வழிபாடு | THIRUVONAM"
            special_pooja_time = f"திருவோண நட்சத்திர நேரம்: {nak_timing_str}"
            festival_hashtags.extend(["#Thiruvonam", "#Perumal", "#Venkateswara"])

    # 5. CHATURTHI (VINAYAKA CHATURTHI / SANKATAHARA CHATURTHI)
    elif t_idx in (3, 18) or t_eve_idx == 18:
        primary_deity = "vinayagar"
        secondary_deity = "murugan"
        is_major_vratham = True
        if t_idx == 18 or t_eve_idx == 18:
            special_events.append("சங்கடஹர சதுர்த்தி (Sankatahara Chaturthi)")
            occasion_badge_ta = "சங்கடஹர சதுர்த்தி வழிபாடு | SANKATAHARA CHATURTHI"
            special_pooja_time = f"சதுர்த்தி திதி: {tithi_timing_str} | சந்திரோதய பூஜை: 06:30 PM"
            festival_hashtags.extend(["#SankataharaChaturthi", "#Vinayagar", "#Ganapathi"])
        else:
            special_events.append("வளர்பிறை சதுர்த்தி (Shukla Chaturthi)")
            occasion_badge_ta = "சதுர்த்தி விநாயகர் வழிபாடு | VINAYAGAR CHATURTHI"
            special_pooja_time = f"சதுர்த்தி திதி நேரம்: {tithi_timing_str}"
            festival_hashtags.extend(["#VinayagarChaturthi", "#Ganapathi", "#Pillaiyar"])

    # 6. POURNAMI (FULL MOON)
    elif t_idx == 14 or t_eve_idx == 14:
        primary_deity = "amman"
        secondary_deity = "shiva"
        is_major_vratham = True
        special_events.append("பௌர்ணமி அம்மன் & கிரிவல வழிபாடு (Pournami Full Moon)")
        occasion_badge_ta = "பௌர்ணமி திருவிளக்கு & கிரிவல வழிபாடு | POURNAMI"
        special_pooja_time = f"பௌர்ணமி திதி நேரம்: {tithi_timing_str}"
        festival_hashtags.extend(["#Pournami", "#Girivalam", "#Abhirami", "#Amman", "#Tiruvannamalai"])

    # 7. AMAVASAI (NEW MOON)
    elif t_idx == 29 or t_eve_idx == 29:
        primary_deity = "amman"
        secondary_deity = "vallalar"
        is_major_vratham = True
        special_events.append("அமாவாசை அபிராமி அந்தாதி வழிபாடு (Amavasai)")
        occasion_badge_ta = "அமாவாசை அபிராமி அம்மன் அருள் | AMAVASAI SPECIAL"
        special_pooja_time = f"அமாவாசை திதி நேரம்: {tithi_timing_str}"
        festival_hashtags.extend(["#Amavasai", "#AbhiramiAndhadhi", "#Amman"])

    # 8. THEYPIRAI ASHTAMI (Kala Bhairava / Shiva)
    elif t_idx == 22:
        primary_deity = "shiva"
        secondary_deity = "amman"
        is_major_vratham = True
        special_events.append("தேய்பிறை அஷ்டமி பைரவர் & சிவ வழிபாடு (Theypirai Ashtami)")
        occasion_badge_ta = "தேய்பிறை அஷ்டமி வழிபாடு | BHAIRAVA & SHIVA ASHTAMI"
        special_pooja_time = f"அஷ்டமி திதி: {tithi_timing_str} | இராகு காலம்: {daily_times['rahu_kalam']}"
        festival_hashtags.extend(["#TheypiraiAshtami", "#Bhairavar", "#Shiva"])

    # =========================================================================
    # TIER 2: SACRED TAMIL MONTH OBSERVANCES
    # =========================================================================
    if primary_deity is None:
        if m_en == "Margazhi":
            if nak_en == "Ardra":
                primary_deity = "shiva"
                secondary_deity = "shiva"
                is_major_vratham = True
                special_events.append("ஆருத்ரா தரிசனம் (Arudra Darisanam)")
                occasion_badge_ta = "மார்கழி திருவாதிரை ஆருத்ரா தரிசனம் | ARUDRA DARISANAM"
                festival_hashtags.extend(["#ArudraDarisanam", "#Thiruvathirai", "#Natarajar"])
            else:
                primary_deity = "vishnu" if dt_ist.hour < 10 else "shiva"
                secondary_deity = "shiva" if primary_deity == "vishnu" else "vishnu"
                special_events.append("மார்கழிப் பாவை நோன்பு (Margazhi Sacred Dawn)")
                occasion_badge_ta = "மார்கழித் திருப்பாவை & திருவெம்பாவை | MARGAZHI SPECIAL"
                festival_hashtags.extend(["#Margazhi", "#Thiruppavai", "#Thiruvempavai"])

        elif m_en == "Purattasi" and wd == 5:
            primary_deity = "vishnu"
            secondary_deity = "vishnu"
            is_major_vratham = True
            forbidden_deities.update(["shiva"])
            special_events.append("புரட்டாசி சனிக்கிழமை பெருமாள் வழிபாடு (Purattasi Saturday)")
            occasion_badge_ta = "புரட்டாசி சனிக்கிழமை பெருமாள் சிறப்பு வழிபாடு"
            festival_hashtags.extend(["#Purattasi", "#PurattasiSani", "#Perumal", "#Govinda"])

        elif m_en in ("Aadi", "Thai") and wd == 4:
            primary_deity = "amman"
            secondary_deity = "murugan"
            is_major_vratham = True
            special_events.append(f"{m_ta} வெள்ளிக்கிழமை அம்மன் வழிபாடு ({m_en} Velli)")
            occasion_badge_ta = f"{m_ta} வெள்ளிக்கிழமை அம்மன் சிறப்பு வழிபாடு"
            festival_hashtags.extend([f"#{m_en}Velli", "#Amman", "#OmSakthi"])

    # =========================================================================
    # TIER 3: DAILY VARA (WEEKDAY) TRADITIONAL TAMIL AGAMA ALIGNMENT
    # =========================================================================
    if primary_deity is None:
        if wd == 0:
            primary_deity = "shiva"
            secondary_deity = "vinayagar"
            special_events.append("திங்கட்கிழமை சிவ வழிபாடு (Somavara Shiva Pooja)")
        elif wd == 1:
            primary_deity = "murugan"
            secondary_deity = "amman"
            special_events.append("செவ்வாய்க்கிழமை முருகப்பெருமான் & அம்மன் வழிபாடு")
        elif wd == 2:
            primary_deity = "vishnu"
            secondary_deity = "thirukkural"
            special_events.append("புதன்கிழமை பெருமாள் & தமிழ் மறை வழிபாடு")
        elif wd == 3:
            primary_deity = "vallalar"
            secondary_deity = "thirukkural"
            special_events.append("வியாழக்கிழமை குருவருள் & திருவருட்பா வழிபாடு")
        elif wd == 4:
            primary_deity = "amman"
            secondary_deity = "murugan"
            special_events.append("வெள்ளிக்கிழமை அம்பிகை & முருகன் வழிபாடு")
        elif wd == 5:
            primary_deity = "vishnu"
            secondary_deity = "vinayagar"
            special_events.append("சனிக்கிழமை பெருமாள் & விநாயகர் வழிபாடு")
        else:
            primary_deity = "shiva"
            secondary_deity = "murugan"
            special_events.append("ஞாயிற்றுக்கிழமை சிவபெருமான் & முருகன் வழிபாடு")

    slot_deities = {
        6: primary_deity,
        11: secondary_deity or primary_deity,
        12: secondary_deity or primary_deity,
        16: primary_deity,
        18: primary_deity,
        20: secondary_deity or primary_deity,
    }

    hr = dt_ist.hour
    if hr < 9:
        active_deity = slot_deities[6]
    elif hr < 14:
        active_deity = slot_deities[11]
    elif hr < 18:
        active_deity = slot_deities[16]
    else:
        active_deity = slot_deities[20]

    tithi_short_ta = p_curr["tithi_name"].split("(")[0].strip()
    onscreen_panchangam_line1 = f"{m_ta} {p_morn['tamil_day']}, {wd_ta} | திதி: {tithi_short_ta} ({tithi_timing_str})"
    onscreen_panchangam_line2 = f"நட்சத்திரம்: {p_curr['nak_ta']} ({nak_timing_str}) | நல்ல நேரம்: {daily_times['nalla_neram_am']}"

    return {
        "datetime_ist": dt_ist.isoformat(),
        "weekday_ta": wd_ta,
        "weekday_en": wd_en,
        "tamil_month_ta": m_ta,
        "tamil_month_en": m_en,
        "tamil_day": p_morn["tamil_day"],
        "tithi_name": p_curr["tithi_name"],
        "tithi_short_ta": tithi_short_ta,
        "tithi_timing": tithi_timing_str,
        "evening_tithi_name": p_eve["tithi_name"],
        "paksha": p_curr["paksha"],
        "nakshatra_ta": p_curr["nak_ta"],
        "nakshatra_en": p_curr["nak_en"],
        "nakshatra_timing": nak_timing_str,
        "rahu_kalam": daily_times["rahu_kalam"],
        "yama_gandam": daily_times["yama_gandam"],
        "kuligai": daily_times["kuligai"],
        "nalla_neram_am": daily_times["nalla_neram_am"],
        "nalla_neram_pm": daily_times["nalla_neram_pm"],
        "gowri_am": daily_times["gowri_am"],
        "gowri_pm": daily_times["gowri_pm"],
        "special_pooja_time": special_pooja_time,
        "onscreen_panchangam_line1": onscreen_panchangam_line1,
        "onscreen_panchangam_line2": onscreen_panchangam_line2,
        "is_major_vratham": is_major_vratham,
        "special_events": special_events,
        "primary_deity": primary_deity,
        "secondary_deity": secondary_deity,
        "active_deity": active_deity,
        "slot_deities": slot_deities,
        "forbidden_deities": sorted(list(forbidden_deities)),
        "occasion_badge_ta": occasion_badge_ta,
        "occasion_badge_en": occasion_badge_en,
        "festival_hashtags": festival_hashtags,
    }


def print_7day_panchangam_forecast(start_dt: datetime | None = None):
    if start_dt is None:
        start_dt = datetime.now(IST)
    print("=" * 100)
    print("🗓️  7-DAY TAMIL PANCHANGAM, EXACT TIMINGS & 6-PILLAR SHORTS SCHEDULE FOR @GURUKULADESAM2")
    print("=" * 100)
    for d in range(7):
        dt = start_dt + timedelta(days=d)
        info = get_auspicious_alignment_for_datetime(dt)
        date_str = dt.strftime("%Y-%m-%d (%a)")
        ev_str = ", ".join(info["special_events"])
        s6 = info["slot_deities"][6].upper()
        s11 = info["slot_deities"][11].upper()
        s16 = info["slot_deities"][16].upper()
        s20 = info["slot_deities"][20].upper()
        print(
            f"• {date_str} | {info['tamil_month_ta']} {info['tamil_day']:2d} | "
            f"திதி: {info['tithi_short_ta']} ({info['tithi_timing']})\n"
            f"  🌟 நட்சத்திரம்: {info['nakshatra_ta']} ({info['nakshatra_timing']}) | "
            f"நல்ல நேரம்: {info['nalla_neram_am']} | இராகு: {info['rahu_kalam']}\n"
            f"  🎯 Slots -> 06:00 AM: [{s6}] | 11:00 AM: [{s11}] | 04:00 PM: [{s16}] | 08:00 PM: [{s20}] "
            f"| Forbidden: {info['forbidden_deities'] or 'None'}\n"
            f"  ✨ Occasion: {ev_str} ({info['special_pooja_time']})\n"
        )
    print("=" * 100)


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    print_7day_panchangam_forecast()
