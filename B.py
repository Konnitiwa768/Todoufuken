from PIL import Image
import numpy as np
import random
import csv
from tqdm import tqdm
from skimage.measure import label

# --- 設定 ---
INPUT_PATH = 'chaos/map/default.png'
OUTPUT_IMAGE_PATH = 'chaos/map/provinces.png'
DEFINITION_CSV_PATH = 'chaos/map/definition.csv'
PROVINCE_COUNT = 13375
DEFAULT_TYPE = 'land'
DEFAULT_CONTINENT = '1'

# --- 画像読み込みと処理準備 ---
image = Image.open(INPUT_PATH).convert('RGB')
pixels = np.array(image)
height, width = pixels.shape[:2]

# 黒以外のユニーク色を取得
unique_colors = list({tuple(pixels[y, x]) for y in range(height) for x in range(width) if tuple(pixels[y, x]) != (0, 0, 0)})

# --- 色ごとに領域を抽出しラベリング ---
region_pixels = []
for base_color in unique_colors:
    mask = np.all(pixels == base_color, axis=2)
    labeled = label(mask, connectivity=1)  # 連結領域に番号付け
    for label_id in range(1, labeled.max() + 1):
        coords = list(zip(*np.where(labeled == label_id)))
        if len(coords) > 5:  # 小さすぎる領域は無視
            region_pixels.append(coords)

# --- 領域シャッフルとプロヴィンス分割 ---
random.shuffle(region_pixels)
all_coords = [coord for region in region_pixels for coord in region]
if len(all_coords) < PROVINCE_COUNT:
    raise ValueError(f"プロヴィンス領域が不足（必要: {PROVINCE_COUNT}, 実際: {len(all_coords)}）")

province_coords = [[] for _ in range(PROVINCE_COUNT)]
for i, coord in enumerate(all_coords):
    province_coords[i % PROVINCE_COUNT].append(coord)

# --- ユニーク色を生成 ---
def generate_unique_colors(n):
    colors = set()
    while len(colors) < n:
        r, g, b = random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)
        if (r, g, b) != (0, 0, 0):
            colors.add((r, g, b))
    return list(colors)

province_colors = generate_unique_colors(PROVINCE_COUNT)
province_id_to_color = {i + 1: c for i, c in enumerate(province_colors)}

# --- 画像とCSV出力 ---
output_image = Image.new('RGB', (width, height), (0, 0, 0))
for pid, coords in enumerate(tqdm(province_coords, desc="プロヴィンス塗り分け"), start=1):
    color = province_id_to_color[pid]
    for y, x in coords:
        output_image.putpixel((x, y), color)

output_image.save(OUTPUT_IMAGE_PATH)

with open(DEFINITION_CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    for pid, color in province_id_to_color.items():
        r, g, b = color
        writer.writerow([pid, DEFAULT_TYPE, r, g, b, DEFAULT_CONTINENT, f'province_{pid}'])

print(f"✅ 完了: {PROVINCE_COUNT} プロヴィンスを図形ベースでランダムに生成・塗り分けました")
