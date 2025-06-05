#!/bin/bash

OUTPUT=index.html
VERSIONS_DIR=versions
BASE_URL=$(basename `git config --get remote.origin.url` .git)

echo '<!DOCTYPE html>' > $OUTPUT
echo '<html lang="ja"><head><meta charset="UTF-8"><title>ドキュメントバージョン一覧</title></head><body>' >> $OUTPUT
echo '<h1>ドキュメントバージョン一覧</h1><ul>' >> $OUTPUT

for version in $(ls -1 $VERSIONS_DIR); do
  BASE="/$BASE_URL/versions/$version"

  echo "<li><strong>$version</strong><ul>" >> $OUTPUT

  [[ -d "$VERSIONS_DIR/$version/site" ]] && echo "<li><a href=\"$BASE/site/\">📘 MkDocs</a></li>" >> $OUTPUT
  [[ -d "$VERSIONS_DIR/$version/redoc" ]] && echo "<li><a href=\"$BASE/redoc/\">📕 ReDoc</a></li>" >> $OUTPUT
  [[ -d "$VERSIONS_DIR/$version/htmlcov" ]] && echo "<li><a href=\"$BASE/htmlcov/\">📊 Coverage</a></li>" >> $OUTPUT

  echo "</ul></li>" >> $OUTPUT
done

echo '</ul></body></html>' >> $OUTPUT