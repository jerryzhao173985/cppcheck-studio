# CPPCheck Studio Deployment Guide

## 🚀 Quick Deploy

### Vercel (Recommended for Web App)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/cppcheck-studio)

### npm Package

```bash
# Publish to npm
npm login
npm publish --workspace=cppcheck-studio
```

## 📦 Building for Production

```bash
# Install dependencies
npm install

# Build all packages
npm run build

# Run tests
npm test

# Create production bundle
./scripts/build.sh --prod
```

## 🐳 Docker Deployment

### Build Docker Image

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder

# Install cppcheck
RUN apk add --no-cache cppcheck g++ make python3

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY turbo.json ./
COPY packages ./packages
COPY apps ./apps

# Install dependencies
RUN npm ci

# Build
RUN npm run build

# Production image
FROM node:18-alpine

RUN apk add --no-cache cppcheck

WORKDIR /app

# Copy built files
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

EXPOSE 3000 3001

CMD ["npm", "start"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - API_URL=http://api:3001
    depends_on:
      - api
      
  api:
    build: .
    command: ["npm", "run", "start:api"]
    ports:
      - "3001:3001"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/cppcheck
    depends_on:
      - db
      - redis
      
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=cppcheck
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## ☁️ Cloud Deployment

### AWS

1. **EC2 Deployment**
```bash
# Install on Ubuntu
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs cppcheck

# Clone and build
git clone https://github.com/yourusername/cppcheck-studio
cd cppcheck-studio
npm install
npm run build

# Use PM2 for process management
npm install -g pm2
pm2 start ecosystem.config.js
```

2. **ECS with Fargate**
```json
{
  "family": "cppcheck-studio",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "web",
      "image": "your-registry/cppcheck-studio:latest",
      "portMappings": [
        {
          "containerPort": 3000,
          "protocol": "tcp"
        }
      ]
    }
  ]
}
```

### Google Cloud Platform

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/cppcheck-studio

# Deploy to Cloud Run
gcloud run deploy cppcheck-studio \
  --image gcr.io/PROJECT_ID/cppcheck-studio \
  --platform managed \
  --port 3000 \
  --allow-unauthenticated
```

### Azure

```bash
# Create web app
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name cppcheck-studio \
  --deployment-container-image-name your-registry/cppcheck-studio

# Configure
az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name cppcheck-studio \
  --settings NODE_ENV=production
```

## 🔧 Configuration

### Environment Variables

```bash
# Web App
NEXT_PUBLIC_API_URL=https://api.cppcheck.studio
NEXT_PUBLIC_ANALYTICS_ID=UA-XXXXXXXX

# API Server
NODE_ENV=production
PORT=3001
DATABASE_URL=postgresql://user:pass@localhost:5432/cppcheck
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
CORS_ORIGIN=https://cppcheck.studio

# CLI
CPPCHECK_BINARY=/usr/bin/cppcheck
CPPCHECK_STUDIO_API=https://api.cppcheck.studio
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name cppcheck.studio;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name cppcheck.studio;
    
    ssl_certificate /etc/ssl/certs/cppcheck.studio.crt;
    ssl_certificate_key /etc/ssl/private/cppcheck.studio.key;
    
    # Web app
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
    
    # API
    location /api {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
    }
    
    # WebSocket support
    location /socket.io {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 📊 Monitoring

### Health Checks

```bash
# Web app
curl https://cppcheck.studio/api/health

# API
curl https://api.cppcheck.studio/health
```

### PM2 Ecosystem

```javascript
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name: 'cppcheck-web',
      script: 'npm',
      args: 'run start:web',
      env: {
        NODE_ENV: 'production',
        PORT: 3000
      }
    },
    {
      name: 'cppcheck-api',
      script: 'npm',
      args: 'run start:api',
      env: {
        NODE_ENV: 'production',
        PORT: 3001
      }
    }
  ]
}
```

### Logging

```javascript
// winston configuration
{
  transports: [
    new winston.transports.File({
      filename: '/var/log/cppcheck-studio/error.log',
      level: 'error'
    }),
    new winston.transports.File({
      filename: '/var/log/cppcheck-studio/combined.log'
    })
  ]
}
```

## 🔒 Security

### SSL/TLS

```bash
# Let's Encrypt
certbot certonly --standalone -d cppcheck.studio -d www.cppcheck.studio
```

### Security Headers

```javascript
// helmet configuration
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'", "'unsafe-eval'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
}))
```

### Rate Limiting

```javascript
const rateLimit = require('express-rate-limit')

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
})

app.use('/api/', limiter)
```

## 📈 Scaling

### Horizontal Scaling

```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cppcheck-studio
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cppcheck-studio
  template:
    metadata:
      labels:
        app: cppcheck-studio
    spec:
      containers:
      - name: web
        image: your-registry/cppcheck-studio:latest
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

### CDN Integration

```javascript
// Next.js configuration for CDN
module.exports = {
  assetPrefix: 'https://cdn.cppcheck.studio',
  images: {
    domains: ['cdn.cppcheck.studio'],
  },
}
```

## 🚀 CI/CD Pipeline

### GitHub Actions

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        
    - name: Install dependencies
      run: npm ci
      
    - name: Run tests
      run: npm test
      
    - name: Build
      run: npm run build
      
    - name: Deploy to Vercel
      run: vercel --prod
      env:
        VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
```

## 📝 Post-Deployment

1. **Verify deployment**
   ```bash
   curl https://cppcheck.studio/api/health
   ```

2. **Run smoke tests**
   ```bash
   npm run test:e2e
   ```

3. **Monitor logs**
   ```bash
   pm2 logs
   ```

4. **Set up alerts**
   - Configure monitoring (DataDog, New Relic, etc.)
   - Set up error tracking (Sentry)
   - Configure uptime monitoring

## 🆘 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   lsof -i :3000
   kill -9 <PID>
   ```

2. **cppcheck not found**
   ```bash
   which cppcheck
   export CPPCHECK_BINARY=/path/to/cppcheck
   ```

3. **Database connection failed**
   ```bash
   # Check PostgreSQL status
   systemctl status postgresql
   
   # Test connection
   psql -U user -d cppcheck -h localhost
   ```

4. **Redis connection failed**
   ```bash
   redis-cli ping
   ```

## 📚 Additional Resources

- [Production Checklist](https://nextjs.org/docs/going-to-production)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)