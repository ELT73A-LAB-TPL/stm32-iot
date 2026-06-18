
## Updated Dockerfile
- https://thingsboard.io/docs/installation/docker-windows/

###  Initialize database schema and system assets

Before starting ThingsBoard, initialize the database schema and load built-in assets. Choose the option that matches your goal:

- With demo data — also loads a sample tenant account, pre-built dashboards, and demo devices. Useful for exploring the platform before deploying to production.

```bash
docker compose run --rm -e INSTALL_TB=true -e LOAD_DEMO=true thingsboard-ce
```

- Clean install — initializes the database with system data only (rule chains, widget bundles, system dashboards).

```bash
docker compose run --rm -e INSTALL_TB=true thingsboard-ce
```

### Start the platform

Start all containers:

```bash
docker compose up -d
```

Monitor the startup. The line confirming the platform is ready will be highlighted:

```bash
docker compose logs -f thingsboard-ce
```