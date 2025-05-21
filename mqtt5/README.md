## Steps to Test mqtt5

Follow these steps to test the `mqtt5` service (Mosquitto MQTT broker) using interactive Docker containers (`docker -it`). These steps assume the `STM32-MQTT-DB` Docker Compose stack is running and `mosquitto.conf` allows anonymous connections for testing.

### 1. Verify the mqtt5 Container is Running
Ensure the `mqtt5` container is active and listening on ports `1883` and `9001`.

- Check running containers:
```bash
docker ps
```
Look for the mqtt5 container with the image eclipse-mosquitto:latest.
If not running, start the stack:
```bash
docker-compose up -d
 ```
### 2. Run an Interactive Mosquitto Client Container
Use the eclipse-mosquitto:latest image to run mosquitto_sub and mosquitto_pub commands in separate containers connected to the iot-network.
Subscribe to a Topic (mosquitto_sub)

Start a container to subscribe to a test topic:
```bash
docker run -it --rm --network stm32-mqtt-db_iot-network eclipse-mosquitto:latest mosquitto_sub -h mqtt5 -p 1883 -t test/topic
```
        --rm: Removes the container after it exits.
        --network stm32-mqtt-db_iot-network: Connects to the Docker Compose network, allowing resolution of the mqtt5 hostname.
        -h mqtt5: Targets the mqtt5 service.
        -p 1883: Uses the MQTT port.
        -t test/topic: Subscribes to the test/topic topic.
The terminal will wait for incoming messages. Keep it running.

Publish a Message (mosquitto_pub)

    In a new terminal, run a container to publish a message:
```bash
docker run -it --rm --network stm32-mqtt-db_iot-network eclipse-mosquitto:latest mosquitto_pub -h mqtt5 -p 1883 -t test/topic -m "Hello, MQTT!"
```
 -m "Hello, MQTT!": Publishes the message "Hello, MQTT!" to test/topic.
The container exits after publishing (due to --rm).
Check the subscriber terminal (from the previous step). You should see:

 Hello, MQTT!


### 3. Test MQTT5-Specific Features (Optional)
The mqtt5 service supports MQTT 5.0. Test features like user properties if enabled in mosquitto.conf (e.g., protocol mqtt).

    Publish with User Property:
```bash
docker run -it --rm --network stm32-mqtt-db_iot-network eclipse-mosquitto:latest mosquitto_pub -h mqtt5 -p 1883 -t test/topic -m "MQTT5 Test" -V mqttv5 -P "key1=value1"
```
 -V mqttv5: Forces MQTT 5.0 protocol.
 -P "key1=value1": Adds a user property.
 Subscribe with Debug Output:
```bash
docker run -it --rm --network stm32-mqtt-db_iot-network eclipse-mosquitto:latest mosquitto_sub -h mqtt5 -p 1883 -t test/topic -V mqttv5 --debug
```
--debug: Displays MQTT5 properties (e.g., user properties).

### 4. Test WebSocket (Optional)
The mqtt5 service exposes port 9001 for WebSocket. Test using a WebSocket-compatible MQTT client (e.g., MQTT.js or HiveMQ WebSocket Client).

Example with MQTT.js (requires Node.js):
```javascript
    const mqtt = require('mqtt');
    const client = mqtt.connect('ws://localhost:9001', { protocolVersion: 5 });
    client.on('connect', () => {
      client.subscribe('test/topic');
      client.publish('test/topic', 'Hello via WebSocket!');
    });
    client.on('message', (topic, message) => {
      console.log(`Received: ${message} on ${topic}`);
    });
```
Connect to ws://localhost:9001 and test with topic test/topic.

### How to Use
- **Copy the Markdown**: Paste this into a `.md` file (e.g., `test_mqtt5_steps.md`) using a Markdown-compatible editor (e.g., VS Code, Obsidian).
- **Execute Commands**: Run the commands in the listed order to test the `mqtt5` service.
- **Verify**: Confirm messages are sent and received as expected.

If you need additional details (e.g., troubleshooting, configuring `mosquitto.conf`, or STM32 integration), let me know!
