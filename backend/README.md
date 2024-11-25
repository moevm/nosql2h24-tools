# Backend

## Run dev using docker

```sh
cd deployment/dev/
```
```sh
docker-compose up -d
```

## Run tests using docker
```sh
cd deployment/test/
```
```sh
docker-compose up -d
```

**Expected output** `======================= 110 passed, 44 warnings in 5.28s =======================`


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
