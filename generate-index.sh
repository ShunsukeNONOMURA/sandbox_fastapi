#!/bin/bash

OUTPUT=index.html
VERSIONS_DIR=versions
BASE_URL=$(basename `git config --get remote.origin.url` .git)

echo '<!DOCTYPE html>' > $OUTPUT
echo '<html lang="ja"><head><meta charset="UTF-8"><title>ドキュメントバージョン一覧</title></head><body>' >> $OUTPUT
echo '<h1>ドキュメントバージョン一覧</h1><ul>' >> $OUTPUT

for version_dir in $(find $VERSIONS_DIR -mindepth 1 -maxdepth 10 -type d); do
  version_path=${version_dir#$VERSIONS_DIR/}  # versions/ を除去
  BASE="/$BASE_URL/$VERSIONS_DIR/$version_path"

  echo "<li><strong>$version_path</strong><ul>" >> $OUTPUT

  [[ -d "$version_dir/site" ]] && echo "<li><a href=\"$BASE/site/\">📘 MkDocs</a></li>" >> $OUTPUT
  [[ -d "$version_dir/redoc" ]] && echo "<li><a href=\"$BASE/redoc/\">📕 ReDoc</a></li>" >> $OUTPUT
  [[ -d "$version_dir/htmlcov" ]] && echo "<li><a href=\"$BASE/htmlcov/\">📊 Coverage</a></li>" >> $OUTPUT

  echo "</ul></li>" >> $OUTPUT
done
echo '</ul></body></html>' >> $OUTPUT