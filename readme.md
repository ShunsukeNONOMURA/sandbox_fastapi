実験用Fastapiリポジトリ

## 実験項目

- pyarmorによる難読化
- github actionsによるCI
    - コンテナイメージのghcrへの公開
    - ghpagesへのビルドドキュメント公開


## リンク
https://github.com/ShunsukeNONOMURA/sandbox_fastapi
https://github.com/users/ShunsukeNONOMURA/packages/container/package/my-app
https://shunsukenonomura.github.io/sandbox_fastapi/api.html


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
