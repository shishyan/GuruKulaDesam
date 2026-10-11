import subprocess
from pathlib import Path

card_file = Path('renders/temp_flow_YxP_uh3dM18/lyrics_cards/card_003.txt').resolve()
txt_path = str(card_file).replace('\\', '/').replace(':', '\\:')
video_file = Path('renders/temp_flow_YxP_uh3dM18/looped_video.mp4').resolve()
font_path = 'C\\:/Windows/Fonts/NirmalaB.ttf'

for spacing in [8, 5, 2, 0]:
    out_img = f'renders/test_spacing_{spacing}.png'
    vf = (
        f"drawtext=fontfile='{font_path}':"
        f"textfile='{txt_path}':"
        f"fontcolor=white:fontsize=24:x=(w-text_w)/2:y=h-text_h-35:"
        f"text_shaping=1:borderw=2:bordercolor=black:"
        f"box=1:boxcolor=black@0.5:boxborderw=10:line_spacing={spacing}"
    )
    cmd = ['ffmpeg', '-y', '-ss', '00:00:20', '-i', str(video_file), '-vf', vf, '-vframes', '1', out_img]
    subprocess.run(cmd, capture_output=True, check=True)
    print(f'Rendered {out_img}')

