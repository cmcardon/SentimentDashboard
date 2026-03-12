FROM node:22-alpine

WORKDIR /workspace/apps/web

COPY apps/web/package.json /workspace/apps/web/package.json
COPY apps/web/tsconfig.json /workspace/apps/web/tsconfig.json
COPY apps/web/next-env.d.ts /workspace/apps/web/next-env.d.ts
COPY apps/web/next.config.ts /workspace/apps/web/next.config.ts
COPY apps/web/app /workspace/apps/web/app
COPY apps/web/components /workspace/apps/web/components
COPY apps/web/lib /workspace/apps/web/lib

RUN npm install

CMD ["npm", "run", "dev"]

