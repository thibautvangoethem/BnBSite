FROM node:18-slim

WORKDIR /app

COPY ./frontend/package*.json ./

RUN npm install

COPY . .

ARG VITE_BACKEND_URL
ENV VITE_BACKEND_URL=$VITE_BACKEND_URL

RUN npm run build

EXPOSE 5173


CMD ["npm", "run", "start"]