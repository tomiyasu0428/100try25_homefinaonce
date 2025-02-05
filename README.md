# My Budget App

このプロジェクトは、Python (Flask) を用いたシンプルな家計簿WEBアプリです。

## 機能
- **収支入力**：日付、金額、カテゴリ（収入・支出）、メモの入力フォーム  
- **記録一覧**：入力済みの収支レコードを一覧表示、編集・削除が可能  
- **集計機能**：今月の収支合計と、各カテゴリの割合を円グラフで表示（Chart.js利用）  
- **レシート読み取り**：アップロードされた画像を受け取り、OCR処理（pytesseractとPillow使用）でテキストを抽出

## 技術スタック
- Python 3.x
- Flask 3.1.0
- Flask-WTF 1.2.2
- Flask-SQLAlchemy 3.1.1
- SQLite
- Chart.js (CDN利用)
- Pillow, pytesseract (OCR機能)

## セットアップ方法

1. リポジトリをクローン  
   ```bash
   git clone <repository_url>
   cd my_budget_app
