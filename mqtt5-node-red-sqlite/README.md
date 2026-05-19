
## Updated Dockerfile

To completely reset and rebuild everything from absolute scratch (wipes out old build cache):

```bash
docker compose build --no-cache
```

Rebuild the Node-RED image and recreate the container:

```bash
docker compose up -d --build
```

## Dashboard

For [FlowFuse Dashboard](https://dashboard.flowfuse.com/):
- http://localhost:1881/dashboard
  
For [node-red-dashboard](https://flows.nodered.org/node/node-red-dashboard):
- http://localhost:1881/ui
