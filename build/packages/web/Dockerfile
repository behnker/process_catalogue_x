# Development Dockerfile for Next.js
FROM node:20-alpine

# Install pnpm
RUN corepack enable && corepack prepare pnpm@9.1.0 --activate

WORKDIR /app

# Copy package files first for better layer caching
COPY package.json pnpm-lock.yaml* ./

# Install dependencies
RUN pnpm install --frozen-lockfile || pnpm install

# Copy source code
COPY . .

# Expose the Next.js development port
EXPOSE 3000

# Start development server
CMD ["pnpm", "dev"]
