from PIL import Image
import numpy as np
import random
import csv
from tqdm import tqdm

# --- 設定 ---
INPUT_PATH = 'chaos/map/default.png'
OUTPUT_IMAGE_PATH = 'chaos/map/provinces.png'
DEFINITION_CSV_PATH = 'chaos/map/definition.csv'
PROVINCE_COUNT = 13375
DEFAULT_TYPE = 'land'
DEFAULT_CONTINENT = '1'

# --- 有効ピクセルの抽出 ---
image = Image.open(INPUT_PATH).convert('RGB')
pixels = np.array(image)
height, width = pixels.shape[:2]

valid_coords = [
    (x, y) for y in range(height) for x in range(width)
    if tuple(pixels[y, x]) != (0, 0, 0)
]

if len(valid_coords) < PROVINCE_COUNT:
    raise ValueError(f"プロヴィンス領域が不足しています（必要: {PROVINCE_COUNT}, 実際: {len(valid_coords)}）")

random.shuffle(valid_coords)

# --- プロヴィンス領域を分割 ---
province_coords = [[] for _ in range(PROVINCE_COUNT)]
for i, coord in enumerate(valid_coords):
    province_coords[i % PROVINCE_COUNT].append(coord)

# --- 重複なしユニーク色生成 ---
def generate_unique_colors(n):
    colors = set()
    while len(colors) < n:
        r = random.randint(1, 255)
        g = random.randint(0, 255)
        b = random.randint(1, 255)  # 0,0,0 禁止
        if (r, g, b) != (0, 0, 0):
            colors.add((r, g, b))
    return list(colors)

unique_colors = generate_unique_colors(PROVINCE_COUNT)

# --- province ID → 色 対応表 ---
province_id_to_color = {
    i + 1: color for i, color in enumerate(unique_colors)
}

# --- 出力画像作成 ---
output_image = Image.new('RGB', (width, height), (0, 0, 0))

for pid, coords in enumerate(tqdm(province_coords, desc="プロヴィンス塗り分け"), start=1):
    color = province_id_to_color[pid]
    for x, y in coords:
        output_image.putpixel((x, y), color)

output_image.save(OUTPUT_IMAGE_PATH)

# --- definition.csv 出力 ---
with open(DEFINITION_CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    for pid, color in province_id_to_color.items():
        r, g, b = color
        writer.writerow([pid, DEFAULT_TYPE, r, g, b, DEFAULT_CONTINENT, f'province_{pid}'])

print(f"✅ 完了: {PROVINCE_COUNT} プロヴィンスをランダムに生成・塗り分けました")
print(f"🖼️ provinces.png → {OUTPUT_IMAGE_PATH}")
print(f"📄 definition.csv → {DEFINITION_CSV_PATH}")
