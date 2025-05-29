https://github.com/ShunsukeNONOMURA/test_image_build
https://github.com/users/ShunsukeNONOMURA/packages/container/package/my-app
https://shunsukenonomura.github.io/test_image_build/api.html

```bash
# dev
docker compose up
# build
docker build -f docker/release/Dockerfile -t myapp:release .
```

```bash
docker pull ghcr.io/shunsukenonomura/my-app:latest
```
