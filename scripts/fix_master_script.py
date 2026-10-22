import re

with open(r'C:\GitHub\Gurukuladesam\scripts\generate_master_108_authentic_stories.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the loop in main()
old_main = """def main():
    print("Generating 108 authentic unique children stories...")
    chapters = []
    for item in TOPICS_FOR_REST:
        num, t_ta, t_en = item
        ch = generate_story(num, t_ta, t_en)
        chapters.append(ch)"""

new_main = """def main():
    print("Generating 108 authentic unique children stories...")
    chapters = []
    # 1 to 5 from MASTER_108
    for item in MASTER_108:
        num, t_ta, t_en, syn, p1, p2, p3, p4 = item
        ch = generate_story(num, t_ta, t_en)
        chapters.append(ch)
    # 6 to 108 from TOPICS_FOR_REST
    for item in TOPICS_FOR_REST:
        num, t_ta, t_en = item
        ch = generate_story(num, t_ta, t_en)
        chapters.append(ch)"""

code = code.replace(old_main, new_main)
with open(r'C:\GitHub\Gurukuladesam\scripts\generate_master_108_authentic_stories.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated script to include all 1..108 chapters!")
