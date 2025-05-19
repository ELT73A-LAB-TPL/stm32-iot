# Use the official Node-RED base image
FROM nodered/node-red:latest

# Set working directory
WORKDIR /usr/src/node-red
	
# Install additional Node-RED nodes
RUN npm install --unsafe-perm --no-update-notifier --no-fund \
    node-red-contrib-influxdb \
	node-red-dashboard \
	node-red-contrib-bcrypt \
	node-red-contrib-finite-statemachine \
	node-red-contrib-ui-led \
	node-red-node-serialport \
	node-red-node-ui-table
	
# Alternative STM32-related nodes (optional, uncomment if needed)
#RUN npm install --unsafe-perm --no-update-notifier --no-fund \
#    @stm32/node-red-contrib-stm32cubemonitor

# Copy custom settings file (optional)
#COPY settings.js /data/settings.js

# Copy custom flows (optional)
#COPY flows.json /data/flows.json

# Expose Node-RED port
EXPOSE 1880

# Use the default entrypoint and command from the base image
# CMD ["npm", "start", "--", "--userDir", "/data"]