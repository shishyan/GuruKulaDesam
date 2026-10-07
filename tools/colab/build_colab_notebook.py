# -*- coding: utf-8 -*-
"""
Builder script to generate the official Google Colab Jupyter Notebook:
`colab_generate_gurukulam_artworks.ipynb`
Enables fast, local GPU generation of the remaining lesson illustrations
and Thirukkural chapter visuals on Google Colab (nagaraj957@gmail.com).
"""

import json
import os

LESSON_PROMPTS = [
    {
        "filename": "grade8_chatur_ashrama.jpg",
        "title": "தரம் 8 — சதுர் ஆசிரமங்கள் (Four Ashramas with Grihastha as the Foundation)",
        "prompt": "Masterpiece classical Raja Ravi Varma style oil painting depicting the Four Ashramas (Chatur Ashramas) with Grihastha householder as the central sustaining foundation. In the center, a noble Tamil householder couple in traditional silk attire warmly offers food, shelter and dana to a young Gurukula student (Brahmachari) holding palm leaf scriptures, an elderly retired couple in simple cotton walking peacefully toward forest contemplation (Vanaprastha), and an enlightened wandering ascetic monk with wooden danda and water pot (Sannyasi). An ancient majestic banyan tree arches overhead sheltering all life. Temple village courtyard in ancient Tamil Nadu, warm morning sunlight, deep cultural nobility, hyper-detailed oil on canvas.",
        "negative_prompt": "modern clothes, vehicles, electrical wires, plastic, watermark, text, signature, low quality, cartoon, anime, blurry, distorted hands, extra limbs"
    },
    {
        "filename": "grade9_saiva_agamas.jpg",
        "title": "தரம் 9 — இருபத்தெட்டு சைவ ஆகமங்கள் (28 Saiva Agamas & Sacred Temple Architecture)",
        "prompt": "Classical South Indian historical oil painting portraying the living tradition of the 28 Saiva Agamas. Inside an ancient Dravidian granite temple courtyard during temple consecration (Kumbhabhishekam), a master Temple Architect (Sthapati) holds carved brass tools and unfurls sacred palm leaf architectural plans (Silpa Sastras), while revered Sivacharya priests adorned with white vibhuti and rudraksha conduct Vedic homa fire rituals before a monumental granite Shiva Lingam. Majestic towering carved granite pillars with Yali motifs, hanging brass lamps, fragrant incense smoke, Chola period realism.",
        "negative_prompt": "modern clothes, concrete, plastic, digital artifacts, text, watermark, distorted hands, blurry, bad anatomy"
    },
    {
        "filename": "grade9_body_is_temple.jpg",
        "title": "தரம் 9 — உடலே ஆலயம் (Ullum Perungoil - Body is the Sacred Temple)",
        "prompt": "Mystical classical Indian spiritual oil painting illustrating Saint Thirumoolar's philosophy 'உள்ளம் பெருங்கோயில் ஊனுடம்பு ஆலயம்' (The Soul is the Great Sanctum, the Body is the Temple). A meditating Tamil yogi seated in serene padmasana with luminous chakras aligned along the spine. Subtle translucent architectural lines of a sacred Dravidian temple sanctum, gopuram, and golden kalasam seamlessly merge with the yogi's physical form. Golden divine light radiating from the heart center (Anahata), sacred temple courtyard, sunrise mist, transcendental realism.",
        "negative_prompt": "grotesque, dark, horror, modern clothes, text, watermark, bad anatomy, deformed limbs"
    },
    {
        "filename": "grade9_shaddarshanas_dialogue.jpg",
        "title": "தரம் 9 — பாரதத்தின் ஷட்தர்சனங்கள் (Six Indian Philosophical Darshanas Debate)",
        "prompt": "Classical South Indian oil painting depicting the great philosophical assembly of the Six Darshanas (Nyaya, Vaisheshika, Samkhya, Yoga, Mimamsa, Vedanta). Revered Tamil and Vedic scholars, rishis, and seekers seated beneath an ancient peepal tree in a tranquil riverside forest hermitage. Palm leaf manuscripts on low wooden peedams, spirited yet peaceful philosophical discourse, sacred vibhuti stripes, morning golden hour light breaking through canopy mist, Tanjore masterwork fine art.",
        "negative_prompt": "modern clothing, microphones, printed books, plastic, text, watermark, distorted faces, blurry"
    },
    {
        "filename": "grade10_pati_pasu_pasam.jpg",
        "title": "தரம் 10 — பதி பசு பாசம் (Pati-Pasu-Pasam Saiva Siddhanta Philosophy)",
        "prompt": "Allegorical classical South Indian spiritual oil painting representing Saiva Siddhanta's core doctrine: Pati (Lord Shiva), Pasu (the individual soul / Jiva), and Pasam (the threefold bond of Anava, Karma, Maya). Lord Shiva appears in serene benevolent cosmic form holding the deer of the mind, with divine grace (Arul) descending upon a devout soul depicted as a radiant cow and human seeker breaking free from dark swirling ethereal bonds into pure golden consciousness. Luminous spiritual aura, temple cosmic atmosphere.",
        "negative_prompt": "horror, demons, cartoon, anime, text, watermark, low quality, bad anatomy, modern elements"
    },
    {
        "filename": "grade10_temple_chariot_festival.jpg",
        "title": "தரம் 10 — தேர்த் திருவிழா (Grand Temple Chariot Festival - Ther Thiruvizha)",
        "prompt": "Magnificent classical South Indian historical painting depicting the grand temple chariot festival (Ther Thiruvizha) in Thiruvarur or Madurai. A colossal multi-tiered wooden temple chariot (Ratham) intricately hand-carved with thousands of sacred deities, draped in vibrant silk pennants and floral garlands. Thousands of joyful devotees in traditional white dhotis pulling the massive coir ropes in collective surrender. Ancient Dravidian gopuram in background, festival energy, morning sun, classical oil painting.",
        "negative_prompt": "modern cars, electric poles, tarmac road, jeans, t-shirts, text, watermark, low resolution"
    },
    {
        "filename": "grade11_nachiketas_yama.jpg",
        "title": "தரம் 11 — நசிகேதன் மற்றும் எமதர்மன் (Katha Upanishad - Nachiketas & Lord Yama Dialogue)",
        "prompt": "Classical Indian philosophical oil painting of young Nachiketas questioning Lord Yama from the Katha Upanishad. The brave, radiant boy-seeker Nachiketas with folded hands stands fearlessly in the hall of Lord Yama, rejecting kingdoms and gold, asking for the supreme secret of immortality and the Self (Atman). Lord Yama, majestic and crowned in ancient Vedic regalia, looks upon the youth with deep reverence and imparts the sacred knowledge of Om. Golden spiritual ambience, dramatic chiaroscuro.",
        "negative_prompt": "grotesque horror, demonic, modern clothes, text, watermark, cartoon, bad proportions"
    },
    {
        "filename": "grade11_pancha_koshas.jpg",
        "title": "தரம் 11 — பஞ்ச கோசங்கள் (The Five Sheaths of Human Existence)",
        "prompt": "Transcendental classical spiritual oil painting depicting the Five Koshas (Annamaya, Pranamaya, Manomaya, Vijnanamaya, Anandamaya). A serene human figure meditating in full lotus posture, with five concentric radiant luminous sheaths gently glowing around the body from physical earthy warmth to emerald breath, azure mental focus, golden wisdom light, and outermost diamond-white bliss (Anandamaya) merging with cosmic Paramatman. Sacred sacred geometry, temple aura.",
        "negative_prompt": "sci-fi neon, cyberpunk, modern, text, watermark, low quality, bad anatomy"
    },
    {
        "filename": "grade12_jivanmukti_36tattvas.jpg",
        "title": "தரம் 12 — ஜீவன்முக்தி & 36 தத்துவங்கள் (Jivanmukti & Transcendence of the 36 Tattvas)",
        "prompt": "Monumental classical Indian spiritual painting of an enlightened sage attaining Jivanmukti (liberation while living in the body). The sage sits motionless in nirvikalpa samadhi on a mountain ledge above the mist in the Western Ghats, eyes half-closed in boundless bliss. Below are symbolic subtle steps representing the 36 Tattvas of Saiva philosophy transcended, while above Lord Shiva Nataraja dances in the cosmic starlight. Transcendent golden and indigo harmony, museum masterpiece realism.",
        "negative_prompt": "dark, gloomy, text, watermark, cartoon, low resolution, bad anatomy, modern elements"
    },
    {
        "filename": "grade12_thayumanavar_universal.jpg",
        "title": "தரம் 12 — தாயுமானவ சுவாமிகள் (Saint Thayumanavar - Universal Compassion)",
        "prompt": "Classical South Indian oil painting of Saint Thayumanavar sitting under an ancient neem and vilva tree at Rockfort Tiruchirappalli overlooking the sacred Cauvery river. The saint with peaceful compassionate gaze, sacred vibhuti and rudraksha, holding palm leaves containing his universal hymns 'எல்லாரும் இன்புற்றிருக்க நினைப்பதுவே'. Gentle morning breeze, river reflecting temple gopuram, birds resting peacefully near his feet, radiant spiritual warmth.",
        "negative_prompt": "modern clothing, plastic, bridges with cars, text, watermark, cartoon, bad anatomy"
    },
    {
        "filename": "grade12_grihastha_nirvana.jpg",
        "title": "தரம் 12 — இல்லற தர்மமே அதிவேக முக்தி (Noble Grihastha Living as Supreme Path to Nirvana)",
        "prompt": "Masterpiece classical Tamil oil painting honoring noble family living (இல்லறம்) as the supreme and fastest path to spiritual liberation. An exemplary Tamil father and mother with their respectful children in their sacred home courtyard, surrounded by elderly parents, sharing grain with visiting guests and birds, with a glowing Shiva lingam altar inside the inner thinnai. Golden morning sun rays, harmony, dignity, absolute spiritual peace and family dharma, Raja Ravi Varma style oil on canvas.",
        "negative_prompt": "modern gadgets, plastic, western clothes, text, watermark, low quality, cartoon"
    }
]

THIRUKKURAL_PROMPTS = [
    {
        "chapter": 54,
        "filename": "54-pochchaavaamai/12-watchtower-dawn-clarity.jpg",
        "title": "அதிகாரம் 54: பொச்சாவாமை — விடியலில் கோட்டைக்காவலன் விழிப்புணர்வு",
        "prompt": "Classical South Indian oil painting depicting an ancient Chola fortress watchtower at dawn. A focused sentinel in traditional armor gripping a polished brass spear, looking out over the misty mountain frontier passes with unwavering vigilance and mindfulness. Morning sun cresting over the Western Ghats, oil on canvas."
    },
    {
        "chapter": 54,
        "filename": "54-pochchaavaamai/13-state-treasury-vigilance.jpg",
        "title": "அதிகாரம் 54: பொச்சாவாமை — கருவூலக் காவல் & கணக்கர் விழிப்பு",
        "prompt": "Classical South Indian historical oil painting of royal treasury officials and scribes meticulously auditing grain sacks and gold coins by candlelight in an ancient stone vault, unwavering vigilance against the slightest negligence, chiaroscuro lighting."
    },
    {
        "chapter": 57,
        "filename": "57-veruvantha-seyyaamai/12-just-king-merciful-judgment.jpg",
        "title": "அதிகாரம் 57: வெருவந்த செய்யாமை — அஞ்சத்தக்க கொடுஞ்செயல் செய்யாமை",
        "prompt": "Classical South Indian royal court oil painting of a righteous Tamil monarch seated on an intricately carved wooden throne, listening with compassion and restraint to a humble subject, refusing harsh penalties in favor of gentle righteous counsel, noble durbar."
    },
    {
        "chapter": 57,
        "filename": "57-veruvantha-seyyaamai/13-peaceful-subjects-royal-court.jpg",
        "title": "அதிகாரம் 57: வெருவந்த செய்யாமை — அச்சமின்றி வாழும் நாட்டு மக்கள்",
        "prompt": "Classical South Indian oil painting of a thriving ancient village market where citizens, farmers, and artisans conduct trade with joy and fearlessness under the protection of a benevolent, merciful sovereign, rich golden light."
    },
    {
        "chapter": 61,
        "filename": "61-madiyinmai/12-blacksmith-forge-diligence.jpg",
        "title": "அதிகாரம் 61: மடியின்மை — விடாமுயற்சியோடு உழைக்கும் உலைக்களப் பட்டறை",
        "prompt": "Classical South Indian oil painting of ancient Tamil blacksmiths and artisans working vigorously at a glowing bronze and iron forge at dawn, sparks flying, muscular arms wielding hammers in relentless effort to create plowshares, no sloth or delay."
    },
    {
        "chapter": 61,
        "filename": "61-madiyinmai/13-prosperous-homestead-harvest.jpg",
        "title": "அதிகாரம் 61: மடியின்மை — சோம்பலின்றி உழைத்த உழவர் குடும்பத்தின் வளமான இல்லம்",
        "prompt": "Classical South Indian oil painting of a prosperous Tamil farming homestead bathed in morning light, overflowing granaries of golden paddy, cattle grazing peacefully, industrious family rejoicing in the fruits of diligence and ethical work."
    }
]

def make_cell(cell_type, source):
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    }

def build_notebook():
    cells = []
    
    # Header markdown
    cells.append(make_cell("markdown", """# 🎨 குரு குல தேசம் (Guru Kula Desam) — AI Artwork Generator
### Dedicated GPU Colab Server for nagaraj957@gmail.com
This notebook uses **SDXL-Lightning (ByteDance 4-Step UNet on Stable Diffusion XL)** to rapidly generate the remaining classical South Indian educational illustrations and Thirukkural visual series at native **1024×768 / 1024×1024 high resolution**.

- **Speed:** ~2 to 3 seconds per image on free Colab T4 GPU!
- **Auth:** No HuggingFace token or payment required (uses open weights).
- **Style:** Authentic classical South Indian academic realism, Raja Ravi Varma oil aesthetic, Chola architecture, sacred temple lighting.
- **Output:** Automatically packages all generated images into `gurukuladesam_artworks.zip` with exact folder paths ready to be dropped into the website repository.
"""))

    # Step 1: Install
    cells.append(make_cell("code", """# Step 1: Install required high-performance generation libraries
!pip install -q diffusers transformers accelerate safetensors torch torchvision

import torch
print("PyTorch Version:", torch.__version__)
if torch.cuda.is_available():
    print(f"✅ GPU Detected: {torch.cuda.get_device_name(0)}")
    print(f"✅ VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
else:
    print("⚠️ WARNING: GPU not detected! Please go to Runtime -> Change runtime type -> Select T4 GPU.")
"""))

    # Step 2: Pipeline
    cells.append(make_cell("code", """# Step 2: Initialize SDXL-Lightning Pipeline (4-step ultra-fast 1024px generator)
from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
import os

base = "stabilityai/stable-diffusion-xl-base-1.0"
repo = "ByteDance/SDXL-Lightning"
ckpt = "sdxl_lightning_4step_unet.safetensors"

print("⏳ Loading SDXL Base + SDXL-Lightning 4-step UNet (takes ~1-2 mins)...")

# Load UNet
unet = UNet2DConditionModel.from_config(base, subfolder="unet").to("cuda", torch.float16)
unet.load_state_dict(load_file(hf_hub_download(repo, ckpt), device="cuda"))

# Load Pipeline
pipe = StableDiffusionXLPipeline.from_pretrained(
    base,
    unet=unet,
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")

# Ensure sampler uses trailing timesteps
pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")

print("✅ Pipeline loaded and ready for high-speed generation!")
"""))

    # Step 3: Lesson Artworks
    lesson_prompts_json = json.dumps(LESSON_PROMPTS, indent=4, ensure_ascii=False)
    cells.append(make_cell("code", f"""# Step 3: Generate the Remaining 11 Coursebook Lesson Illustrations (Grades 8 to 12)
import os
from PIL import Image
from IPython.display import display

output_dir = "assets/images/lessons"
os.makedirs(output_dir, exist_ok=True)

lesson_tasks = {lesson_prompts_json}

print(f"🚀 Starting generation of {{len(lesson_tasks)}} Coursebook Master Artworks...")

for idx, task in enumerate(lesson_tasks, 1):
    out_path = os.path.join(output_dir, task['filename'])
    print(f"\\n[{{idx}}/{{len(lesson_tasks)}}] Generating: {{task['title']}} -> {{task['filename']}}")
    
    # 4-step generation with guidance_scale=0 for Lightning
    image = pipe(
        prompt=task['prompt'],
        negative_prompt=task['negative_prompt'],
        num_inference_steps=4,
        guidance_scale=0.0,
        width=1024,
        height=768
    ).images[0]
    
    image.save(out_path, quality=95)
    print(f" Saved: {{out_path}} ({{image.size[0]}}x{{image.size[1]}})")
    # Preview
    display(image.resize((512, 384)))

print("\\n All 11 Coursebook Lesson Artworks successfully generated!")
"""))

    # Step 4: Thirukkural Visuals
    thirukkural_prompts_json = json.dumps(THIRUKKURAL_PROMPTS, indent=4, ensure_ascii=False)
    cells.append(make_cell("code", f"""# Step 4: Generate Thirukkural Chapter Visuals (Chapters 54, 57, 61)
tk_tasks = {thirukkural_prompts_json}

base_tk_dir = "production/visuals/thirukkural"

print(f"🚀 Generating {{len(tk_tasks)}} Thirukkural Chapter Visuals...")

for idx, task in enumerate(tk_tasks, 1):
    out_path = os.path.join(base_tk_dir, task['filename'])
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    print(f"\\n[{{idx}}/{{len(tk_tasks)}}] Generating: {{task['title']}} -> {{task['filename']}}")
    
    image = pipe(
        prompt=task['prompt'],
        negative_prompt="modern elements, distorted limbs, blurry, text, watermark, bad anatomy",
        num_inference_steps=4,
        guidance_scale=0.0,
        width=1024,
        height=768
    ).images[0]
    
    image.save(out_path, quality=95)
    print(f" Saved: {{out_path}}")

print("\\n All Thirukkural visuals successfully generated!")
"""))

    # Step 5: Packaging & Download
    cells.append(make_cell("code", """# Step 5: Create Zip Archive and Trigger Instant Download to Your Machine
import shutil
from google.colab import files

zip_filename = "gurukuladesam_artworks.zip"

print(f"📦 Packaging all generated images into {zip_filename}...")
# Create zip containing assets/ and production/ folders
shutil.make_archive("gurukuladesam_artworks", 'zip', root_dir=".", base_dir="assets")

# Append production visuals if present
if os.path.exists("production"):
    import zipfile
    with zipfile.ZipFile(zip_filename, 'a', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files_list in os.walk("production"):
            for file in files_list:
                full_path = os.path.join(root, file)
                zf.write(full_path, full_path)

print(f"✅ Archive created! Size: {os.path.getsize(zip_filename) / 1024 / 1024:.2f} MB")
print("⬇️ Triggering browser download now...")
files.download(zip_filename)
"""))

    notebook = {
        "nbformat": 4,
        "nbformat_minor": 0,
        "metadata": {
            "accelerator": "GPU",
            "colab": {
                "provenance": [],
                "authorship_tag": "GuruKulaDesam",
                "include_colab_link": True
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "cells": cells
    }
    
    nb_path = "colab_generate_gurukulam_artworks.ipynb"
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
        
    print(f"Generated Colab Notebook: {nb_path} with {len(cells)} cells.")

if __name__ == '__main__':
    build_notebook()
