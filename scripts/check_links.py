with open(r'C:\GitHub\Gurukuladesam\puranas.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# check all elements inside <main class="purana-page-wrap">
main_part = re.search(r'<main[^>]*class="purana-page-wrap".*?</main>', text, re.DOTALL)
if main_part:
    print('Main length:', len(main_part.group(0)))
    # print lines of main_part that are not puranaBookList or puranaReadingArea
    lines = main_part.group(0).split('\n')
    for l in lines[:40]:
        print(l.encode('ascii', 'replace').decode('ascii'))
