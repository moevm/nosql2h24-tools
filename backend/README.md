# Backend

## Run via docker

```sh
cd deployment/dev/
```

```sh
docker-compose up -d
```
## OpenAPI docs
```sh
http://127.0.0.1:8000/docs
```

## Default credentials

### Worker
- **email**: `worker@example.com`
- **password**:  `worker_123`

### Client
- **email**: `client@example.com`
- **password**:  `client_123`

## Connect to the MongoDB instance using MongoDB Compass
```sh
mongodb://testUser:123456@localhost:27017/tools_database?authSource=tools_database
```
