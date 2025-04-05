import cv2
import os
import numpy as np
import imageio.v2 as imageio

# 設定
image_folder = "./"
output_gif = "slideshow.gif"

fps = 30  # アニメーションのなめらかさ（1秒=30フレーム）
slide_duration_sec = 1.0
pause_duration_sec = 3.0

slide_frames = int(fps * slide_duration_sec)
pause_frames = int(fps * pause_duration_sec)

# PNG画像を取得
image_files = sorted([
    os.path.join(image_folder, f)
    for f in os.listdir(image_folder)
    if f.lower().endswith(".png")
])

if len(image_files) < 2:
    print("画像が2枚以上必要です。")
    exit()

# 画像を統一サイズで読み込み
base_img = cv2.imread(image_files[0])
h, w, _ = base_img.shape
images = [cv2.resize(cv2.imread(f), (w, h)) for f in image_files]

frames = []

# スライドショー作成（ループのため最後→最初も入れる）
for i in range(len(images)):
    img1 = images[i]
    img2 = images[(i + 1) % len(images)]  # 最後→最初

    # 静止表示（3秒）
    for _ in range(pause_frames):
        frames.append(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))

    # スライドアニメーション（1秒）
    for step in range(slide_frames):
        alpha = step / slide_frames
        shift = int(alpha * w)

        canvas = np.zeros_like(img1)
        canvas[:, :w - shift] = img1[:, shift:]
        canvas[:, w - shift:] = img2[:, :shift]

        frames.append(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))

# GIFとして保存（duration=フレーム単位、ループあり）
imageio.mimsave(output_gif, frames, duration=1 / fps, loop=0)
print(f"✅ GIF保存完了：{output_gif}")
