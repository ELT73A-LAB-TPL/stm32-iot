

# Docker Compose Configuration for STM32-IoT

This Docker Compose configuration defines an IoT stack named "STM32-IoT" with three services: `mqtt5` (Mosquitto MQTT broker), `node-red` (Node-RED), and `influxdb2` (InfluxDB). The services are connected via a bridge network, with persistent volumes for data storage.

## Services

### 1. mqtt5 (MQTT Broker)
- **Image**: `eclipse-mosquitto:latest` (latest Mosquitto MQTT broker).
- **Container Name**: `mqtt5`
- **Ports**:
  - `1883:1883` (standard MQTT port).
  - `9001:9001` (WebSocket port for MQTT over WebSocket).
- **Volumes**:
  - `mqtt-config`, `mqtt-data`, `mqtt-log`: Persistent storage for configuration, data, and logs.
  - `./mosquitto.conf:/mosquitto/config/mosquitto.conf`: Custom Mosquitto configuration file.
- **Network**: `iot-network` (bridge network).
- **Restart Policy**: `unless-stopped` (restarts unless explicitly stopped).
- **Notes**:
  - A comment references `host.docker.internal`, suggesting configuration for host machine access. Update `mosquitto.conf` to include `listener 1883 0.0.0.0` and consider authentication for production.

### 2. node-red (Node-RED)
- **Image**: Custom-built using a `Dockerfile` in the current directory (not the official `nodered/node-red:latest`).
- **Container Name**: `node-red`
- **Environment**:
  - `TZ=America/Sao_Paulo`: Sets timezone to São Paulo, Brazil.
- **Ports**:
  - `1881:1880`: Maps host port 1881 to container port 1880 (likely to avoid conflict with STM32CubeMonitor).
- **Volumes**:
  - `node-red-data`: Persistent storage for Node-RED flows and settings.
- **Depends On**: `mqtt5` (ensures MQTT broker starts first).
- **Network**: `iot-network`.
- **Restart Policy**: `unless-stopped`.

### 3. influxdb2 (InfluxDB)
- **Image**: `influxdb:alpine` (lightweight InfluxDB based on Alpine Linux).
- **Container Name**: `influxdb2`
- **Ports**:
  - `8086:8086` (InfluxDB UI and API).
- **Environment**:
  - `DOCKER_INFLUXDB_INIT_MODE=setup`: Initializes InfluxDB automatically.
  - `DOCKER_INFLUXDB_INIT_USERNAME=${INFLUXDB_USERNAME:-myusername}`: Default username (overridable via environment).
  - `DOCKER_INFLUXDB_INIT_PASSWORD=${INFLUXDB_PASSWORD:-mypassword}`: Default password.
  - `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=${INFLUXDB_TOKEN:-mytoken}`: Default admin token.
  - `DOCKER_INFLUXDB_INIT_ORG=IoT`: Organization name.
  - `DOCKER_INFLUXDB_INIT_BUCKET=Node-RED`: Default bucket.
  - `DOCKER_INFLUXDB_INIT_RETENTION=1w`: Data retention for 1 week.
- **Volumes**:
  - `influxdb2-data`: Persistent database storage.
  - `influxdb2-config`: Configuration files.
- **Network**: `iot-network`.
- **Restart Policy**: `unless-stopped`.

## Volumes
- **Named Volumes**:
  - `mqtt-config`, `mqtt-data`, `mqtt-log`: For Mosquitto persistence.
  - `node-red-data`: For Node-RED persistence.
  - `influxdb2-data`, `influxdb2-config`: For InfluxDB persistence.
- Ensures data persists across container restarts.

## Network
- **iot-network**: Bridge network enabling communication between services using container names (e.g., `mqtt5`, `influxdb2`).

## Potential Issues and Recommendations

1. **host.docker.internal**:
   - Configure `mosquitto.conf` for host access:
     ```conf
     listener 1883 0.0.0.0
     allow_anonymous true  # For testing; use authentication in production
     ```
   - On Linux, add `--add-host=host.docker.internal:host-gateway` to `docker-compose up`.

2. **Custom Node-RED Image**:
   - Ensure the `Dockerfile` includes required nodes (e.g., `node-red-contrib-mqtt`, `node-red-contrib-influxdb`).
   - Example `Dockerfile`:
     ```dockerfile
     FROM nodered/node-red:latest
     RUN npm install node-red-contrib-influxdb node-red-contrib-mqtt
     ```

3. **InfluxDB Security**:
   - Use a `.env` file for sensitive credentials:
     ```env
     INFLUXDB_USERNAME=secureuser
     INFLUXDB_PASSWORD=securepassword
     INFLUXDB_TOKEN=securetoken
     ```
   - Avoid hardcoding defaults like `myusername` or `mypassword`.

4. **Port Conflict**:
   - Node-RED uses `1881` on the host to avoid conflicts with port `1880`. Verify no other service uses `1881`.

5. **Mosquitto Configuration**:
   - Ensure `mosquitto.conf` supports MQTT5 if needed and includes security settings (e.g., TLS, authentication).

6. **InfluxDB Version**:
   - Verify `influxdb:alpine` is the desired version (e.g., InfluxDB 2.x). Use a specific tag like `influxdb:2.7-alpine` if needed.

7. **Security Recommendations**:
   - Enable authentication and TLS for Mosquitto.
   - Secure Node-RED UI with a password in `settings.js`.
   - Use HTTPS for InfluxDB.

8. **Docker Compose Version**:
   - Add `version: '3.8'` at the top of the file for clarity.

## How to Run

1. **Create `mosquitto.conf`**:
   - Place in the same directory as `docker-compose.yml`:
     ```conf
     persistence true
     persistence_location /mosquitto/data/
     log_dest file /mosquitto/log/mosquitto.log
     listener 1883
     allow_anonymous true  # For testing
     ```

2. **Optional: Create `.env` File**:
   ```env
   INFLUXDB_USERNAME=youruser
   INFLUXDB_PASSWORD=yourpass
   INFLUXDB_TOKEN=yourtoken
