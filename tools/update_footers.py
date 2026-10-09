import glob

files = glob.glob('*.html')
count = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        text = fh.read()
    orig = text
    text = text.replace('1. பாலப் பருவம் (தரம் 1–4) • அற அடித்தளம்', '1. பாலப் பருவம் (தரம் 1–5) • தொடக்கக் கல்வி &amp; 3 நூல்கள்')
    text = text.replace('href="tharam-5.html">2. இளம் பருவம் (தரம் 5–8)', 'href="tharam-6.html">2. இளம் பருவம் (தரம் 6–8)')
    text = text.replace('2. இளம் பருவம் (தரம் 5–8) • பண்பாடு &amp; நெறி', '2. இளம் பருவம் (தரம் 6–8) • நடுநிலைப் பள்ளி &amp; 7 நூல்கள்')
    if text != orig:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(text)
        count += 1
print(f"Updated footer links in {count} files.")
