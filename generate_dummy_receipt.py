from PIL import Image, ImageDraw, ImageFont
import datetime
import os

# 画像のサイズや背景色を設定
width, height = 600, 800
background_color = (255, 255, 255)  # 白
text_color = (0, 0, 0)  # 黒

# 新しい画像を生成
image = Image.new("RGB", (width, height), background_color)
draw = ImageDraw.Draw(image)

# フォントの設定（macOSの日本語フォントを使用）
font_path = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"  # macOSの日本語フォント
if not os.path.exists(font_path):
    font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"  # 代替フォント
if not os.path.exists(font_path):
    print("警告: 日本語フォントが見つかりません。デフォルトフォントを使用します。")
    font = ImageFont.load_default()
else:
    font = ImageFont.truetype(font_path, 20)

# ダミーのレシート内容（例）
now = datetime.datetime.now().strftime("%Y/%m/%d")
lines = [
    "ABCスーパー",
    "〒123-4567 東京都新宿区西新宿1-1-1",
    "------------------------------",
    f"日付: {now}",
    "------------------------------",
    "商品名        数量   単価   金額",
    "りんご         2     100   200",
    "牛乳           1     150   150",
    "パン           1     120   120",
    "------------------------------",
    "小計:                        470",
    "消費税:                      38",
    "合計:                        508",
    "------------------------------",
    "お買い上げありがとうございます！",
    "またのお越しをお待ちしております。",
]

# テキスト描画の開始位置と行間を設定
x, y = 50, 50
line_height = 30

for line in lines:
    draw.text((x, y), line, font=font, fill=text_color)
    y += line_height

# 画像ファイルとして保存
image.save("dummy_receipt.jpg")
print("ダミーのレシート画像を生成しました: dummy_receipt.jpg")
