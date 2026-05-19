# generate_index.py
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

# 設定（検索対象フォルダと出力ファイル）
HTML_DIR = Path('html_files')
OUTPUT_FILE = Path('index.html')

def get_file_info(filepath):
    """ファイルのタイトルとGitの最終更新日時を取得する"""
    # タイトルの取得（<title>タグが存在しない場合はファイル名をフォールバックとして使用）
    title = filepath.name
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if match:
                title = match.group(1).strip()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

    # 更新日時の取得（Gitのコミット履歴から取得し、正確な更新日を保証する）
    update_date = ""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%cI', str(filepath)],
            capture_output=True, text=True, check=True
        )
        date_str = result.stdout.strip()
        if date_str:
            dt = datetime.fromisoformat(date_str)
            update_date = dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            # Git管理下にない場合（ローカルでの初回テスト時など）はOSのタイムスタンプを使用
            mtime = os.path.getmtime(filepath)
            update_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        mtime = os.path.getmtime(filepath)
        update_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')

    return {
        'path': str(filepath.as_posix()), # Windows環境でもURL用のスラッシュ区切りを維持
        'title': title,
        'date': update_date,
        'filename': filepath.name
    }

def generate_html(file_list):
    """一覧リストおよび検索機能を備えたHTMLを生成する"""
    # 日付の降順（新しい順）でソート
    sorted_files = sorted(file_list, key=lambda x: x['date'], reverse=True)

    rows_html = ""
    for f in sorted_files:
        # 【変更箇所】ファイル名(filename)もaタグで囲み、リンク化しました。クラス名を付与してスタイルを当てています。
        rows_html += f"""
            <tr class="file-row">
                <td class="file-title"><a href="{f['path']}">{f['title']}</a></td>
                <td class="file-name"><a href="{f['path']}" class="filename-link">{f['filename']}</a></td>
                <td class="file-date">{f['date']}</td>
            </tr>"""

    html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>アップロードファイル一覧</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px auto; max-width: 1000px; color: #333; }}
        h1 {{ border-bottom: 2px solid #0366d6; padding-bottom: 10px; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        th, td {{ border: 1px solid #e1e4e8; padding: 12px 15px; text-align: left; }}
        th {{ background-color: #f6f8fa; font-weight: 600; }}
        tr:hover {{ background-color: #f1f8ff; }}
        a {{ color: #0366d6; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        /* 【変更箇所】ファイル名をコードバッジ風に装飾し、視認性を向上させるCSSを追加 */
        .filename-link {{ color: #476380; font-family: Consolas, monospace; font-size: 0.95em; background-color: #f3f4f6; padding: 4px 8px; border-radius: 4px; display: inline-block; border: 1px solid #e1e4e8; }}
        .filename-link:hover {{ background-color: #e1e4e8; text-decoration: none; }}
        .search-container {{ margin: 20px 0; }}
        input[type="text"] {{ padding: 10px; width: 100%; max-width: 400px; font-size: 16px; border: 1px solid #d1d5da; border-radius: 4px; }}
    </style>
</head>
<body>
    <h1>ドキュメント一覧</h1>

    <div class="search-container">
        <input type="text" id="searchInput" onkeyup="filterFiles()" placeholder="ファイル名で検索...">
    </div>

    <table id="fileTable">
        <thead>
            <tr>
                <th>タイトル</th>
                <th>ファイル名</th>
                <th>更新日時</th>
            </tr>
        </thead>
        <tbody>{rows_html}
        </tbody>
    </table>

    <script>
        function filterFiles() {{
            const input = document.getElementById('searchInput');
            const filter = input.value.toLowerCase();
            const table = document.getElementById('fileTable');
            const tr = table.getElementsByClassName('file-row');

            for (let i = 0; i < tr.length; i++) {{
                const tdName = tr[i].getElementsByClassName('file-name')[0];
                if (tdName) {{
                    // 【変更箇所】aタグが含まれていても、textContentで純粋なファイル名文字列のみを抽出して判定するため、検索は正常に機能します
                    const txtValue = tdName.textContent || tdName.innerText;
                    if (txtValue.toLowerCase().indexOf(filter) > -1) {{
                        tr[i].style.display = "";
                    }} else {{
                        tr[i].style.display = "none";
                    }}
                }}
            }}
        }}
    </script>
</body>
</html>
"""
    return html_template

def main():
    # ターゲットディレクトリが存在しない場合は作成
    if not HTML_DIR.exists():
        HTML_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {HTML_DIR}")

    file_info_list = []
    # 直下のすべてのhtmlファイルと、サブディレクトリ内のindex.htmlを対象とする
    for filepath in HTML_DIR.rglob('*.html'):
        if filepath.parent == HTML_DIR or filepath.name == 'index.html':
            info = get_file_info(filepath)
            file_info_list.append(info)

    html_output = generate_html(file_info_list)

    # index.htmlの書き出し
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"Successfully generated {OUTPUT_FILE} with {len(file_info_list)} files.")

if __name__ == '__main__':
    main()
