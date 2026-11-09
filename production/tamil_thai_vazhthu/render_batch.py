import subprocess
import time
from pathlib import Path

workdir = Path('/home/antigravity/shishyan/GuruKulaDesam/production/tamil_thai_vazhthu')
total_dur = 234.03
seg_len = 15.0
num_segs = int(total_dur // seg_len) + (1 if total_dur % seg_len != 0 else 0)

print(f"Total duration: {total_dur}s, Number of segments: {num_segs}")

seg_files = []
for i in range(num_segs):
    st = i * seg_len
    en = min(total_dur, (i + 1) * seg_len)
    dur = en - st
    out_seg = workdir / f'seg_{i:02d}.mp4'
    seg_files.append(out_seg)
    
    if out_seg.exists() and out_seg.stat().st_size > 100000:
        print(f"Segment {i:02d} already exists ({out_seg.stat().st_size} bytes), skipping...")
        continue

    print(f"Rendering segment {i:02d}/{num_segs-1}: {st:.2f}s -> {en:.2f}s (dur={dur:.2f}s)...")
    t0 = time.time()
    
    is_last = (i == num_segs - 1)
    if is_last:
        fade_st = max(0.0, dur - 3.0)
        audio_filter = f'[1:a]atrim=0:{dur},asetpts=PTS-STARTPTS,afade=t=out:st={fade_st:.2f}:d=3.0[a_seg]'
    else:
        audio_filter = f'[1:a]atrim=0:{dur},asetpts=PTS-STARTPTS[a_seg]'

    cmd = [
        'ffmpeg', '-y',
        '-ss', str(st), '-i', str(workdir / 'raw_input.mp4'),
        '-ss', str(st), '-i', str(workdir / 'raw_input.mp4'),
        '-stream_loop', '-1', '-i', str(workdir / 'upward_rainbow_rain_loop.mp4'),
        '-stream_loop', '-1', '-i', str(workdir / 'perimeter_mist_loop.mp4'),
        '-loop', '1', '-t', str(dur), '-i', str(workdir / 'sacred_overlay_1080p.png'),
        '-filter_complex', f'''
            [0:v]trim=0:{dur},setpts=PTS-STARTPTS,fps=30,scale=1920:1080,colorbalance=rs=-0.035:gs=0.01:bs=0.065:rm=-0.025:gm=0.01:bm=0.05:rh=-0.02:gh=0.005:bh=0.04,format=rgba[v_base];
            [2:v]trim=0:{dur},setpts=PTS-STARTPTS,fps=30,scale=1920:1080,format=rgba[v_rain];
            [v_base][v_rain]blend=all_mode=screen:all_opacity=0.35,format=rgba[v_rained];
            [3:v]trim=0:{dur},setpts=PTS-STARTPTS,fps=30,scale=1920:1080,format=rgba[v_mist];
            [v_rained][v_mist]blend=all_mode=screen:all_opacity=0.25,format=rgba[v_misted];
            [4:v]scale=1920:1080,format=rgba[v_overlay];
            [v_misted][v_overlay]overlay=0:0:format=auto[v_framed];
            [v_framed]ass={workdir}/tamil_thai_vazhthu_master.ass,format=yuv420p[v_out];
            {audio_filter}
        ''',
        '-map', '[v_out]', '-map', '[a_seg]',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '20', '-threads', '4',
        '-c:a', 'aac', '-b:a', '320k', '-ar', '48000',
        '-t', str(dur),
        str(out_seg)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error rendering segment {i:02d}:\n{res.stderr}")
        exit(1)
    print(f"Segment {i:02d} rendered in {time.time() - t0:.1f}s ({out_seg.stat().st_size} bytes)")

# Concat
concat_list = workdir / 'concat_list.txt'
with open(concat_list, 'w') as f:
    for seg in seg_files:
        f.write(f"file '{seg.name}'\n")

print("Concatenating all segments into master video...")
master_out = workdir / 'tamil_thai_vazhthu_1080p_master.mp4'
concat_cmd = [
    'ffmpeg', '-y',
    '-f', 'concat', '-safe', '0',
    '-i', str(concat_list),
    '-c', 'copy',
    str(master_out)
]
res = subprocess.run(concat_cmd, capture_output=True, text=True)
if res.returncode != 0:
    print(f"Concat failed:\n{res.stderr}")
    exit(1)

print(f"Master created successfully: {master_out} ({master_out.stat().st_size} bytes)")
