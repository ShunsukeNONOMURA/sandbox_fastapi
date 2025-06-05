実験用Fastapiベースリポジトリ

## 実験項目
- pyarmor難読化
- fastapi-mcp対応
- github actions CI
    - コンテナイメージのghcrへの公開
    - ghpagesへのビルドドキュメント公開
        - `/{ブランチ}/{ビルド項目}` で分離
        - 対象
            - mkdocs
            - schemaspy(sqlite)
            - redoc
            - pytest cov
    - [手動掃除](https://github.com/ShunsukeNONOMURA/sandbox_fastapi/actions/workflows/delete-version.yml)
        - ブランチ名orタグ名指定
        - ブランチorタグ削除
        - ghpagesの対応ファイル削除

## リンク
- 本リポジトリ
    - https://github.com/ShunsukeNONOMURA/sandbox_fastapi
- gh cr の公開コンテナ
    - https://github.com/users/ShunsukeNONOMURA/packages/container/package/my-app
- [gh pages](https://shunsukenonomura.github.io/sandbox_fastapi)
- [pagesのブランチ](https://github.com/ShunsukeNONOMURA/sandbox_fastapi/tree/gh-pages)

## 利用方法メモ
```bash
# dev
docker compose up
# build
docker build -f docker/release/Dockerfile -t myapp:release .
```

```bash
docker pull ghcr.io/shunsukenonomura/my-app:latest
```
