import os, subprocess, json

dl = os.path.expanduser("~/Downloads")
src_video = os.path.join(dl, "Woman_reading_book_in_temple_20261012205600.mp4")
cog_ext = os.path.join(dl, "Divine_Reading_cogvideo.mp4")
ltx_ext = os.path.join(dl, "Divine_Reading_extension.mp4")

out_14s = os.path.join(dl, "Woman_reading_book_in_temple_Extended_14s.mp4")
out_18s = os.path.join(dl, "Woman_reading_book_in_temple_Extended_18s.mp4")

os.makedirs("production/temp_extend", exist_ok=True)

# 1. Normalize original 8s clip (1280x720, 24fps, high quality H.264)
p1 = "production/temp_extend/part1_orig.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", src_video,
    "-vf", "scale=1280:720:flags=lanczos,fps=24,format=yuv420p",
    "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-an", p1
], check=True)

# 2. Upscale & motion-interpolate CogVideo extension (6.12s -> 1280x720 @ 24fps with unsharp mask)
p2 = "production/temp_extend/part2_cog_24fps.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", cog_ext,
    "-vf", "minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,scale=1280:720:flags=lanczos,unsharp=5:5:0.8:5:5:0.0,format=yuv420p",
    "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-an", p2
], check=True)

# 3. Upscale & motion-interpolate LTX extension (3.57s -> 1280x720 @ 24fps)
p3 = "production/temp_extend/part3_ltx_24fps.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", ltx_ext,
    "-vf", "minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,scale=1280:720:flags=lanczos,unsharp=5:5:0.8:5:5:0.0,format=yuv420p",
    "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-an", p3
], check=True)

# 4. Concatenate Original (8s) + CogVideo (6.12s) -> 14.12s seamless extended master
concat_14_txt = "production/temp_extend/concat_14.txt"
with open(concat_14_txt, "w", encoding="utf-8") as f:
    f.write(f"file '{os.path.abspath(p1).replace(chr(92), '/')}'\n")
    f.write(f"file '{os.path.abspath(p2).replace(chr(92), '/')}'\n")

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_14_txt,
    "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p", out_14s
], check=True)

# 5. Concatenate Original (8s) + CogVideo (6.12s) + LTX (3.57s) -> 17.7s extended master
concat_18_txt = "production/temp_extend/concat_18.txt"
with open(concat_18_txt, "w", encoding="utf-8") as f:
    f.write(f"file '{os.path.abspath(p1).replace(chr(92), '/')}'\n")
    f.write(f"file '{os.path.abspath(p2).replace(chr(92), '/')}'\n")
    f.write(f"file '{os.path.abspath(p3).replace(chr(92), '/')}'\n")

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_18_txt,
    "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p", out_18s
], check=True)

for out_f in [out_14s, out_18s]:
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", out_f]
    res = subprocess.run(cmd, capture_output=True, text=True)
    info = json.loads(res.stdout)
    v = [s for s in info.get("streams", []) if s.get("codec_type") == "video"][0]
    sz = os.path.getsize(out_f) / (1024 * 1024)
    print(f"Created: {out_f} | {v.get('width')}x{v.get('height')} @ {v.get('r_frame_rate')} fps | Duration: {v.get('duration')}s | Size: {sz:.2f} MB")
