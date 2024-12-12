
db = db.getSiblingDB(process.env.MONGO_DB);

db.createUser({
    user: process.env.MONGO_USER,
    pwd: process.env.MONGO_PASSWORD,
    roles: [
        {
            role: "readWrite",
            db: process.env.MONGO_DB
        }
    ]
});

db.createCollection(process.env.CLIENT_COLLECTION);
db.createCollection(process.env.WORKER_COLLECTION);
db.createCollection(process.env.TOOL_COLLECTION);
db.createCollection(process.env.CATEGORY_COLLECTION);
db.createCollection(process.env.TYPE_COLLECTION);
db.createCollection(process.env.ORDER_COLLECTION);

db.getCollection(process.env.WORKER_COLLECTION).insertOne({
    email: "worker@example.com",
    password: "$2b$12$6osWoQyXJQCuUKdn76sUweeHcZ0FiIux9M3htL0LghHQbGr3TQZe.", // worker_123
    name: "Иван",
    surname: "Иванов",
    phone: "+71234567890",
    jobTitle: "Главный работник",
    date: new Date(),
    orders: [],
    image: null,
    created_at: new Date(),
    updated_at: new Date()
});


db.getCollection(process.env.CLIENT_COLLECTION).insertOne({
    email: "client@example.com",
    password: "$2b$12$1oR3y9CFG9M3rhuClfX8eudl3.8Kh94pLMXeybrzjqeEqe3f27kSS", // client_123
    name: "Алексей",
    surname: "Алексеев",
    orders: [],
    phone: "+70987654321",
    image: null,
    created_at: new Date(),
    updated_at: new Date()
});