#!/bin/bash
OUTPUT=${1:-index.html}  # ← 引数がなければ index.html に出力
VERSIONS_DIR=versions
BASE_URL=$(basename `git config --get remote.origin.url` .git)

echo '<!DOCTYPE html>' > $OUTPUT
echo '<html lang="ja"><head><meta charset="UTF-8"><title>ドキュメントバージョン一覧</title></head><body>' >> $OUTPUT
echo '<h1>ドキュメントバージョン一覧</h1><ul>' >> $OUTPUT

find "$VERSIONS_DIR" -mindepth 1 -maxdepth 2 -type d | sort -V | while read version_dir; do
  # フィルタ条件：最低1つのバージョン用サブディレクトリが存在する
  has_content=false
  [[ -d "$version_dir/site" ]] && has_content=true
  [[ -d "$version_dir/schemaspy" ]] && has_content=true
  [[ -d "$version_dir/redoc" ]] && has_content=true
  [[ -d "$version_dir/htmlcov" ]] && has_content=true
  [[ -d "$version_dir/manual-html" ]] && has_content=true
  [[ -f "$version_dir/manual-pdf/manual.pdf" ]] && has_content=true

  $has_content || continue

  version_path=${version_dir#$VERSIONS_DIR/}
  BASE="/$BASE_URL/$VERSIONS_DIR/$version_path"

  echo "<li><strong>$version_path</strong><ul>" >> $OUTPUT
  [[ -d "$version_dir/site" ]] && echo "<li><a href=\"$BASE/site/\">📘 MkDocs</a></li>" >> $OUTPUT
  [[ -f "$version_dir/schemaspy/index.html" ]] && echo "<li><a href=\"$BASE/schemaspy/index.html\">🗂 SchemaSpy</a></li>" >> $OUTPUT
  [[ -f "$version_dir/redoc/api.html" ]] && echo "<li><a href=\"$BASE/redoc/api.html\">📕 ReDoc</a></li>" >> $OUTPUT
  [[ -d "$version_dir/htmlcov" ]] && echo "<li><a href=\"$BASE/htmlcov/\">📊 Coverage</a></li>" >> $OUTPUT
  [[ -f "$version_dir/manual-html/manual.html" ]] && echo "<li><a href=\"$BASE/manual-html/manual.html\">📗 Manual (HTML)</a></li>" >> $OUTPUT
  [[ -f "$version_dir/manual-pdf/manual.pdf" ]] && echo "<li><a href=\"$BASE/manual-pdf/manual.pdf\">📄 Manual (PDF)</a></li>" >> $OUTPUT
  echo "</ul></li>" >> $OUTPUT
done

echo '</ul></body></html>' >> $OUTPUT