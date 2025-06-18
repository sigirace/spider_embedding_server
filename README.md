```
docker buildx build --platform linux/amd64,linux/arm64 \
  -t sigirace/studio:latest \
  . \
  --push
```

대용량 파일

```
curl -X 'POST' \
  'http://localhost:8001/document/[app_id]' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer [token]' \
  -F 'file_list=@[file_path]'
```