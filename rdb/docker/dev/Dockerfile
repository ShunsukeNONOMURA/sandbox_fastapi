FROM postgres:17.5

# 必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    ca-certificates \
    postgresql-server-dev-17 \
    cmake \
    clang \
    pkg-config \
    libssl-dev \
    flex \
    bison && \
    rm -rf /var/lib/apt/lists/*

# pgvector インストール
RUN git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && \
    make install && \
    cd .. && rm -rf pgvector

# AGE インストール
RUN git clone --branch PG17 https://github.com/apache/age.git && \
    cd age && \
    make PG_CONFIG=/usr/lib/postgresql/17/bin/pg_config && \
    make install PG_CONFIG=/usr/lib/postgresql/17/bin/pg_config && \
    cd .. && rm -rf age

# psql -U postgres
# CREATE EXTENSION vector;
# CREATE EXTENSION age; 
# LOAD 'age';
# SET search_path TO ag_catalog, "$user", public;
# SELECT * FROM create_graph('test_graph');