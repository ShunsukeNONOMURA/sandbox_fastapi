# ----------- Build stage -------------
FROM python:3.13-slim AS builder

# システムロケールとタイムゾーンの設定（必要な場合）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

# Poetryインストール
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false

# 作業ディレクトリ
WORKDIR /root/volume

# ライブラリ定義ファイルのみ先にコピーしてキャッシュ効かせる
COPY volume/pyproject.toml volume/poetry.lock* ./

# ライブラリインストール
RUN poetry install --only main --no-root

# アプリケーションコードコピー
COPY volume/ .

# 暗号化ビルド(ランタイム構成＋難読化)
RUN pyarmor gen runtime && \
    pyarmor gen -O dist app/

# ----------- Release stage -------------
FROM python:3.13-slim

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

WORKDIR /root/volume

# builderから必要なものだけコピー
COPY --from=builder /root/volume/dist /root/volume 
COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10

# 実行コマンド（リロードは不要）
# CMD ["poetry", "run", "uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]
CMD ["python", "-m", "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=80"]

EXPOSE 80