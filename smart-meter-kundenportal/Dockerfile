FROM node:latest AS base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
COPY . /app
WORKDIR /app

RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install
RUN pnpm prisma generate
RUN pnpm sync

ENV PORT=3001
ENV ORIGIN="http://localhost:3001"
RUN pnpm run build
CMD node -r dotenv/config build