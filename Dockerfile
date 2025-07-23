# Multi-stage Dockerfile for CPPCheck Studio

# Stage 1: Base dependencies
FROM ubuntu:22.04 AS base
RUN apt-get update && apt-get install -y \
    curl \
    git \
    jq \
    python3 \
    python3-pip \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: CPPCheck builder
FROM base AS cppcheck-builder
ARG CPPCHECK_VERSION=2.13
RUN apt-get update && apt-get install -y wget && \
    wget https://github.com/danmar/cppcheck/archive/${CPPCHECK_VERSION}.tar.gz && \
    tar xzf ${CPPCHECK_VERSION}.tar.gz && \
    cd cppcheck-${CPPCHECK_VERSION} && \
    cmake . && \
    cmake --build . -j$(nproc) && \
    make install && \
    cd .. && rm -rf cppcheck-${CPPCHECK_VERSION} ${CPPCHECK_VERSION}.tar.gz

# Stage 3: Node.js builder
FROM node:18-slim AS node-builder
WORKDIR /app
COPY cppcheck-dashboard-generator/package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force

# Stage 4: Python dependencies
FROM base AS python-builder
WORKDIR /app
COPY requirements.txt* ./
RUN pip3 install --no-cache-dir -r requirements.txt || true

# Stage 5: Final production image
FROM ubuntu:22.04
LABEL maintainer="CPPCheck Studio Team"
LABEL description="CPPCheck Studio Analysis Environment"

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nodejs \
    npm \
    git \
    jq \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy built artifacts
COPY --from=cppcheck-builder /usr/local/bin/cppcheck /usr/local/bin/
COPY --from=cppcheck-builder /usr/local/share/cppcheck /usr/local/share/cppcheck
COPY --from=node-builder /app/node_modules /app/node_modules

# Copy application code
WORKDIR /app
COPY . .

# Install dashboard generator globally
RUN cd cppcheck-dashboard-generator && \
    npm ci && \
    npm run build && \
    npm link

# Create non-root user
RUN useradd -m -s /bin/bash cppcheck && \
    chown -R cppcheck:cppcheck /app
USER cppcheck

# Set environment variables
ENV NODE_ENV=production
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD cppcheck --version || exit 1

# Default command
CMD ["/bin/bash"]