import glob
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

# 写真の保存場所
PHOTO_DIR = 'photos'
photo_files = sorted(glob.glob(os.path.join(PHOTO_DIR, '*.jpg')))
num_photos = len(photo_files)

print(f"検出された写真の枚数: {num_photos}枚")

# 写真が3枚未満の場合は解析を開始せず終了
if num_photos < 3:
    print("写真が3枚未満（Step 0〜2未完了）のため、最適HSV計算とグラフ作成を待機します。")
    exit(0)

# --- 最適HSV閾値の決定（Step 0, 1, 2の3枚を使用） ---
# ※既存の固定閾値または自動計算ロジックを設定
# ここでは緑色検出の標準的なHSV範囲を設定（必要に応じて数値を調整可能）
hsv_min = np.array([30, 40, 40])
hsv_max = np.array([85, 255, 255])

# --- 各写真の緑色画素数の割合計算 ---
green_ratios = []
for img_path in photo_files:
    img = cv2.imread(img_path)
    if img is None:
        continue
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsv_min, hsv_max)

    # 画像全体に対する緑色画素の割合 (%)
    ratio = (np.count_nonzero(mask) / mask.size) * 100
    green_ratios.append(ratio)

# --- グラフの描画とプロット（点 ＋ 曲線） ---
steps = list(range(len(green_ratios)))
plt.figure(figsize=(8, 5))

# 点プロットと折れ線/曲線接続
plt.plot(steps, green_ratios, marker='o', linestyle='-', color='green', linewidth=2, markersize=8, label='Green Pixel Ratio (%)')

plt.title('Negi Growth Analysis Graph', fontsize=14)
plt.xlabel('Step (Photo Index)', fontsize=12)
plt.ylabel('Green Pixel Ratio (%)', fontsize=12)
plt.xticks(steps) # Step数を整数で表示
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

# 写真と同じフォルダ (photos/) にグラフ画像を保存
output_graph_path = os.path.join(PHOTO_DIR, 'negi_growth_graph.png')
plt.savefig(output_graph_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"解析が完了しました。グラフを出力しました: {output_graph_path}")
