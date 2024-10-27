ARG NODE_VERSION=20

FROM node:${NODE_VERSION}-slim AS build
LABEL maintainer="Rahul Agarwal <agarwal.rahul324@gmail.com>"

ARG BUN_VERSION=1.0.15

WORKDIR /build


# Install Bun in the specified version
RUN apt update && apt install -y bash curl unzip && \
    rm -rf /var/lib/apt/lists/* && \
    curl https://bun.sh/install | bash -s -- bun-v${BUN_VERSION}

ENV PATH="${PATH}:/root/.bun/bin"

#
# Copy the lock file and app manifest, then install
# the dependencies, including the dev dependencies
#
COPY bun.lockb package.json ./

RUN bun install

# Copy the application sources into the build stage
COPY . .

# ADJUST: Build your application
RUN bun run build

#
# After building the application, we will remove the node_modules
# directory and install only the production dependencies.
#
# Note that clearing the Bun package cache is necessary because I encountered
# extremely slow install times during building the image. This issue seems to be
# related to: https://github.com/oven-sh/bun/issues/4066
#
RUN rm -rf node_modules && \
  rm -rf /root/.bun/install/cache/ && \
  bun install --frozen-lockfile --production

#
# Optional step: Here we will prune all unnecessary files from our
# node_modules directory, such as markdown and TypeScript source files,
# to further reduce the container image size.
#
RUN curl -sf https://gobinaries.com/tj/node-prune | sh && \
    node-prune

FROM node:${NODE_VERSION}-alpine AS distribution

ENV NODE_ENV="production"

WORKDIR /app

COPY --from=build --chown=node:node /build/package.json ./package.json
COPY --from=build --chown=node:node /build/node_modules ./node_modules
COPY --from=build --chown=node:node /build/.next ./.next
COPY --from=build --chown=node:node /build/public ./public

# Set up non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 && \
    chown -R nextjs:nodejs /app
    
USER nextjs
EXPOSE 3000
ENV HOSTNAME=0.0.0.0

CMD ["npm", "start"]