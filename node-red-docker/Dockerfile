# ------------------------------------------------------
# Custom minimal Node-RED image (Alpine)
# ------------------------------------------------------

FROM node:24-alpine

LABEL org.opencontainers.image.title="Custom Node-RED Minimal" \
      org.opencontainers.image.description="Minimal Node-RED image with dashboard and sqlite support" \
      org.opencontainers.image.source="https://github.com/node-red/node-red"

ENV NODE_ENV=production \
    NODE_RED_HOME=/usr/src/node-red \
    TZ=America/Sao_Paulo

# Install minimal runtime dependencies
RUN apk add --no-cache \
        tini \
        tzdata \
        git \
    && addgroup -S node-red \
    && adduser -S -G node-red -h /data node-red

# Set working directory
WORKDIR ${NODE_RED_HOME}

# Install Node-RED and nodes
RUN npm install --omit=dev --no-update-notifier --no-fund \
        node-red \
        node-red-node-sqlite \
        @flowfuse/node-red-dashboard \
        @flowfuse/node-red-dashboard-2-ui-led \
        node-red-dashboard \
        node-red-node-ui-table \
        node-red-contrib-ui-led \
        node-red-contrib-bcrypt \
        node-red-contrib-finite-statemachine \
    && npm cache clean --force

# Create persistent directories
RUN mkdir -p \
        /data \
        /data/sqlite \
    && chown -R node-red:node-red \
        /data \
        ${NODE_RED_HOME}

# Optional custom settings and flows
COPY --chown=node-red:node-red settings.js /data/settings.js
COPY --chown=node-red:node-red flows.json /data/flows.json

# Run as non-root
USER node-red

# Node-RED port
EXPOSE 1880

# Persistent storage
VOLUME ["/data"]

# Proper signal handling
ENTRYPOINT ["/sbin/tini", "--"]

# Start Node-RED
CMD ["node", "/usr/src/node-red/node_modules/node-red/red.js", "--userDir", "/data"]
