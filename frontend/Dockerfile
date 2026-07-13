FROM node:20-slim AS base
WORKDIR /app/frontend
COPY frontend/package.json ./
RUN npm install
COPY frontend ./
ENV NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
