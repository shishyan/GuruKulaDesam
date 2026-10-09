"""Batch comment poster for Topic videos using Playwright browser automation.
Iterates over all Topic tracks that have matching verified lyrics & meaning from our catalog/films,
and posts them as owner comments.
"""
import sys
import time
import json
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / 'production' / 'youtube_backup'
LOG = B / 'playwright_comment_log.jsonl'
CDP_URL = "http://127.0.0.1:9222"

def format_comment(text):
    lines = text.splitlines()
    body_lines = []
    capture = False
    for l in lines:
        if "பாடல் வரிகள்" in l:
            capture = True
        if capture:
            if l.startswith("http") and "gurukuladesam" in l:
                body_lines.append(l)
                break
            body_lines.append(l)
    return "\n".join(body_lines).strip()

def load_ready_pairs():
    f2o = json.load(open(B / 'film_to_original.json', encoding='utf-8'))
    applied = {json.loads(l)['id'] for l in open(B / 'apply_log.jsonl', encoding='utf-8') if json.loads(l).get('ok') and not json.loads(l).get('rollback')}
    vids = {v['id']: v for v in json.load(open(B / 'videos.json', encoding='utf-8'))}
    topics = {v['id']: v for v in json.load(open(B / 'playlist_only_videos.json', encoding='utf-8'))}
    
    done = set()
    if LOG.exists():
        for l in open(LOG, encoding='utf-8'):
            try:
                r = json.loads(l)
                if r.get('ok'): done.add(r['id'])
            except:
                pass
                
    pairs = []
    seen = set()
    for m in f2o:
        orig = m['original']
        film = m['film']
        if orig in done or orig in seen:
            continue
        if orig in topics and film in applied:
            desc = vids[film]['snippet']['description']
            if 'பாடல் வரிகள்' in desc:
                comment_text = format_comment(desc)
                if len(comment_text) > 100:
                    pairs.append({
                        'topic_id': orig,
                        'film_id': film,
                        'topic_title': topics[orig]['snippet']['title'],
                        'comment_text': comment_text
                    })
                    seen.add(orig)
    
    # Also load from catalog.json for topic tracks directly having lyrics
    cat = json.load(open(ROOT / 'assets/data/catalog.json', encoding='utf-8'))
    for vname in ['thirukkural', 'vinayagar', 'murugan', 'shiva', 'amman', 'vishnu_krishna']:
        for item in cat.get(vname, []):
            vid = item['id']
            if vid in topics and vid not in done and vid not in seen:
                lyr = (item.get('lyrics') or '').strip()
                mean = (item.get('meaning') or '').strip()
                if len(lyr) > 150:
                    comment_text = f"பாடல் வரிகள் (Lyrics)\n{lyr}\n\nபொருள் (Meaning)\n{mean}\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
                    pairs.append({
                        'topic_id': vid,
                        'film_id': vid,
                        'topic_title': topics[vid]['snippet']['title'],
                        'comment_text': comment_text
                    })
                    seen.add(vid)
    return pairs

def post_comment(page, video_id, comment_text):
    url = f"https://www.youtube.com/watch?v={video_id}"
    page.goto(url, wait_until='domcontentloaded', timeout=30000)
    time.sleep(3)
    
    for _ in range(5):
        page.evaluate("window.scrollBy(0, 600)")
        time.sleep(1)
        
    placeholder = page.locator('#placeholder-area, #simplebox-placeholder').first
    try:
        placeholder.wait_for(state='visible', timeout=8000)
    except Exception:
        # One extra scroll attempt
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(2)
        
    if not placeholder.is_visible():
        return False, "Placeholder not visible"
        
    placeholder.click()
    time.sleep(1.5)
    
    input_box = page.locator('#contenteditable-root').first
    if not input_box.is_visible():
        return False, "Input box not visible"
        
    page.evaluate("""({text}) => {
        const el = document.querySelector('#contenteditable-root');
        el.focus();
        document.execCommand('insertText', false, text);
    }""", {'text': comment_text})
    time.sleep(1)
    
    submit_btn = page.locator('#submit-button button, ytd-button-renderer#submit-button').first
    if submit_btn.is_enabled():
        submit_btn.click()
        time.sleep(4)
        return True, "Success"
    else:
        return False, "Submit button disabled"

if __name__ == '__main__':
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    pairs = load_ready_pairs()
    print(f"Total ready Topic videos with lyrics: {len(pairs)}")
    print(f"Processing batch of {min(limit, len(pairs))} videos...")
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        # Open one dedicated page for YouTube commenting
        page = context.new_page()
        
        count = 0
        for item in pairs[:limit]:
            vid = item['topic_id']
            title = item['topic_title']
            text = item['comment_text']
            print(f"\n[{count+1}/{limit}] Commenting on {vid} ({title[:30]})...", flush=True)
            
            try:
                ok, msg = post_comment(page, vid, text)
            except Exception as e:
                ok, msg = False, str(e)
                print(f"  -> EXCEPTION: {e}", flush=True)
                
            log_entry = {'id': vid, 'film': item['film_id'], 'ok': ok, 'msg': msg, 'title': title}
            with open(LOG, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
            if ok:
                print(f"  -> SUCCESS", flush=True)
                count += 1
            else:
                print(f"  -> FAILED: {msg}", flush=True)
            time.sleep(4)
            
        print(f"\nDone! Successfully posted {count} comments.")
