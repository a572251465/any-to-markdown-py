![logo](logo.png)

# any-to-markdown-py
Convert any document into a markdown document based on a large model

## Future tasks
- [x] base service setup (25/06/22)
- [x] py web (25/06/22)
- [ ] Multiple Agent tasks to be executed
- [ ] pdf -> image
- [ ] image -> markdown
- [ ] pdf + image -> markdown
- [ ] text -> markdown
- [ ] word -> markdown
- [ ] xlsx -> markdown
- [ ] offline deploy model
- [ ] docker deploy project

## start command

### dev start command
```bash
uv run uvicorn main:app --host $web_server_host --port $web_server_port --reload
```

### prod start command
```bash
uv run uvicorn main:app --host $WEB_SERVER_HOST --port $WEB_SERVER_PORT
```