The provided `docker-compose.yml` file defines a Docker Compose setup for an MQTT broker, specifically using the Eclipse Mosquitto image. Let's break down its components:

**Overall Project Name:**

* `name: STM32-MQTT` - This sets the name of your Docker Compose project. When you run `docker compose up`, the containers, networks, and volumes will be prefixed with `stm32-mqtt_` by default.

**Services:**

* `mqtt5:` - This defines a service named `mqtt5`.

    * `image: eclipse-mosquitto:latest` - Specifies that this service will use the latest available image of Eclipse Mosquitto from Docker Hub.
    * `container_name: mqtt5` - Assigns a fixed name `mqtt5` to the container created by this service. This makes it easier to reference the container (e.g., in Docker commands).
    * `ports:`
        * `- "1883:1883"` - Maps port 1883 on the host machine to port 1883 inside the container. This is the standard unencrypted MQTT port.
        * `- "9001:9001"` - Maps port 9001 on the host machine to port 9001 inside the container. This is commonly used for MQTT over WebSockets.
    * `volumes:`
        * `- mqtt-config:/mosquitto/config:rw` - Mounts a named Docker volume `mqtt-config` to `/mosquitto/config` inside the container. This directory typically stores Mosquitto's configuration files. `rw` means read-write access.
        * `- mqtt-data:/mosquitto/data:rw` - Mounts a named Docker volume `mqtt-data` to `/mosquitto/data`. This is where Mosquitto stores its persistence data (e.g., retained messages, client sessions).
        * `- mqtt-log:/mosquitto/log:rw` - Mounts a named Docker volume `mqtt-log` to `/mosquitto/log`. This is where Mosquitto writes its log files.
        * `- ./mosquitto.conf:/mosquitto/config/mosquitto.conf` - This is a crucial line. It mounts a *local file* named `mosquitto.conf` (which should be in the same directory as your `docker-compose.yml` file) directly into the container as `/mosquitto/config/mosquitto.conf`. This allows you to provide a custom configuration for your Mosquitto broker, overriding any default settings or settings from the `mqtt-config` volume.
    * `networks:`
        * `- iot-network` - Connects the `mqtt5` service to the `iot-network` that is defined later in the file. This allows other services within the `iot-network` to communicate with the Mosquitto broker by its service name (`mqtt5`).
    * `restart: unless-stopped` - Configures the container to restart automatically unless it is explicitly stopped. This ensures the MQTT broker remains available even if the Docker daemon restarts.
    * `# config for host.docker.internal` - This is a comment indicating a potential configuration or consideration related to `host.docker.internal`, which is a special DNS name that resolves to the host machine's IP address from within a Docker container. This is often used when a container needs to connect to a service running directly on the host.

**Volumes:**

* `mqtt-config:` - Declares a named Docker volume called `mqtt-config`. Docker manages the creation and lifecycle of this volume.
* `mqtt-data:` - Declares a named Docker volume called `mqtt-data`.
* `mqtt-log:` - Declares a named Docker volume called `mqtt-log`.

    *By using named volumes, your Mosquitto configuration, data, and logs will persist even if you remove and recreate the `mqtt5` container. This is highly recommended for stateful applications like MQTT brokers.*

**Networks:**

* `iot-network:` - Declares a custom Docker network named `iot-network`.
    * `driver: bridge` - Specifies that this network will use the default `bridge` driver. This creates a private internal network that containers can connect to.

**In summary, this `docker-compose.yml` file provides a robust setup for an MQTT broker:**

* **Easy Deployment:** Simplifies the deployment of a Mosquitto MQTT broker with a single command (`docker compose up`).
* **Portability:** The setup is self-contained and can be easily moved and deployed on different Docker-enabled environments.
* **Persistence:** Utilizes named volumes to ensure that your Mosquitto configuration, message data, and logs are preserved across container restarts or removals.
* **Custom Configuration:** Allows you to provide a custom `mosquitto.conf` file to tailor the broker's behavior.
* **Network Isolation:** Creates a dedicated `iot-network` for your IoT-related services, improving network organization and security.
* **Automatic Restart:** Ensures high availability of the MQTT broker.

To use this file, you would typically:

1.  Save it as `docker-compose.yml` in a directory.
2.  Create a `mosquitto.conf` file in the *same directory* with your desired Mosquitto configurations.
3.  Navigate to that directory in your terminal.
4.  Run `docker compose up -d` to start the services in detached mode.


## To test your **STM32-MQTT** Docker Compose setup, you'll need an **MQTT client** to publish messages to and subscribe from your Mosquitto broker.

First, ensure your Docker Compose services are running:

```bash
docker compose up -d
```

You can verify that the `mqtt5` container is running by:

```bash
docker ps
```

You should see `mqtt5` listed with a `Status` of `Up`.

---

### 1. Using Mosquitto Command-Line Clients (`mosquitto_pub` and `mosquitto_sub`)

These tools are usually part of the Mosquitto package on your host machine. If you don't have them, you might need to install `mosquitto-clients` (e.g., `sudo apt-get install mosquitto-clients` on Debian/Ubuntu, or Homebrew on macOS).

Alternatively, you can run them from *within* your Mosquitto Docker container, which ensures you have the correct versions and avoids local installation:

**a) Subscribe to a topic:**

Open a new terminal and run:

```bash
docker exec -it mqtt5 mosquitto_sub -h localhost -p 1883 -t "test/topic" -q 1
```

This terminal will now wait for messages on `"test/topic"`.

**b) Publish a message:**

Open *another* new terminal and run:

```bash
docker exec -it mqtt5 mosquitto_pub -h localhost -p 1883 -t "test/topic" -m "Hello from Docker!" -q 1
```

After running the `mosquitto_pub` command, you should see "Hello from Docker!" appear in the terminal where you ran `mosquitto_sub`. This confirms your broker is receiving and forwarding messages.

---

### 2. Using a Desktop MQTT Client (Recommended for GUI)

Graphical MQTT clients offer a much more user-friendly interface for testing. Popular options include:

* **MQTT Explorer:** Highly recommended for its intuitive UI, topic visualization, and ease of use.
* **MQTTX:** Another excellent cross-platform client with good features.

**Steps for a Desktop Client (general):**

1.  **Download and Install:** Get your preferred MQTT client from its official website.
2.  **Create a New Connection:**
    * **Host:** `localhost` (or `127.0.0.1`) – This refers to your host machine, which Docker is mapping ports to.
    * **Port:** `1883` (for standard MQTT)
    * **Port:** `9001` (for MQTT over WebSockets, if your client supports it and you want to test that)
    * **Client ID:** (Optional) A unique identifier for your client.
    * **Username/Password:** (Optional, if you configured authentication in `mosquitto.conf`)
3.  **Connect:** Establish the connection.
4.  **Subscribe:** Add a new subscription, e.g., to topic `test/topic` or `sensor/#` (using wildcards).
5.  **Publish:** Send a message to a topic, e.g., `test/topic` with a payload like "Hello from MQTT Explorer!".

You should see your published message appear in the subscription panel of the same client (if subscribed to that topic) or in a different client connected to the same broker.

---

### 3. Using a Web-Based MQTT Client (MQTT over WebSockets)

Since your `docker-compose.yml` exposes port `9001` for WebSockets, you can use a web-based client:

* **MQTTX Web:** A popular browser-based MQTT client.

**Steps for a Web-Based Client:**

1.  **Open the Web Client:** Go to a website like `https://mqttx.app/web` or search for "online MQTT client."
2.  **Configure Connection:**
    * **Protocol:** Select `WebSocket` (or `ws://`).
    * **Host:** `localhost` (or `127.0.0.1`)
    * **Port:** `9001`
    * **Path:** Often `/mqtt` is required by some brokers, but for Mosquitto's default WebSocket listener, it's usually not necessary unless explicitly configured in `mosquitto.conf`. Try without a path first.
3.  **Connect:** Click the connect button.
4.  **Subscribe and Publish:** Similar to desktop clients, subscribe to a topic and publish messages.

---

### 4. Simple Python Script (Paho MQTT Client)

This is great for programmatic testing and automation.

First, install the Paho MQTT client library:

```bash
pip install paho-mqtt
```

**a) Subscriber Script (`subscriber.py`):**

```python
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("test/python")

def on_message(client, userdata, msg):
    print(f"Received message on topic '{msg.topic}': {msg.payload.decode()}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# Connect to the Mosquitto broker running on your host machine
# which is mapped to port 1883 of the container
client.connect("localhost", 1883, 60)

# Loop forever to process network traffic, dispatch callbacks, and handle reconnects
client.loop_forever()
```

**b) Publisher Script (`publisher.py`):**

```python
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

# Connect to the Mosquitto broker running on your host machine
# which is mapped to port 1883 of the container
client.connect("localhost", 1883, 60)
client.loop_start() # Start a non-blocking loop in a separate thread

try:
    for i in range(5):
        message = f"Python message {i}"
        client.publish("test/python", message)
        print(f"Published: '{message}' to 'test/python'")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting publisher.")
finally:
    client.loop_stop()
    client.disconnect()
```

**To run these scripts:**

1.  Open one terminal and run: `python subscriber.py`
2.  Open another terminal and run: `python publisher.py`

You should see the messages from the publisher script appearing in the subscriber script's terminal.

---

### Troubleshooting Tips:

* **Firewall:** Ensure your firewall isn't blocking ports `1883` or `9001` on your host machine.
* **`mosquitto.conf`:** Double-check your `mosquitto.conf` file. If you've added `allow_anonymous false`, you'll need to provide a username and password (and possibly set up an `aclfile` for topic permissions). For initial testing, `allow_anonymous true` is often used.
* **Docker Logs:** Check the logs of your Mosquitto container for any errors:
    ```bash
    docker logs mqtt5
    ```
* **Network Issues:** If you're having trouble connecting, ensure your client is trying to connect to `localhost` and the correct port, as these are the ports exposed by Docker on your host machine.

By using a combination of these testing methods, you can effectively verify that your Mosquitto MQTT broker is running correctly and that clients can publish and subscribe to messages.
