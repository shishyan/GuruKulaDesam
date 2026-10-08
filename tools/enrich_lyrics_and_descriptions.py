#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guru Kula Desam (@guru-kula-desam)
Lyrics & Metadata Enrichment Specialist Pipeline
=================================================
Systematically enriches every devotional and scripture song in the catalog with:
1. Complete, authentic Tamil lyrics (preserving traditional orthography, Sandhi, and meter).
2. Comprehensive English meanings and spiritual philosophical commentaries.
3. Canonical scripture attribution (Thirukkural, Thiruvasagam, Thevaram, Thiruvarutpa,
   Thirumandhiram, Divya Prabandham, Kandar Anubhuti, Thiruppugazh, etc.).
4. Suno AI prompt lyrics, style tags, and source URLs.
5. Standardized 7-section YouTube description packages.

Persists to:
- production/metadata/all_songs_lyrics_and_meanings.json
- live_youtube_metadata.json
- master_all_598_songs_catalog.json (across all copies)
- assets/data/catalog.json (and mirrors across docs/site)
"""

import os
import sys
import json
import re
import time
import urllib.request
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
def load_env():
    env_file = ROOT_DIR / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("\"'")

load_env()

# Cache file paths
CACHE_DIR = ROOT_DIR / "production" / "metadata"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
SUNO_CACHE_PATH = CACHE_DIR / "suno_cache.json"
GEMINI_CACHE_PATH = CACHE_DIR / "gemini_transcriptions_cache.json"
OUTPUT_MASTER_PATH = CACHE_DIR / "all_songs_lyrics_and_meanings.json"

# ==============================================================================
# 1. SCRIPTURE VERSE MATCHER
# ==============================================================================
class ScriptureVerseMatcher:
    def __init__(self):
        self.kural_data = {}
        self.site_data_by_id = {}
        self.site_data_by_title = {}
        self._load_thirukkural()
        self._load_site_catalog()

    def _load_thirukkural(self):
        kural_path = ROOT_DIR / "production" / "thirukkural_all.json"
        if kural_path.exists():
            with open(kural_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
                kurals = raw.get("kural", [])
                # Group by chapter (10 kurals per chapter)
                for k in kurals:
                    num = k["Number"]
                    ch = ((num - 1) // 10) + 1
                    if ch not in self.kural_data:
                        self.kural_data[ch] = []
                    self.kural_data[ch].append(k)
            print(f"[ScriptureMatcher] Loaded {len(self.kural_data)} Thirukkural chapters ({len(kurals)} couplets)")

    def _load_site_catalog(self):
        cat_path = ROOT_DIR / "assets" / "data" / "catalog.json"
        if cat_path.exists():
            with open(cat_path, "r", encoding="utf-8") as f:
                cat = json.load(f)
                for section, items in cat.items():
                    for it in items:
                        vid = it.get("id")
                        if vid:
                            self.site_data_by_id[vid] = it
                        title = (it.get("title") or "").strip()
                        if title:
                            # Normalize title key
                            norm_key = re.sub(r'[\s\-_|:()\[\]]+', '', title.lower())
                            self.site_data_by_title[norm_key] = it
            print(f"[ScriptureMatcher] Loaded {len(self.site_data_by_id)} entries from site catalog")

    def match_thirukkural(self, title, video_id=""):
        """Extracts chapter number and returns complete 10 kurals and commentary."""
        m = re.search(r'அதிகாரம்\s*(\d+)', title, re.IGNORECASE)
        if not m:
            m = re.search(r'(?:chapter|adhigaram)\s*(\d+)', title, re.IGNORECASE)
        
        if not m:
            return None

        ch_num = int(m.group(1))
        kurals = self.kural_data.get(ch_num)
        if not kurals:
            return None

        # Build Tamil lyrics (All 10 couplets)
        tamil_lines = []
        english_lines = []
        tamil_commentary = []

        for k in kurals:
            num = k["Number"]
            l1 = k.get("Line1", "").strip()
            l2 = k.get("Line2", "").strip()
            tamil_lines.append(f"குறள் {num}:\n{l1}\n{l2}")
            
            exp = k.get("explanation", "").strip() or k.get("Translation", "").strip()
            cplt = k.get("couplet", "").strip()
            eng_text = f"Kural {num}: {cplt if cplt else exp}"
            if exp and cplt and exp != cplt:
                eng_text += f"\n  Meaning: {exp}"
            english_lines.append(eng_text)

            mv = k.get("mv", "").strip()
            if mv:
                tamil_commentary.append(f"குறள் {num}: {mv}")

        full_tamil_lyrics = "\n\n".join(tamil_lines)
        full_english_meaning = "\n\n".join(english_lines)
        full_tamil_meaning = "\n\n".join(tamil_commentary)

        return {
            "source_type": "thirukkural",
            "chapter_number": ch_num,
            "scripture": "திருக்குறள் (Thirukkural)",
            "author": "திருவள்ளுவர் (Thiruvalluvar)",
            "lyrics": full_tamil_lyrics,
            "meaning_tamil": full_tamil_meaning,
            "meaning_english": full_english_meaning
        }

    def match_canonical_scripture(self, video_id, title, scripture_source="", author=""):
        """Matches classical Tamil scripture from existing verified database."""
        # 1. Thirukkural match
        kural_match = self.match_thirukkural(title, video_id)
        if kural_match:
            return kural_match

        # 2. Match by video ID in site catalog
        if video_id in self.site_data_by_id:
            entry = self.site_data_by_id[video_id]
            lyrics = entry.get("lyrics", "").strip()
            meaning = entry.get("meaning", "").strip()
            if len(lyrics) > 20 and len(meaning) > 20:
                return {
                    "source_type": "site_catalog",
                    "scripture": entry.get("source") or scripture_source or "மரபு இலக்கியம்",
                    "author": entry.get("author") or author or "பாரம்பரிய ஆன்றோர்",
                    "lyrics": lyrics,
                    "meaning_tamil": meaning,
                    "meaning_english": ""
                }

        # 3. Match by normalized title in site catalog
        norm_title = re.sub(r'[\s\-_|:()\[\]]+', '', title.lower())
        for k, entry in self.site_data_by_title.items():
            if norm_title in k or k in norm_title:
                lyrics = entry.get("lyrics", "").strip()
                meaning = entry.get("meaning", "").strip()
                if len(lyrics) > 20 and len(meaning) > 20:
                    return {
                        "source_type": "site_catalog_fuzzy",
                        "scripture": entry.get("source") or scripture_source or "மரபு இலக்கியம்",
                        "author": entry.get("author") or author or "பாரம்பரிய ஆன்றோர்",
                        "lyrics": lyrics,
                        "meaning_tamil": meaning,
                        "meaning_english": ""
                    }

        return None


# ==============================================================================
# 2. SUNO DATA RETRIEVER
# ==============================================================================
class SunoDataRetriever:
    def __init__(self):
        self.cache = {}
        self._load_cache()

    def _load_cache(self):
        if SUNO_CACHE_PATH.exists():
            try:
                with open(SUNO_CACHE_PATH, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
                print(f"[SunoRetriever] Loaded {len(self.cache)} cached Suno entries")
            except Exception as e:
                print(f"[SunoRetriever] Cache load error: {e}")

    def _save_cache(self):
        try:
            with open(SUNO_CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[SunoRetriever] Cache save error: {e}")

    @staticmethod
    def extract_suno_uuid(text):
        if not text:
            return None
        m = re.search(r'suno\.com/song/([a-f0-9\-]{36})', text, re.IGNORECASE)
        return m.group(1) if m else None

    def fetch_suno_data(self, suno_uuid):
        if not suno_uuid:
            return None

        if suno_uuid in self.cache:
            return self.cache[suno_uuid]

        url = f"https://suno.com/song/{suno_uuid}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                html = resp.read().decode("utf-8")

            # Parse title from og:title
            m_title = re.search(r'<meta\s+property="og:title"\s+content="([^"]*)"', html)
            title = m_title.group(1).replace(" | Suno", "") if m_title else ""

            # Parse Next.js App Router chunks
            m_push = re.search(r'self\.__next_f\.push\(\[1,\s*"(.*)"\]\)', html, re.DOTALL)
            lyrics = ""
            tags = ""

            if m_push:
                s = m_push.group(1)
                lines = s.split('\\n')
                
                # Search for tags
                m_tags = re.search(r'"tags":"(.*?)(?<!\\)"', s)
                if m_tags:
                    tags = m_tags.group(1)

                # Collect prompt lines
                prompt_lines = []
                collecting = False
                for line in lines:
                    if line.startswith("58:T") or "T35b9" in line:
                        # Extract after tag
                        parts = line.split(",", 1)
                        if len(parts) > 1:
                            prompt_lines.append(parts[1].strip())
                        collecting = True
                        continue

                    if collecting:
                        # Check if line marks end of prompt payload
                        if line.startswith("45:[") or line.startswith("4c:[") or line.startswith("46:["):
                            break
                        if line.startswith("59:") or line.startswith("58:"):
                            break
                        cleaned_line = line.strip()
                        if cleaned_line:
                            prompt_lines.append(cleaned_line)

                if prompt_lines:
                    lyrics = "\n".join(prompt_lines)

            # Fallback if lyrics still empty: scan for Tamil stanzas in html
            if not lyrics:
                tamil_blocks = re.findall(r'[\u0B80-\u0BFF\s\n,!.?]{30,}', html)
                if tamil_blocks:
                    lyrics = "\n".join([b.strip() for b in tamil_blocks if len(b.strip()) > 30])

            result = {
                "uuid": suno_uuid,
                "url": url,
                "title": title,
                "style_tags": tags,
                "lyrics": lyrics,
                "fetched_at": datetime.utcnow().isoformat() + "Z"
            }
            self.cache[suno_uuid] = result
            self._save_cache()
            print(f"[SunoRetriever] Successfully fetched Suno song: {suno_uuid} ('{title}')")
            return result
        except Exception as e:
            print(f"[SunoRetriever] Error fetching Suno song {suno_uuid}: {e}")
            return None


# ==============================================================================
# 3. MULTIMODAL GEMINI TRANSCRIBER & PHILOSOPHICAL ENRICHER
# ==============================================================================
class MultimodalGeminiTranscriber:
    def __init__(self):
        self.cache = {}
        self.client = None
        self._load_cache()
        self._init_client()

    def _load_cache(self):
        if GEMINI_CACHE_PATH.exists():
            try:
                with open(GEMINI_CACHE_PATH, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
                print(f"[GeminiTranscriber] Loaded {len(self.cache)} cached Gemini transcriptions")
            except Exception as e:
                print(f"[GeminiTranscriber] Cache load error: {e}")

    def _save_cache(self):
        try:
            with open(GEMINI_CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[GeminiTranscriber] Cache save error: {e}")

    def _init_client(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("[GeminiTranscriber] WARNING: GEMINI_API_KEY not found in environment!")
            return
        try:
            from google import genai
            self.client = genai.Client()
            print("[GeminiTranscriber] Gemini 3.8 Flash Client initialized successfully")
        except Exception as e:
            print(f"[GeminiTranscriber] Failed to initialize Gemini Client: {e}")

    def transcribe_or_enrich(self, video_id, title, scripture_source, deity, existing_lyrics=""):
        """Transcribes from audio if present, or enriches lyrics and philosophical commentary."""
        if video_id in self.cache:
            return self.cache[video_id]

        if not self.client:
            return None

        # Check for local audio file
        audio_candidates = [
            ROOT_DIR / "source" / "youtube" / f"{video_id}.m4a",
            ROOT_DIR / "source" / "youtube" / f"{video_id}.mp3",
            ROOT_DIR / "source" / f"{video_id}.m4a"
        ]
        local_audio = next((p for p in audio_candidates if p.exists()), None)

        prompt_system = (
            "You are the revered Tamil Vedic scholar, musicologist, and spiritual master of Guru Kula Desam (@guru-kula-desam).\n"
            "Your sacred duty is to provide authentic Tamil devotional verses, complete line-by-line lyrics (preserving classical orthography), "
            "and profound English philosophical commentary with Sanatana reverence.\n\n"
            "Return a strictly valid JSON object with the following keys:\n"
            "{\n"
            "  \"tamil_lyrics\": \"Full authentic Tamil lyrics with poetic stanzas/couplets\",\n"
            "  \"english_translation\": \"Line-by-line or stanza-by-stanza English translation\",\n"
            "  \"philosophical_commentary\": \"Deep spiritual commentary in English explaining the inner mystical import\",\n"
            "  \"tamil_meaning\": \"Detailed explanation in formal classical Tamil (உரை விளக்கம்)\",\n"
            "  \"musical_style\": \"Flute, Veena, Mridangam, Tanpura, Temple Bells, Classical Vedic Raga\"\n"
            "}\n"
            "Ensure the response is ONLY valid JSON, with NO surrounding markdown backticks or extra text."
        )

        try:
            if local_audio and local_audio.stat().st_size > 0:
                print(f"[GeminiTranscriber] Listening to local audio for {video_id} ({local_audio.name})...")
                audio_file = self.client.files.upload(file=str(local_audio))
                content_list = [
                    audio_file,
                    f"{prompt_system}\n\nSong Title: {title}\nScripture Source: {scripture_source}\nDeity/Subject: {deity}"
                ]
                resp = self.client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=content_list
                )
                try:
                    self.client.files.delete(name=audio_file.name)
                except Exception:
                    pass
            else:
                context_info = f"Song Title: {title}\nScripture Source: {scripture_source}\nDeity/Subject: {deity}"
                if existing_lyrics:
                    context_info += f"\nExisting Tamil Lyrics fragment:\n{existing_lyrics}"
                
                resp = self.client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=f"{prompt_system}\n\n{context_info}"
                )

            raw_text = resp.text.strip()
            # Clean JSON formatting
            if raw_text.startswith("```"):
                raw_text = re.sub(r'^```(?:json)?\s*', '', raw_text)
                raw_text = re.sub(r'\s*```$', '', raw_text)

            parsed = json.loads(raw_text)
            self.cache[video_id] = parsed
            self._save_cache()
            print(f"[GeminiTranscriber] Successfully generated/transcribed metadata for {video_id}")
            return parsed
        except Exception as e:
            print(f"[GeminiTranscriber] Generation error for {video_id}: {e}")
            return None


# ==============================================================================
# 4. STANDARDIZED DESCRIPTION BUILDER (7 SECTIONS)
# ==============================================================================
class DescriptionPackageBuilder:
    @staticmethod
    def build_hashtags(deity, scripture, title):
        tags = ["#GuruKulaDesam", "#TamilDevotional", "#VedicChants", "#SanatanaDharma"]
        
        # Scripture tags
        if "திருக்குறள்" in scripture or "thirukkural" in title.lower():
            tags.extend(["#திருக்குறள்", "#Thirukkural", "#Thiruvalluvar", "#TamilWisdom", "#SangamLiterature"])
        elif "திருவாசகம்" in scripture or "thiruvasagam" in title.lower():
            tags.extend(["#திருவாசகம்", "#Thiruvasagam", "#Manikkavasagar", "#Shaivam", "#ShivaBhakti"])
        elif "தேவாரம்" in scripture or "thevaram" in title.lower():
            tags.extend(["#தேவாரம்", "#Thevaram", "#Appar", "#Sambandar", "#Sundarar", "#Thirumurai"])
        elif "திருவருட்பா" in scripture or "vallalar" in title.lower():
            tags.extend(["#திருவருட்பா", "#Thiruvarutpa", "#Vallalar", "#Sanmargam", "#Arutperunjothi"])
        elif "திருப்பாவை" in scripture or "divya" in scripture.lower() or "krishna" in title.lower():
            tags.extend(["#திருப்பாவை", "#Thiruppavai", "#Andal", "#DivyaPrabandham", "#Vaishnavism"])
        elif "முருகன்" in deity or "முருக" in title or "murugan" in title.lower():
            tags.extend(["#முருகன்", "#LordMurugan", "#Thiruppugazh", "#KandarAnubhuti", "#ArupadaiVeedu"])
        elif "சிவன்" in deity or "shiva" in title.lower():
            tags.extend(["#சிவன்", "#LordShiva", "#OmNamahShivaya", "#Mahadev", "#ShivaTandavam"])
        elif "விநாயகர்" in deity or "ganesha" in title.lower():
            tags.extend(["#விநாயகர்", "#LordGanesha", "#VinayagarAgaval", "#Pillaiyar", "#PrathamPujya"])
        elif "அம்மன்" in deity or "devi" in title.lower():
            tags.extend(["#அம்மன்", "#GoddessShakthi", "#AbhiramiAnthathi", "#DeviStotram", "#DivineMother"])

        # Deduplicate preserving order
        seen = set()
        deduped = []
        for t in tags:
            if t not in seen:
                seen.add(t)
                deduped.append(t)
        return " ".join(deduped[:12])

    @staticmethod
    def generate_timestamps(title, is_film=False):
        """Generates thematic chapter timestamps based on track length and type."""
        if "அதிகாரம்" in title or "thirukkural" in title.lower():
            return (
                "00:00 - சங்க கால முகப்பு & தோற்றுவாய் (Sangam Invocation & Prelude)\n"
                "00:45 - அதிகார மூலக் குறட்பாக்கள் (Sacred Couplets & Recitation)\n"
                "02:30 - மெய்ப்பொருள் தத்துவ விளக்கம் (Philosophical Contemplation)\n"
                "04:15 - ஆன்ம அமைதி & மங்கள நிறைவு (Benediction & Silence)"
            )
        elif is_film:
            return (
                "00:00 - மங்கள ஆரம்பம் & திருக்காட்சி (Sacred Visual Opening)\n"
                "01:00 - பக்திப் பாசுர கானம் (Divine Hymn Recitation)\n"
                "02:40 - இறைவனின் அருட்காட்சி (Divine Epiphany & Transcendence)\n"
                "04:00 - சாந்தி நிறைவு (Universal Peace Benediction)"
            )
        else:
            return (
                "00:00 - தோற்றுவாய் (Sacred Prelude)\n"
                "00:30 - மூலப் பாடல் பதிகம் (Primary Hymn Verses)\n"
                "02:15 - ஆன்மீக தியான லயம் (Meditative Absorption)\n"
                "03:45 - மங்கள நிறைவு (Benediction & Shanti)"
            )

    @classmethod
    def assemble_package(cls, track_info, scripture_info, suno_info, gemini_info):
        video_id = track_info.get("video_id") or track_info.get("id")
        title = track_info.get("canonical_title") or track_info.get("title", "")
        tamil_title = track_info.get("tamil_title") or title
        english_title = track_info.get("english_title", "")
        descriptor = track_info.get("descriptor") or ("Film" if "[Film]" in title else "Audio")
        genre = track_info.get("genre", "தமிழ் பக்தி மரபு")

        # Determine scripture and author
        scripture = (
            (scripture_info and scripture_info.get("scripture")) or
            track_info.get("scripture_source") or
            track_info.get("source") or
            "பாரம்பரிய பக்திப் பனுவல்"
        )
        author = (
            (scripture_info and scripture_info.get("author")) or
            track_info.get("author") or
            "பாரம்பரிய சைவ/வைணவ ஆன்றோர்கள்"
        )

        # Determine Tamil Lyrics
        tamil_lyrics = ""
        if scripture_info and scripture_info.get("lyrics"):
            tamil_lyrics = scripture_info["lyrics"]
        elif suno_info and suno_info.get("lyrics") and len(suno_info["lyrics"]) > 30:
            tamil_lyrics = suno_info["lyrics"]
        elif gemini_info and gemini_info.get("tamil_lyrics"):
            tamil_lyrics = gemini_info["tamil_lyrics"]
        elif track_info.get("lyrics"):
            tamil_lyrics = track_info["lyrics"]

        # Determine Tamil Meaning
        tamil_meaning = ""
        if scripture_info and scripture_info.get("meaning_tamil"):
            tamil_meaning = scripture_info["meaning_tamil"]
        elif gemini_info and gemini_info.get("tamil_meaning"):
            tamil_meaning = gemini_info["tamil_meaning"]
        elif track_info.get("meaning"):
            tamil_meaning = track_info["meaning"]

        # Determine English Translation / Meaning
        english_meaning = ""
        if scripture_info and scripture_info.get("meaning_english"):
            english_meaning = scripture_info["meaning_english"]
        elif gemini_info and gemini_info.get("english_translation"):
            english_meaning = gemini_info["english_translation"]
            if gemini_info.get("philosophical_commentary"):
                english_meaning += "\n\nSpiritual Commentary:\n" + gemini_info["philosophical_commentary"]
        else:
            english_meaning = (
                f"Sacred devotional offering from '{scripture}', invoking divine grace, inner purity, "
                f"and ethical transcendence according to the timeless Sanatana Tamil heritage."
            )

        # Determine Musical Style & Credits
        musical_style = ""
        if suno_info and suno_info.get("style_tags"):
            musical_style = suno_info["style_tags"]
        elif gemini_info and gemini_info.get("musical_style"):
            musical_style = gemini_info["musical_style"]
        else:
            musical_style = "Traditional Vedic & Carnatic Instrumentation, Flute, Veena, Tanpura, Temple Bells, Symphony"

        # Official Source Links
        official_sources = [
            f"• YouTube Channel: https://www.youtube.com/@guru-kula-desam",
            f"• Master Audio / Video: https://www.youtube.com/watch?v={video_id}"
        ]
        if suno_info and suno_info.get("url"):
            official_sources.append(f"• Suno AI Production Master: {suno_info['url']}")
        if "திருக்குறள்" in scripture:
            official_sources.append("• Canonical Scripture Reference: Thirukkural (Shaivam.org / Project Madurai)")
        elif "திருவாசகம்" in scripture or "தேவாரம்" in scripture:
            official_sources.append("• Canonical Scripture Reference: Panniru Thirumurai (Shaivam.org / Tamil Virtual Academy)")
        elif "திருவருட்பா" in scripture:
            official_sources.append("• Canonical Scripture Reference: Thiruvarutpa by Thiru Arutprakasa Vallalar")
        elif "திருப்பாவை" in scripture:
            official_sources.append("• Canonical Scripture Reference: Nalayira Divya Prabandham (Andal Thiruppavai)")

        timestamps = cls.generate_timestamps(title, is_film=("[Film]" in title))
        hashtags = cls.build_hashtags(genre, scripture, title)

        # Assemble Full Description Package
        desc = (
            f"{title}\n"
            f"Guru Kula Desam (@guru-kula-desam)\n\n"
            f"═════════════════════════════════════════════════════════════════\n"
            f"🕉️ SCRIPTURE & PHILOSOPHICAL OVERVIEW\n"
            f"═════════════════════════════════════════════════════════════════\n"
            f"Deity / Subject: {genre}\n"
            f"Scripture Source: {scripture}\n"
            f"Author / Saint: {author}\n\n"
            f"{tamil_meaning}\n\n"
            f"═════════════════════════════════════════════════════════════════\n"
            f"📜 பாடல் வரிகள் (FULL TAMIL LYRICS)\n"
            f"═════════════════════════════════════════════════════════════════\n"
            f"{tamil_lyrics}\n\n"
            f"═════════════════════════════════════════════════════════════════\n"
            f"📖 ENGLISH TRANSLATION & MEANING\n"
            f"═════════════════════════════════════════════════════════════════\n"
            f"{english_meaning}\n\n"
            f"═════════════════════════════════════════════════════════════════\n"
            f"🎵 MUSICAL & PRODUCTION CREDITS\n"
            f"═════════════════════════════════════════════════════════════════\n"
            f"• Concept, Production & Curation: Guru Kula Desam (@guru-kula-desam)\n"
            f"• Sound Engineering & Vocal Direction: Nagarajan Balasubramanian\n"
            f"• Musical Composition: Suno AI & Traditional Vedic / Carnatic Ragas\n"
            f"• Musical Style / Instruments: {musical_style}\n"
            f"• Master Audio & Visuals: Guru Kula Desam Creative Lab\n\n"
            f"═════════════════════════════════════════════════════════════════\n"
            f"🔗 OFFICIAL SOURCE & REFERENCES\n"
            f"═════════════════════════════════════════════════════════════════\n"
            + "\n".join(official_sources) + "\n\n"
            f"═════════════════════════════════════════════════════════════════\n"
            f"⏱️ TIMESTAMPS & CHAPTERS\n"
            f"═════════════════════════════════════════════════════════════════\n"
            f"{timestamps}\n\n"
            f"═════════════════════════════════════════════════════════════════\n"
            f"🏷️ HASHTAGS\n"
            f"═════════════════════════════════════════════════════════════════\n"
            f"{hashtags}\n\n"
            f"Subscribe to @guru-kula-desam for authentic Tamil scripture chants, cinematic films, and philosophical wisdom."
        )

        return {
            "video_id": video_id,
            "title": title,
            "scripture": scripture,
            "author": author,
            "genre": genre,
            "tamil_lyrics": tamil_lyrics,
            "tamil_meaning": tamil_meaning,
            "english_meaning": english_meaning,
            "musical_style": musical_style,
            "suno_url": suno_info.get("url") if suno_info else "",
            "description": desc,
            "hashtags": hashtags
        }


# ==============================================================================
# 5. PIPELINE EXECUTION & METADATA PERSISTENCE
# ==============================================================================
def run_enrichment_pipeline():
    print("=" * 80)
    print("GURU KULA DESAM — METADATA & LYRICS ENRICHMENT PIPELINE")
    print("=" * 80)

    # Initialize modules
    matcher = ScriptureVerseMatcher()
    suno_retriever = SunoDataRetriever()
    gemini_transcriber = MultimodalGeminiTranscriber()

    # Load input catalogs
    with open(ROOT_DIR / "live_youtube_metadata.json", "r", encoding="utf-8") as f:
        live_yt = json.load(f)

    with open(ROOT_DIR / "master_all_598_songs_catalog.json", "r", encoding="utf-8") as f:
        master_list = json.load(f)
        master_map = {m["video_id"]: m for m in master_list}

    print(f"Loaded {len(live_yt)} live YouTube items and {len(master_map)} master catalog items.")

    enriched_database = {}
    updated_live_count = 0
    updated_master_count = 0

    total = len(live_yt)
    for idx, (vid_id, live_item) in enumerate(live_yt.items(), 1):
        master_item = master_map.get(vid_id, {})
        title = master_item.get("canonical_title") or live_item.get("title", "")
        scripture_source = master_item.get("scripture_source") or master_item.get("source", "")
        author = master_item.get("author", "")
        genre = master_item.get("genre", "")

        # 1. Match Canonical Scripture
        scripture_info = matcher.match_canonical_scripture(
            video_id=vid_id,
            title=title,
            scripture_source=scripture_source,
            author=author
        )

        # 2. Extract or Fetch Suno data
        current_desc = live_item.get("description", "")
        suno_uuid = SunoDataRetriever.extract_suno_uuid(current_desc)
        suno_info = None
        if suno_uuid:
            suno_info = suno_retriever.fetch_suno_data(suno_uuid)

        # 3. Multimodal Gemini Transcriber (if needed or for deep commentary)
        gemini_info = None
        needs_gemini = (
            scripture_info is None or 
            len(scripture_info.get("lyrics", "")) < 30 or 
            not scripture_info.get("meaning_english")
        )
        if needs_gemini:
            # Check if cached or local audio exists
            local_audio = ROOT_DIR / "source" / "youtube" / f"{vid_id}.m4a"
            if local_audio.exists() or vid_id in gemini_transcriber.cache:
                gemini_info = gemini_transcriber.transcribe_or_enrich(
                    video_id=vid_id,
                    title=title,
                    scripture_source=scripture_source,
                    deity=genre,
                    existing_lyrics=scripture_info.get("lyrics", "") if scripture_info else ""
                )

        # 4. Assemble Standardized Description Package
        track_info = {
            "video_id": vid_id,
            "title": live_item.get("title") or title,
            "canonical_title": title,
            "tamil_title": master_item.get("tamil_title"),
            "english_title": master_item.get("english_title"),
            "descriptor": master_item.get("descriptor"),
            "genre": genre,
            "scripture_source": scripture_source,
            "author": author,
            "lyrics": live_item.get("lyrics") or (scripture_info.get("lyrics") if scripture_info else ""),
            "meaning": live_item.get("meaning") or (scripture_info.get("meaning_tamil") if scripture_info else "")
        }

        package = DescriptionPackageBuilder.assemble_package(
            track_info=track_info,
            scripture_info=scripture_info,
            suno_info=suno_info,
            gemini_info=gemini_info
        )

        enriched_database[vid_id] = package

        # Update live_youtube_metadata in-place
        live_item["description"] = package["description"]
        updated_live_count += 1

        # Update master item fields
        if vid_id in master_map:
            master_map[vid_id]["scripture_source"] = package["scripture"]
            master_map[vid_id]["author"] = package["author"]
            updated_master_count += 1

        if idx % 50 == 0 or idx == total:
            print(f"Progress: [{idx}/{total}] Processed {vid_id} -> '{title[:40]}...'")

    # Persist Master Database of Lyrics, Meanings, and Packages
    print(f"\nWriting master enriched database to {OUTPUT_MASTER_PATH}...")
    with open(OUTPUT_MASTER_PATH, "w", encoding="utf-8") as f:
        json.dump(enriched_database, f, ensure_ascii=False, indent=2)
    print(f"Master database written successfully with {len(enriched_database)} enriched packages.")

    # Update live_youtube_metadata.json
    print(f"Updating live_youtube_metadata.json...")
    with open(ROOT_DIR / "live_youtube_metadata.json", "w", encoding="utf-8") as f:
        json.dump(live_yt, f, ensure_ascii=False, indent=2)
    print("live_youtube_metadata.json updated successfully!")

    # Update master_all_598_songs_catalog.json across repository roots
    print(f"Updating master catalogs...")
    updated_master_list = list(master_map.values())
    master_targets = [
        ROOT_DIR / "master_all_598_songs_catalog.json",
        ROOT_DIR / "assets" / "data" / "master_all_598_songs_catalog.json",
        ROOT_DIR / "docs" / "assets" / "data" / "master_all_598_songs_catalog.json",
        ROOT_DIR / "site" / "assets" / "data" / "master_all_598_songs_catalog.json"
    ]
    for target in master_targets:
        if target.parent.exists():
            with open(target, "w", encoding="utf-8") as f:
                json.dump(updated_master_list, f, ensure_ascii=False, indent=2)
            print(f"  Updated: {target.relative_to(ROOT_DIR)}")

    # Update site catalog.json to ensure 100% of live videos are included and have complete lyrics & meanings
    enrich_site_catalogs(enriched_database)

    print("\nEnrichment pipeline completed successfully!")

def enrich_site_catalogs(enriched_database):
    """Ensures assets/data/catalog.json, docs/assets/data/catalog.json, site/assets/data/catalog.json have all tracks."""
    cat_path = ROOT_DIR / "assets" / "data" / "catalog.json"
    if not cat_path.exists():
        return

    with open(cat_path, "r", encoding="utf-8") as f:
        site_cat = json.load(f)

    # Track existing IDs
    existing_ids = set()
    for cat, items in site_cat.items():
        for it in items:
            existing_ids.add(it["id"])
            # Update existing with enriched data
            if it["id"] in enriched_database:
                data = enriched_database[it["id"]]
                if data["tamil_lyrics"] and len(data["tamil_lyrics"]) > len(it.get("lyrics", "")):
                    it["lyrics"] = data["tamil_lyrics"]
                if data["tamil_meaning"] and len(data["tamil_meaning"]) > len(it.get("meaning", "")):
                    it["meaning"] = data["tamil_meaning"]
                it["author"] = data["author"]
                it["source"] = data["scripture"]

    # Append any missing live items into appropriate category
    added_count = 0
    for vid_id, data in enriched_database.items():
        if vid_id not in existing_ids:
            # Map category
            genre = data["genre"]
            if "திருக்குறள்" in genre or "thirukkural" in data["title"].lower():
                category = "thirukkural"
            elif "சிவபெருமான்" in genre:
                category = "shiva"
            elif "முருக" in genre:
                category = "murugan"
            elif "விஷ்ணு" in genre:
                category = "vishnu_krishna"
            elif "விநாயகர்" in genre:
                category = "vinayagar"
            elif "அம்மன்" in genre:
                category = "amman"
            else:
                category = "vallalar_cultural"

            new_item = {
                "id": vid_id,
                "title": data["title"],
                "type": "film" if "[Film]" in data["title"] else "audio",
                "playlists": ["Discography"],
                "category": category,
                "description": f"{data['title']} - {data['scripture']}",
                "author": data["author"],
                "source": data["scripture"],
                "lyrics": data["tamil_lyrics"],
                "meaning": data["tamil_meaning"] or data["english_meaning"]
            }
            if category not in site_cat:
                site_cat[category] = []
            site_cat[category].append(new_item)
            existing_ids.add(vid_id)
            added_count += 1

    print(f"[SiteCatalog] Added {added_count} missing live items to site catalog.")

    # Write back to assets/data/catalog.json and copy to docs and site
    for dest_dir in [ROOT_DIR / "assets" / "data", ROOT_DIR / "docs" / "assets" / "data", ROOT_DIR / "site" / "assets" / "data"]:
        if dest_dir.exists():
            with open(dest_dir / "catalog.json", "w", encoding="utf-8") as f:
                json.dump(site_cat, f, ensure_ascii=False, indent=2)

    # Regenerate catalog.js across all mirrors
    cat_js_content = f"/**\n * Guru Kula Desam - Complete Devotional & Scripture Catalog\n */\nwindow.GURUKULA_CATALOG = {json.dumps(site_cat, ensure_ascii=False)};\n"
    for dest_dir in [ROOT_DIR / "assets" / "data", ROOT_DIR / "docs" / "assets" / "data", ROOT_DIR / "site" / "assets" / "data"]:
        if dest_dir.exists():
            with open(dest_dir / "catalog.js", "w", encoding="utf-8") as f:
                f.write(cat_js_content)

    # Run trifolder sync
    sync_script = ROOT_DIR / "tools" / "sync" / "sync_trifolder.py"
    if sync_script.exists():
        import subprocess
        subprocess.run([sys.executable, str(sync_script), "--source", "docs"], cwd=str(ROOT_DIR))
        print("[SiteCatalog] Synchronized catalogs across assets, docs, and site via sync_trifolder.py")

if __name__ == "__main__":
    run_enrichment_pipeline()
