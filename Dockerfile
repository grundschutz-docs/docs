# Multi-Stage: Build braucht Node/pnpm, Auslieferung nicht. Die generierten
# .mdx-Seiten liegen bereits im Repo (scripts/generate_docs.py lief vorher,
# siehe README "How the docs are generated") -- dieser Build ruft nur noch
# `astro build`, keinen Python-Schritt, kein Zugriff auf den BSI-Katalog nötig.
FROM node:22-slim AS build
WORKDIR /app

# Nur Manifeste zuerst kopieren -- Docker cached den pnpm-install-Layer,
# solange sich package.json/pnpm-lock.yaml nicht aendern, auch wenn sich
# Quellcode oder Inhalt danach staendig aendert.
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

COPY . .
# .env wird hier zur Build-Zeit gelesen (astro.config.mjs, loadEnvFile()) --
# bei einer rein statischen Seite gibt es zur Laufzeit keinen Prozess mehr,
# der Umgebungsvariablen lesen koennte. Betreiberangaben/SITE_NAME aendern
# heisst: Image neu bauen, nicht Container neu starten.
RUN pnpm run build

# Auslieferung: nur die fertigen Dateien, kein Node, keine node_modules.
# nginx-unprivileged: Master und Worker laufen als Benutzer 101 statt als root und
# lauschen auf 8080 (Ports unter 1024 darf dieser Benutzer nicht binden). Stable-Zweig
# 1.30; 1.27 bekommt keine Sicherheitskorrekturen mehr.
FROM nginxinc/nginx-unprivileged:1.30-alpine AS serve
COPY --from=build /app/dist /usr/share/nginx/html
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY docker/security-headers.conf /etc/nginx/snippets/security-headers.conf
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q --spider http://127.0.0.1:8080/ || exit 1
