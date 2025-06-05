FROM python:3.10

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

# schemaspy用の追加設定
RUN apt-get update && apt-get install -y default-jre graphviz

# SchemaSpyとJDBCドライバの配置（任意に切替）
RUN mkdir -p /opt/schemaspy && \
    curl -L -o /opt/schemaspy/schemaspy.jar https://github.com/schemaspy/schemaspy/releases/latest/download/schemaspy-6.2.4.jar && \
    curl -L -o /opt/schemaspy/postgresql-jdbc.jar https://jdbc.postgresql.org/download/postgresql-42.7.3.jar && \
    curl -L -o /opt/schemaspy/sqlite-jdbc.jar https://repo1.maven.org/maven2/org/xerial/sqlite-jdbc/3.45.1.0/sqlite-jdbc-3.45.1.0.jar

ENV PATH="/opt/schemaspy:$PATH"