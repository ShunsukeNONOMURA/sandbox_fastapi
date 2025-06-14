import json
import yaml
from pathlib import Path

from app.main import app

# export openapi
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>My Project - ReDoc</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    <style>
        body {
            margin: 0;
            padding: 0;
        }
    </style>
    <style data-styled="" data-styled-version="4.4.1"></style>
</head>
<body>
    <div id="redoc-container"></div>
    <script src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"> </script>
    <script>
        var spec = %s;
        Redoc.init(spec, {}, document.getElementById("redoc-container"));
    </script>
</body>
</html>
"""

# パス定義
path_root = Path("./docs")
path_output_dir = path_root / "backend"
path_output_html = path_output_dir / "api.html"
path_output_openapi_json = path_output_dir / "openapi.json"
path_output_openapi_yaml = path_output_dir / "openapi.yaml"

# ディレクトリを作成（存在しない場合）
path_output_dir.mkdir(parents=True, exist_ok=True)

with Path(path_output_html).open("w") as fd:
    print(HTML_TEMPLATE % json.dumps(app.openapi()), file=fd)
with Path(path_output_openapi_json).open("w") as f:
    api_spec = app.openapi()
    f.write(json.dumps(api_spec, indent=2))
with Path(path_output_openapi_yaml).open("w", encoding="utf-8") as f:
    api_spec = app.openapi()
    yaml.dump(api_spec, f, allow_unicode=True, sort_keys=False)