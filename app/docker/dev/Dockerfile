FROM python:3.13

RUN apt-get update &&\
    apt-get -y install locales &&\
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 &&\
    apt-get -y upgrade
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN pip install --upgrade pip

# Poetryのインストール
RUN curl -sSL https://install.python-poetry.org | python -

# Poetryのパスの設定
ENV PATH /root/.local/bin:$PATH

# Poetryが仮想環境を生成しないようにする
RUN poetry config virtualenvs.create false

# pyproject.tomlからライブラリを初回導入
COPY volume/pyproject.toml .
RUN poetry install --no-root
