
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
db.createCollection(process.env.REVIEW_COLLECTION);

db.getCollection(process.env.WORKER_COLLECTION).insertOne(
    {
        "_id": ObjectId("67488ea1e0b092cfb2fe6911"),

        "email": "worker@example.com",
        "password": "$2b$12$6osWoQyXJQCuUKdn76sUweeHcZ0FiIux9M3htL0LghHQbGr3TQZe.",
        "name": "Иван",
        "surname": "Иванов",
        "phone": "+71234567890",
        "jobTitle": "Главный работник",
        "date": ISODate("2024-11-28T15:39:13.05Z"),
        "image": "http://localhost:8000/api/resources/images/workers/c0999ff2f2c730678f0356603e424516b674ccb0d599b87dedb7a9a1bc89646f/1.png",
        "created_at": ISODate("2024-11-28T15:39:13.05Z"),
        "updated_at": ISODate("2024-11-28T15:39:13.05Z")
    }
);

db.getCollection(process.env.CLIENT_COLLECTION).insertMany([
	{
		"_id": ObjectId("6762d6a2f6292fe72b752b5e"),

		"email": "client_1@example.com",
		"password": "$2b$12$.RzxPWac/e4RISJEnw69YuqMw8PLmBACZdGWZPeLAIw6M.IiWT4rq",
		"created_at": ISODate("2024-12-18T14:05:22.519Z"),
		"updated_at": ISODate("2024-12-18T14:10:29.924Z"),
		"name": "Иван",
		"surname": "Петров",
		"phone": "+79161234567",
		"image": "http://localhost:8000/api/resources/images/clients/d89b750bd5a875c166119bf523fa5dabd5b3e2d263ea63b68aa26cd0411af1f3/1.png"
	},
	{
		"_id": ObjectId("6762d6d9f6292fe72b752b5f"),

		"email": "client_2@example.com",
		"password": "$2b$12$pWggz5PL/5gtaRrS56nNPupZfyKB/DCcNznf/.au4KCoEhZLpGLnm",
		"created_at": ISODate("2024-12-18T14:06:17.859Z"),
		"updated_at": ISODate("2024-12-18T14:10:53.606Z"),
		"name": "Ольга",
		"surname": "Смирнова",
		"phone": "+79991234567",
		"image": "http://localhost:8000/api/resources/images/clients/4d1732f83c592083c1d3c77ec3b45ec1c950f7c974c938fc1affaed81cf6f084/1.png"
	},
	{
		"_id": ObjectId("6762d6ebf6292fe72b752b60"),

		"email": "client_3@example.com",
		"password": "$2b$12$Ujrol9/uLzk8tV6rn5S.w.mAJJFhjO1OtO.IwpT5WRk1g/XZt41s.",
		"created_at": ISODate("2024-12-18T14:06:35.724Z"),
		"updated_at": ISODate("2024-12-18T14:11:20.467Z"),
		"name": "Алексей",
		"surname": "Васильев",
		"phone": "+79271234567",
		"image": "http://localhost:8000/api/resources/images/clients/263dc3e1633465f5cc6cfc17daec3627764a43cdbba3ebcbe9eca18aa2acb105/1.png"
	}
]);

db.getCollection(process.env.CATEGORY_COLLECTION).insertMany([
	{
		"_id": ObjectId("6762d9126b4835df660bce63"),

		"name": "Ручной инструмент",
		"types": [
			ObjectId("6762d9526b4835df660bce67"),

			ObjectId("6762d9656b4835df660bce68"),

			ObjectId("6762d96c6b4835df660bce69")

		]
	},
	{
		"_id": ObjectId("6762d91b6b4835df660bce64"),

		"name": "Электроинструмент",
		"types": [
			ObjectId("6762d9776b4835df660bce6a"),

			ObjectId("6762d97d6b4835df660bce6b"),

			ObjectId("6762d9816b4835df660bce6c")

		]
	},
	{
		"_id": ObjectId("6762d9226b4835df660bce65"),

		"name": "Измерительные инструменты",
		"types": [
			ObjectId("6762d98e6b4835df660bce6d"),

			ObjectId("6762d9946b4835df660bce6e")

		]
	},
	{
		"_id": ObjectId("6762d92d6b4835df660bce66"),

		"name": "Защитное оборудование",
		"types": [
			ObjectId("6762d9bd6b4835df660bce70"),

			ObjectId("6762d9c76b4835df660bce71"),

			ObjectId("6762d9d16b4835df660bce72")

		]
	}
]);


db.getCollection(process.env.TYPE_COLLECTION).insertMany([
	{
		"_id": ObjectId("6762d9526b4835df660bce67"),

		"name": "Молоток",
		"category_name": "Ручной инструмент",
		"tools": [

			ObjectId("6762db8ad5595612f0a21207"),

			ObjectId("6762dbe7d5595612f0a21208"),

			ObjectId("6762dbefd5595612f0a21209")

		]
	},
	{
		"_id": ObjectId("6762d9656b4835df660bce68"),

		"name": "Отвертка",
		"category_name": "Ручной инструмент",
		"tools": [
			ObjectId("6762dc08d5595612f0a2120a"),

			ObjectId("6762dc15d5595612f0a2120b"),

			ObjectId("6762dc27d5595612f0a2120c")

		]
	},
	{
		"_id": ObjectId("6762d96c6b4835df660bce69"),

		"name": "Рожковый ключ",
		"category_name": "Ручной инструмент",
		"tools": [
			ObjectId("6762dc34d5595612f0a2120d"),

			ObjectId("6762dc3ad5595612f0a2120e"),

			ObjectId("6762dc40d5595612f0a2120f")

		]
	},
	{
		"_id": ObjectId("6762d9776b4835df660bce6a"),

		"name": "Дрель",
		"category_name": "Электроинструмент",
		"tools": [
			ObjectId("6762dc49d5595612f0a21210"),

			ObjectId("6762dc4ed5595612f0a21211"),

			ObjectId("6762dc54d5595612f0a21212")

		]
	},
	{
		"_id": ObjectId("6762d97d6b4835df660bce6b"),

		"name": "Болгарка",
		"category_name": "Электроинструмент",
		"tools": [
			ObjectId("6762dc67d5595612f0a21213"),

			ObjectId("6762dc6fd5595612f0a21214"),

			ObjectId("6762dc83d5595612f0a21215")

		]
	},
	{
		"_id": ObjectId("6762d9816b4835df660bce6c"),

		"name": "Перфоратор",
		"category_name": "Электроинструмент",
		"tools": [
			ObjectId("6762dc98d5595612f0a21216"),

			ObjectId("6762dca1d5595612f0a21217"),

			ObjectId("6762dca5d5595612f0a21218")

		]
	},
	{
		"_id": ObjectId("6762d98e6b4835df660bce6d"),

		"name": "Рулетка",
		"category_name": "Измерительные инструменты",
		"tools": [
			ObjectId("6762dcabd5595612f0a21219"),

			ObjectId("6762dcb5d5595612f0a2121a"),

			ObjectId("6762dcd8d5595612f0a2121b")

		]
	},
	{
		"_id": ObjectId("6762d9946b4835df660bce6e"),

		"name": "Уровень",
		"category_name": "Измерительные инструменты",
		"tools": [
			ObjectId("6762dcfcd5595612f0a2121c"),

			ObjectId("6762dd02d5595612f0a2121d"),

			ObjectId("6762dd0cd5595612f0a2121e")

		]
	},
	{
		"_id": ObjectId("6762d9bd6b4835df660bce70"),

		"name": "Очки защитные",
		"category_name": "Защитное оборудование",
		"tools": [
			ObjectId("6762dd44d5595612f0a2121f"),

			ObjectId("6762dd4cd5595612f0a21220"),

			ObjectId("6762dd52d5595612f0a21221")

		]
	},
	{
		"_id": ObjectId("6762d9c76b4835df660bce71"),

		"name": "Каска",
		"category_name": "Защитное оборудование",
		"tools": [
			ObjectId("6762dd5bd5595612f0a21222"),

			ObjectId("6762dd63d5595612f0a21223"),

			ObjectId("6762dd68d5595612f0a21224")

		]
	},
	{
		"_id": ObjectId("6762d9d16b4835df660bce72"),

		"name": "Перчатки рабочие",
		"category_name": "Защитное оборудование",
		"tools": [
			ObjectId("6762dd6ed5595612f0a21225"),

			ObjectId("6762dd89d5595612f0a21226"),

            ObjectId("6762dd89d5595612f0a21227")
		]
	}
]);

db.getCollection(process.env.TOOL_COLLECTION).insertMany([
	{
		"_id": ObjectId("6762db8ad5595612f0a21207"),

		"name": "Молоток-гвоздодер Kraftool",
		"dailyPrice": 40.0,
		"totalPrice": 850.0,
		"images": [
			"http://localhost:8000/api/resources/images/tools/5d25e3d8154a07b5edc4ed1c9c09930494980b1942f1d979b867c4391baf1e2f/1.png",
			"http://localhost:8000/api/resources/images/tools/5d25e3d8154a07b5edc4ed1c9c09930494980b1942f1d979b867c4391baf1e2f/2.png"
		],
		"features": {
			"Вес": "500 г",
			"Материал": "Закаленная сталь",
			"Ручка": "Эргономичная резиновая",
			"Назначение": "Работа с гвоздями"
		},
		"rating": 3.0,
		"category": "Ручной инструмент",
		"type": "Молоток",
		"description": "Многофункциональный молоток с гвоздодером. Подходит для легких строительных работ и ремонта.",
		"created_at": ISODate("2024-12-18T14:26:18.458Z"),
		"updated_at": ISODate("2024-12-18T14:26:18.458Z"),
		"reviews_count": 2
	},
	{
		"_id": ObjectId("6762dbe7d5595612f0a21208"),

		"name": "Молоток слесарный Matrix",
		"dailyPrice": 50.0,
		"totalPrice": 700.0,
		"images": [],
		"features": {
			"Вес": "1000 г",
			"Материал": "Сталь с антикоррозийным покрытием",
			"Ручка": "Двухкомпонентная ручка",
			"Назначение": "Слесарные работы"
		},
		"rating": 4.5,
		"category": "Ручной инструмент",
		"type": "Молоток",
		"description": "Тяжелый молоток для выполнения слесарных работ. Удобная двухкомпонентная ручка снижает вибрацию при работе.",
		"created_at": ISODate("2024-12-18T14:27:51.127Z"),
		"updated_at": ISODate("2024-12-18T14:27:51.127Z"),
		"reviews_count": 2
	},
	{
		"_id": ObjectId("6762dbefd5595612f0a21209"),

		"name": "Молоток столярный Stanley",
		"dailyPrice": 30.0,
		"totalPrice": 500.0,
		"images": [],
		"features": {
			"Вес": "300 г",
			"Материал": "Углеродистая сталь",
			"Ручка": "Деревянная",
			"Назначение": "Столярные работы"
		},
		"rating": 4.0,
		"category": "Ручной инструмент",
		"type": "Молоток",
		"description": "Легкий молоток, идеально подходящий для столярных и плотницких работ. Деревянная ручка обеспечивает комфортный захват.",
		"created_at": ISODate("2024-12-18T14:27:59.391Z"),
		"updated_at": ISODate("2024-12-18T14:27:59.391Z"),
		"reviews_count": 1
	},
	{
		"_id": ObjectId("6762dc08d5595612f0a2120a"),

		"name": "Отвертка крестовая PH2 Vira",
		"dailyPrice": 20.0,
		"totalPrice": 150.0,
		"images": [],
		"features": {
			"Размер": "PH2",
			"Материал": "Хром-ванадиевая сталь",
			"Ручка": "Эргономичная резиновая",
			"Назначение": "Работа с шурупами"
		},
		"rating": 0.0,
		"category": "Ручной инструмент",
		"type": "Отвертка",
		"description": "Качественная крестовая отвертка для сборки мебели и ремонта. Удобная ручка обеспечивает надежный хват.",
		"created_at": ISODate("2024-12-18T14:28:24.878Z"),
		"updated_at": ISODate("2024-12-18T14:28:24.878Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dc15d5595612f0a2120b"),

		"name": "Отвертка плоская Stayer",
		"dailyPrice": 15.0,
		"totalPrice": 120.0,
		"images": [],
		"features": {
			"Размер": "4 мм",
			"Материал": "Закаленная сталь",
			"Ручка": "Пластиковая",
			"Назначение": "Работа с плоскими крепежами"
		},
		"rating": 4.0,
		"category": "Ручной инструмент",
		"type": "Отвертка",
		"description": "Прочная плоская отвертка для мелких бытовых и профессиональных работ. Подходит для любых стандартных крепежей.",
		"created_at": ISODate("2024-12-18T14:28:37.612Z"),
		"updated_at": ISODate("2024-12-18T14:28:37.612Z"),
		"reviews_count": 1
	},
	{
		"_id": ObjectId("6762dc27d5595612f0a2120c"),

		"name": "Отвертка с набором бит Kraftool",
		"dailyPrice": 50.0,
		"totalPrice": 950.0,
		"images": [],
		"features": {
			"Биты": "12 штук",
			"Материал": "Хром-ванадиевая сталь",
			"Ручка": "Противоскользящая",
			"Назначение": "Многофункциональная работа"
		},
		"rating": 5.0,
		"category": "Ручной инструмент",
		"type": "Отвертка",
		"description": "Отвертка с комплектом сменных бит, идеальна для универсального использования. Надежный инструмент для дома и работы.",
		"created_at": ISODate("2024-12-18T14:28:55.614Z"),
		"updated_at": ISODate("2024-12-18T14:28:55.614Z"),
		"reviews_count": 1
	},
	{
		"_id": ObjectId("6762dc34d5595612f0a2120d"),

		"name": "Ключ рожковый 10x12 мм Sparta",
		"dailyPrice": 25.0,
		"totalPrice": 200.0,
		"images": [],
		"features": {
			"Размер": "10x12 мм",
			"Материал": "Хром-ванадиевая сталь",
			"Покрытие": "Антикоррозийное",
			"Назначение": "Работа с болтами и гайками"
		},
		"rating": 5.0,
		"category": "Ручной инструмент",
		"type": "Рожковый ключ",
		"description": "Универсальный рожковый ключ для работы с крепежами среднего размера. Прочный и удобный в использовании.",
		"created_at": ISODate("2024-12-18T14:29:08.978Z"),
		"updated_at": ISODate("2024-12-18T14:29:08.978Z"),
		"reviews_count": 1
	},
	{
		"_id": ObjectId("6762dc3ad5595612f0a2120e"),

		"name": "Ключ комбинированный 13 мм Stanley",
		"dailyPrice": 30.0,
		"totalPrice": 350.0,
		"images": [],
		"features": {
			"Размер": "13 мм",
			"Материал": "Хром-ванадиевая сталь",
			"Форма": "Рожковая и кольцевая",
			"Назначение": "Профессиональный инструмент"
		},
		"rating": 0.0,
		"category": "Ручной инструмент",
		"type": "Рожковый ключ",
		"description": "Комбинированный ключ с двумя рабочими поверхностями. Подходит для профессионального использования.",
		"created_at": ISODate("2024-12-18T14:29:14.567Z"),
		"updated_at": ISODate("2024-12-18T14:29:14.567Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dc40d5595612f0a2120f"),

		"name": "Ключ рожковый 17x19 мм Kraftool",
		"dailyPrice": 35.0,
		"totalPrice": 450.0,
		"images": [],
		"features": {
			"Размер": "17x19 мм",
			"Материал": "Инструментальная сталь",
			"Покрытие": "Матовое",
			"Назначение": "Работа с крупными крепежами"
		},
		"rating": 0.0,
		"category": "Ручной инструмент",
		"type": "Рожковый ключ",
		"description": "Прочный и надежный рожковый ключ для работы с крупногабаритными крепежами. Подходит для автосервиса и строительства.",
		"created_at": ISODate("2024-12-18T14:29:20.463Z"),
		"updated_at": ISODate("2024-12-18T14:29:20.463Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dc49d5595612f0a21210"),

		"name": "Дрель ударная Bosch GSB 13 RE",
		"dailyPrice": 300.0,
		"totalPrice": 6500.0,
		"images": [],
		"features": {
			"Мощность": "600 Вт",
			"Частота вращения": "2800 об/мин",
			"Режим": "Ударный",
			"Назначение": "Сверление и бурение"
		},
		"rating": 0.0,
		"category": "Электроинструмент",
		"type": "Дрель",
		"description": "Компактная ударная дрель от Bosch для работы с бетоном, деревом и металлом. Эргономичная ручка для комфортной работы.",
		"created_at": ISODate("2024-12-18T14:29:29.832Z"),
		"updated_at": ISODate("2024-12-18T14:29:29.832Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dc4ed5595612f0a21211"),

		"name": "Дрель DeWalt DWD024",
		"dailyPrice": 350.0,
		"totalPrice": 7500.0,
		"images": [],
		"features": {
			"Мощность": "700 Вт",
			"Частота вращения": "2800 об/мин",
			"Вес": "1.8 кг",
			"Назначение": "Профессиональная работа"
		},
		"rating": 0.0,
		"category": "Электроинструмент",
		"type": "Дрель",
		"description": "Мощная дрель от DeWalt с высокой производительностью. Подходит для интенсивного использования на стройке.",
		"created_at": ISODate("2024-12-18T14:29:34.365Z"),
		"updated_at": ISODate("2024-12-18T14:29:34.365Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dc54d5595612f0a21212"),

		"name": "Дрель-шуруповерт Makita DF330DWE",
		"dailyPrice": 400.0,
		"totalPrice": 9500.0,
		"images": [
			"http://localhost:8000/api/resources/images/tools/d56b0d31b3a81077bb50df1f37a30f94fe23ebdbef02d6c6e5d4ef3385279c5c/1.png",
			"http://localhost:8000/api/resources/images/tools/d56b0d31b3a81077bb50df1f37a30f94fe23ebdbef02d6c6e5d4ef3385279c5c/2.png"
		],
		"features": {
			"Аккумулятор": "10.8 В",
			"Частота вращения": "1300 об/мин",
			"Тип": "Аккумуляторный",
			"Назначение": "Сборка мебели"
		},
		"rating": 0.0,
		"category": "Электроинструмент",
		"type": "Дрель",
		"description": "Аккумуляторная дрель-шуруповерт от Makita. Идеальный инструмент для сборки мебели и мелких работ.",
		"created_at": ISODate("2024-12-18T14:29:40.82Z"),
		"updated_at": ISODate("2024-12-18T14:29:40.82Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dc67d5595612f0a21213"),

		"name": "Угловая шлифмашина Bosch GWS 7-125",
		"dailyPrice": 400.0,
		"totalPrice": 6000.0,
		"images": [],
		"features": {
			"Мощность": "720 Вт",
			"Диаметр диска": "125 мм",
			"Частота вращения": "11000 об/мин",
			"Назначение": "Шлифовка и резка"
		},
		"rating": 5.0,
		"category": "Электроинструмент",
		"type": "Болгарка",
		"description": "Компактная болгарка для точной резки и шлифовки металла и камня. Эргономичный дизайн обеспечивает комфортную работу.",
		"created_at": ISODate("2024-12-18T14:29:59.731Z"),
		"updated_at": ISODate("2024-12-18T14:29:59.731Z"),
		"reviews_count": 1
	},
	{
		"_id": ObjectId("6762dc6fd5595612f0a21214"),

		"name": "Болгарка Makita GA5030",
		"dailyPrice": 350.0,
		"totalPrice": 5500.0,
		"images": [],
		"features": {
			"Мощность": "720 Вт",
			"Диаметр диска": "125 мм",
			"Частота вращения": "11000 об/мин",
			"Вес": "1.8 кг"
		},
		"rating": 0.0,
		"category": "Электроинструмент",
		"type": "Болгарка",
		"description": "Удобная и мощная углошлифовальная машина, предназначенная для различных строительных и ремонтных работ.",
		"created_at": ISODate("2024-12-18T14:30:07.428Z"),
		"updated_at": ISODate("2024-12-18T14:30:07.428Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dc83d5595612f0a21215"),

		"name": "Угловая шлифмашина DeWalt DWE4051",
		"dailyPrice": 500.0,
		"totalPrice": 7200.0,
		"images": [],
		"features": {
			"Мощность": "800 Вт",
			"Диаметр диска": "115 мм",
			"Частота вращения": "11000 об/мин",
			"Защита": "Электронная защита двигателя"
		},
		"rating": 0.0,
		"category": "Электроинструмент",
		"type": "Болгарка",
		"description": "Мощная болгарка с компактными размерами, идеальная для профессиональных работ с металлом и бетоном.",
		"created_at": ISODate("2024-12-18T14:30:27.499Z"),
		"updated_at": ISODate("2024-12-18T14:30:27.499Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dc98d5595612f0a21216"),

		"name": "Перфоратор Bosch GBH 2-26 DRE",
		"dailyPrice": 500.0,
		"totalPrice": 11000.0,
		"images": [],
		"features": {
			"Мощность": "800 Вт",
			"Режимы работы": "3 (сверление, долбление, комбинированный)",
			"Сила удара": "2.7 Дж",
			"Назначение": "Работа с бетоном и кирпичом"
		},
		"rating": 0.0,
		"category": "Электроинструмент",
		"type": "Перфоратор",
		"description": "Перфоратор для тяжелых строительных работ. Обеспечивает мощное долбление и высокую производительность.",
		"created_at": ISODate("2024-12-18T14:30:48.504Z"),
		"updated_at": ISODate("2024-12-18T14:30:48.504Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dca1d5595612f0a21217"),

		"name": "Перфоратор Makita HR2470",
		"dailyPrice": 450.0,
		"totalPrice": 9500.0,
		"images": [],
		"features": {
			"Мощность": "780 Вт",
			"Режимы работы": "3 (сверление, долбление, комбинированный)",
			"Сила удара": "2.4 Дж",
			"Назначение": "Универсальные строительные работы"
		},
		"rating": 4.0,
		"category": "Электроинструмент",
		"type": "Перфоратор",
		"description": "Универсальный перфоратор от Makita для работы с бетоном, кирпичом и металлом. Надежный инструмент для строительных задач.",
		"created_at": ISODate("2024-12-18T14:30:57.622Z"),
		"updated_at": ISODate("2024-12-18T14:30:57.622Z"),
		"reviews_count": 1
	},
	{
		"_id": ObjectId("6762dca5d5595612f0a21218"),

		"name": "Перфоратор DeWalt D25133K",
		"dailyPrice": 550.0,
		"totalPrice": 12500.0,
		"images": [],
		"features": {
			"Мощность": "800 Вт",
			"Сила удара": "2.9 Дж",
			"Режимы работы": "3 (сверление, долбление, комбинированный)",
			"Вес": "2.6 кг"
		},
		"rating": 0.0,
		"category": "Электроинструмент",
		"type": "Перфоратор",
		"description": "Мощный перфоратор DeWalt для интенсивного использования. Обеспечивает высокую производительность и комфорт в работе.",
		"created_at": ISODate("2024-12-18T14:31:01.918Z"),
		"updated_at": ISODate("2024-12-18T14:31:01.918Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dcabd5595612f0a21219"),

		"name": "Рулетка измерительная Stanley 5 м",
		"dailyPrice": 20.0,
		"totalPrice": 400.0,
		"images": [],
		"features": {
			"Длина": "5 м",
			"Ширина ленты": "19 мм",
			"Материал корпуса": "Пластик с резиновым покрытием",
			"Назначение": "Измерение длины"
		},
		"rating": 0.0,
		"category": "Измерительные инструменты",
		"type": "Рулетка",
		"description": "Классическая рулетка с прочной лентой для строительных и бытовых нужд. Обеспечивает точные измерения.",
		"created_at": ISODate("2024-12-18T14:31:07.66Z"),
		"updated_at": ISODate("2024-12-18T14:31:07.66Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dcb5d5595612f0a2121a"),

		"name": "Рулетка лазерная Bosch GLM 50",
		"dailyPrice": 200.0,
		"totalPrice": 8000.0,
		"images": [
			"http://localhost:8000/api/resources/images/tools/5ce2f7f4ec7ee5709c101dc011b25001041196e54cab1a44c3911bec2fcc5444/1.png",
			"http://localhost:8000/api/resources/images/tools/5ce2f7f4ec7ee5709c101dc011b25001041196e54cab1a44c3911bec2fcc5444/2.png"
		],
		"features": {
			"Дальность": "50 м",
			"Точность": "± 1.5 мм",
			"Дисплей": "Цветной с подсветкой",
			"Назначение": "Измерение больших расстояний"
		},
		"rating": 0.0,
		"category": "Измерительные инструменты",
		"type": "Рулетка",
		"description": "Лазерная рулетка для измерения больших расстояний с высокой точностью. Подходит для профессионалов и любителей.",
		"created_at": ISODate("2024-12-18T14:31:17.525Z"),
		"updated_at": ISODate("2024-12-18T14:31:17.525Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dcd8d5595612f0a2121b"),

		"name": "Рулетка измерительная Kraftool",
		"dailyPrice": 30.0,
		"totalPrice": 600.0,
		"images": [],
		"features": {
			"Длина": "7.5 м",
			"Ширина ленты": "25 мм",
			"Материал корпуса": "Прорезиненный пластик",
			"Механизм": "Автоматический стопор"
		},
		"rating": 0.0,
		"category": "Измерительные инструменты",
		"type": "Рулетка",
		"description": "Рулетка с увеличенной длиной для профессионального использования. Эргономичный корпус для удобства.",
		"created_at": ISODate("2024-12-18T14:31:52.889Z"),
		"updated_at": ISODate("2024-12-18T14:31:52.889Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dcfcd5595612f0a2121c"),

		"name": "Уровень строительный Stabila 60 см",
		"dailyPrice": 50.0,
		"totalPrice": 1200.0,
		"images": [],
		"features": {
			"Длина": "60 см",
			"Материал": "Алюминий",
			"Точность измерения": "0.5 мм/м",
			"Назначение": "Проверка горизонтальности и вертикальности"
		},
		"rating": 0.0,
		"category": "Измерительные инструменты",
		"type": "Уровень",
		"description": "Компактный строительный уровень для точных измерений. Подходит для использования дома и на стройке.",
		"created_at": ISODate("2024-12-18T14:32:28.599Z"),
		"updated_at": ISODate("2024-12-18T14:32:28.599Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dd02d5595612f0a2121d"),

		"name": "Уровень магнитный Kraftool 80 см",
		"dailyPrice": 70.0,
		"totalPrice": 1500.0,
		"images": [],
		"features": {
			"Длина": "80 см",
			"Магнит": "Да",
			"Материал": "Усиленный алюминий",
			"Точность": "0.5 мм/м"
		},
		"rating": 0.0,
		"category": "Измерительные инструменты",
		"type": "Уровень",
		"description": "Магнитный уровень с прочным корпусом, идеально подходит для работы с металлическими конструкциями.",
		"created_at": ISODate("2024-12-18T14:32:34.536Z"),
		"updated_at": ISODate("2024-12-18T14:32:34.536Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dd0cd5595612f0a2121e"),

		"name": "Лазерный уровень Bosch GLL 2-15",
		"dailyPrice": 300.0,
		"totalPrice": 9500.0,
		"images": [],
		"features": {
			"Дальность": "15 м",
			"Точность": "± 0.3 мм/м",
			"Тип линии": "Горизонтальная и вертикальная",
			"Назначение": "Высокоточные строительные работы"
		},
		"rating": 0.0,
		"category": "Измерительные инструменты",
		"type": "Уровень",
		"description": "Лазерный уровень для точного выравнивания линий на строительных площадках. Компактный и удобный в использовании.",
		"created_at": ISODate("2024-12-18T14:32:44.504Z"),
		"updated_at": ISODate("2024-12-18T14:32:44.504Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dd44d5595612f0a2121f"),

		"name": "Очки защитные Зубр Эксперт",
		"dailyPrice": 20.0,
		"totalPrice": 300.0,
		"images": [],
		"features": {
			"Материал линз": "Поликарбонат",
			"Антизапотевающее покрытие": "Да",
			"Защита": "От механических повреждений",
			"Назначение": "Работа с инструментами"
		},
		"rating": 0.0,
		"category": "Защитное оборудование",
		"type": "Очки защитные",
		"description": "Прочные защитные очки для работы с электроинструментами. Защищают глаза от пыли и осколков.",
		"created_at": ISODate("2024-12-18T14:33:40.545Z"),
		"updated_at": ISODate("2024-12-18T14:33:40.545Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dd4cd5595612f0a21220"),

		"name": "Очки открытого типа Uvex",
		"dailyPrice": 30.0,
		"totalPrice": 500.0,
		"images": [],
		"features": {
			"Материал линз": "Пластик",
			"УФ-защита": "Да",
			"Регулировка": "По ширине",
			"Назначение": "Работа на улице и в помещении"
		},
		"rating": 0.0,
		"category": "Защитное оборудование",
		"type": "Очки защитные",
		"description": "Легкие очки с УФ-защитой для использования в разных условиях. Регулируемые дужки обеспечивают комфортную посадку.",
		"created_at": ISODate("2024-12-18T14:33:48.3Z"),
		"updated_at": ISODate("2024-12-18T14:33:48.3Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dd52d5595612f0a21221"),

		"name": "Очки закрытого типа Makita",
		"dailyPrice": 40.0,
		"totalPrice": 700.0,
		"images": [],
		"features": {
			"Материал линз": "Поликарбонат",
			"Вентиляция": "Пассивная",
			"Назначение": "Работа с пылью и химикатами",
			"Защита": "Полная"
		},
		"rating": 0.0,
		"category": "Защитное оборудование",
		"type": "Очки защитные",
		"description": "Закрытые очки с вентиляцией для защиты от пыли и мелких частиц. Подходят для строительных и ремонтных работ.",
		"created_at": ISODate("2024-12-18T14:33:54.824Z"),
		"updated_at": ISODate("2024-12-18T14:33:54.824Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dd5bd5595612f0a21222"),

		"name": "Каска строительная белая Зубр",
		"dailyPrice": 30.0,
		"totalPrice": 600.0,
		"images": [
			"http://localhost:8000/api/resources/images/tools/1049c30b152de23ffe9667fba626782eb566c9ef5476b0fb08a714051475f500/1.png",
			"http://localhost:8000/api/resources/images/tools/1049c30b152de23ffe9667fba626782eb566c9ef5476b0fb08a714051475f500/2.png"
		],
		"features": {
			"Материал": "Полипропилен",
			"Регулировка": "Обхват головы",
			"Защита": "Механическая",
			"Назначение": "Строительные работы"
		},
		"rating": 0.0,
		"category": "Защитное оборудование",
		"type": "Каска",
		"description": "Прочная строительная каска с регулируемым размером. Надежная защита головы на стройплощадке.",
		"created_at": ISODate("2024-12-18T14:34:03.882Z"),
		"updated_at": ISODate("2024-12-18T14:34:03.882Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dd63d5595612f0a21223"),

		"name": "Каска Ударопрочная красная",
		"dailyPrice": 40.0,
		"totalPrice": 750.0,
		"images": [],
		"features": {
			"Материал": "Усиленный поликарбонат",
			"Регулировка": "Обхват и посадка",
			"Вентиляция": "Есть",
			"Назначение": "Работа на высоте"
		},
		"rating": 0.0,
		"category": "Защитное оборудование",
		"type": "Каска",
		"description": "Ударопрочная каска с вентиляцией для работы на высоте. Обеспечивает комфорт и надежную защиту.",
		"created_at": ISODate("2024-12-18T14:34:11.83Z"),
		"updated_at": ISODate("2024-12-18T14:34:11.83Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dd68d5595612f0a21224"),

		"name": "Каска с козырьком Safetop",
		"dailyPrice": 50.0,
		"totalPrice": 1000.0,
		"images": [],
		"features": {
			"Материал": "ABS-пластик",
			"Особенность": "Козырек",
			"Регулировка": "Размер головы",
			"Назначение": "Промышленные работы"
		},
		"rating": 0.0,
		"category": "Защитное оборудование",
		"type": "Каска",
		"description": "Каска с козырьком для работы на открытых площадках. Защищает от солнца и ударов.",
		"created_at": ISODate("2024-12-18T14:34:16.941Z"),
		"updated_at": ISODate("2024-12-18T14:34:16.941Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dd6ed5595612f0a21225"),

		"name": "Перчатки нитриловые Зубр",
		"dailyPrice": 10.0,
		"totalPrice": 150.0,
		"images": [],
		"features": {
			"Материал": "Нитрил",
			"Защита": "От химикатов и масел",
			"Размер": "Универсальный",
			"Назначение": "Работа с химическими веществами"
		},
		"rating": 0.0,
		"category": "Защитное оборудование",
		"type": "Перчатки рабочие",
		"description": "Прочные нитриловые перчатки, подходящие для работы с химикатами. Отлично защищают руки и обеспечивают комфорт.",
		"created_at": ISODate("2024-12-18T14:34:22.213Z"),
		"updated_at": ISODate("2024-12-18T14:34:22.213Z"),
		"reviews_count": 0
	},
	{
		"_id": ObjectId("6762dd89d5595612f0a21226"),
		"name": "Перчатки кожаные сварщика",
		"dailyPrice": 30.0,
		"totalPrice": 500.0,
		"images": [],
		"features": {
		    "Материал": "Натуральная кожа",
			"Защита": "От высоких температур",
			"Размер": "L",
			"Назначение": "Сварочные работы"
		},
		"rating": 0.0,
		"category": "Защитное оборудование",
		"type": "Перчатки рабочие",
		"description": "Кожаные перчатки, обеспечивающие надежную защиту при сварочных работах. Выдерживают высокие температуры.",
		"created_at": ISODate("2024-12-18T14:34:49.124Z"),
		"updated_at": ISODate("2024-12-18T14:34:49.124Z"),
		"reviews_count": 0
	},
	{
	    "_id": ObjectId("6762dd89d5595612f0a21227"),
	    "name": "Перчатки х/б с ПВХ покрытием",
        "dailyPrice": 5,
        "totalPrice": 80,
        "images": [],
        "features": {
            "Материал": "Хлопок и ПВХ",
            "Защита": "От механических повреждений",
            "Размер": "Универсальный",
            "Назначение": "Строительные и садовые работы"
          },
        "rating": 0.0,
        "category": "Защитное оборудование",
        "type": "Перчатки рабочие",
        "description": "Доступные и удобные перчатки с ПВХ покрытием для универсального использования. Обеспечивают хороший захват.",
        "created_at": ISODate("2024-12-18T14:34:49.124Z"),
		"updated_at": ISODate("2024-12-18T14:34:49.124Z"),
		"reviews_count": 0
	}
]);


db.getCollection(process.env.ORDER_COLLECTION).insertMany([
	{
		"_id": ObjectId("6762e4905644d6846bbf246f"),

		"tools": [
			ObjectId("6762db8ad5595612f0a21207"),

			ObjectId("6762dbe7d5595612f0a21208")

		],
		"start_leasing": ISODate("2024-12-12T15:00:35.437Z"),
		"end_leasing": ISODate("2024-12-30T15:00:35.437Z"),
		"price": 1620.0,
		"client": ObjectId("6762d6a2f6292fe72b752b5e"),

		"delivery_type": "to_door",
		"delivery_state": "delivered",
		"payment_type": "cash",
		"payment_state": "paid",
		"create_order_time": ISODate("2024-12-12T15:00:35.437Z")
	},
	{
		"_id": ObjectId("6762e517561db75d683b6941"),

		"tools": [
			ObjectId("6762db8ad5595612f0a21207"),

			ObjectId("6762dbe7d5595612f0a21208"),

			ObjectId("6762dbefd5595612f0a21209"),

			ObjectId("6762dc34d5595612f0a2120d")

		],
		"start_leasing": ISODate("2024-12-12T15:00:35.437Z"),
		"end_leasing": ISODate("2025-01-30T15:00:35.437Z"),
		"price": 7105.0,
		"client": ObjectId("6762d6d9f6292fe72b752b5f"),

		"delivery_type": "to_door",
		"delivery_state": "delivered",
		"payment_type": "cash",
		"payment_state": "paid",
		"create_order_time": ISODate("2024-12-12T15:00:35.437Z")
	},
	{
		"_id": ObjectId("6762f80747f9d95025a19268"),

		"tools": [
			ObjectId("6762dbefd5595612f0a21209"),

			ObjectId("6762dc34d5595612f0a2120d")

		],
		"start_leasing": ISODate("2024-12-18T10:00:00Z"),
		"end_leasing": ISODate("2024-12-25T10:00:00Z"),
		"price": 275.0,
		"client": ObjectId("6762d6a2f6292fe72b752b5e"),

		"delivery_type": "to_door",
		"delivery_state": "delivered",
		"payment_type": "cash",
		"payment_state": "paid",
		"create_order_time": ISODate("2024-12-18T10:00:00Z")
	},
	{
		"_id": ObjectId("6762f94047f9d95025a1926b"),

		"tools": [
			ObjectId("6762dc15d5595612f0a2120b"),

			ObjectId("6762dc27d5595612f0a2120c")

		],
		"start_leasing": ISODate("2024-12-18T15:00:00Z"),
		"end_leasing": ISODate("2024-12-20T15:00:00Z"),
		"price": 130.0,
		"client": ObjectId("6762d6ebf6292fe72b752b60"),

		"delivery_type": "to_door",
		"delivery_state": "delivered",
		"payment_type": "cash",
		"payment_state": "paid",
		"create_order_time": ISODate("2024-12-18T15:00:00Z")
	},
	{
		"_id": ObjectId("6762f98747f9d95025a1926e"),

		"tools": [
			ObjectId("6762dc67d5595612f0a21213"),

			ObjectId("6762dca1d5595612f0a21217")

		],
		"start_leasing": ISODate("2024-12-18T16:34:15.069Z"),
		"end_leasing": ISODate("2025-01-01T15:00:00Z"),
		"price": 11050.0,
		"client": ObjectId("6762d6ebf6292fe72b752b60"),

		"delivery_type": "to_door",
		"delivery_state": "delivered",
		"payment_type": "cash",
		"payment_state": "paid",
		"create_order_time": ISODate("2024-12-18T16:34:15.069Z")
	},
	{
		"_id": ObjectId("6762fda347f9d95025a1926f"),

		"tools": [
			ObjectId("6762dc67d5595612f0a21213"),

			ObjectId("6762dca1d5595612f0a21217")

		],
		"start_leasing": ISODate("2024-12-18T16:51:47.919Z"),
		"end_leasing": ISODate("2025-01-01T15:00:00Z"),
		"price": 11050.0,
		"client": ObjectId("6762d6d9f6292fe72b752b5f"),

		"delivery_type": "to_door",
		"delivery_state": "delivered",
		"payment_type": "cash",
		"payment_state": "paid",
		"create_order_time": ISODate("2024-12-18T19:51:47.922Z")
	}
]);


db.getCollection(process.env.REVIEW_COLLECTION).insertMany([
	{
		"_id": ObjectId("6762ea83cf5e24ef1c7ce0f1"),

		"toolId": ObjectId("6762db8ad5595612f0a21207"),

		"reviewerId": ObjectId("6762d6a2f6292fe72b752b5e"),

		"rating": 4,
		"date": ISODate("2024-12-19T15:22:28.835Z"),
		"text": "Очень удобный молоток-гвоздодер! Ручка не скользит, а вес идеально подходит для работы. Однако металл на гвоздодере немного мягче, чем ожидалось, и чуть согнулся после работы с твердыми гвоздями."
	},
	{
		"_id": ObjectId("6762ed4e2333862c37e6b76a"),

		"toolId": ObjectId("6762db8ad5595612f0a21207"),

		"reviewerId": ObjectId("6762d6d9f6292fe72b752b5f"),

		"rating": 2,
		"date": ISODate("2024-12-18T15:22:28.835Z"),
		"text": "Молоток оказался неудобным в использовании. Ручка хоть и прорезиненная, но скользит в руках при длительной работе. Гвоздодер согнулся после первой же попытки вытащить плотный гвоздь. За такую цену ожидал большего качества."
	},
	{
		"_id": ObjectId("6762eda72333862c37e6b76b"),

		"toolId": ObjectId("6762dbe7d5595612f0a21208"),

		"reviewerId": ObjectId("6762d6a2f6292fe72b752b5e"),

		"rating": 5,
		"date": ISODate("2024-12-19T15:22:28.835Z"),
		"text": "Отличный молоток! Прочный, тяжелый и идеально подходит для слесарных работ. Двухкомпонентная ручка действительно снижает вибрацию, работать с ним комфортно даже длительное время. Полностью доволен покупкой."
	},
	{
		"_id": ObjectId("6762ee022333862c37e6b76c"),

		"toolId": ObjectId("6762dbe7d5595612f0a21208"),

		"reviewerId": ObjectId("6762d6d9f6292fe72b752b5f"),

		"rating": 4,
		"date": ISODate("2024-12-18T15:22:28.835Z"),
		"text": "Хороший молоток, тяжёлый и качественный. Ручка удобная, но покрытие немного стирается после долгого использования. В остальном инструмент оправдал ожидания."
	},
	{
		"_id": ObjectId("6762f8ac47f9d95025a19269"),

		"toolId": ObjectId("6762dbefd5595612f0a21209"),

		"reviewerId": ObjectId("6762d6a2f6292fe72b752b5e"),

		"rating": 4,
		"date": ISODate("2024-12-26T10:00:00Z"),
		"text": "Отличный столярный молоток, но немного легковат для крупных задач."
	},
	{
		"_id": ObjectId("6762f8d747f9d95025a1926a"),

		"toolId": ObjectId("6762dc34d5595612f0a2120d"),

		"reviewerId": ObjectId("6762d6d9f6292fe72b752b5f"),

		"rating": 5,
		"date": ISODate("2024-12-26T10:00:00Z"),
		"text": "Ключ удобный, антикоррозийное покрытие работает отлично. Рекомендую!"
	},
	{
		"_id": ObjectId("6762f95247f9d95025a1926c"),

		"toolId": ObjectId("6762dc15d5595612f0a2120b"),

		"reviewerId": ObjectId("6762d6ebf6292fe72b752b60"),

		"rating": 4,
		"date": ISODate("2024-12-22T10:00:00Z"),
		"text": "Отвертка плоская оказалась надежной, но ручка чуть скользила."
	},
	{
		"_id": ObjectId("6762f96a47f9d95025a1926d"),

		"toolId": ObjectId("6762dc27d5595612f0a2120c"),

		"reviewerId": ObjectId("6762d6ebf6292fe72b752b60"),

		"rating": 5,
		"date": ISODate("2024-12-22T10:00:00Z"),
		"text": "Набор бит Kraftool спас много раз. Отличный инструмент!"
	},
	{
		"_id": ObjectId("6762fdc747f9d95025a19270"),

		"toolId": ObjectId("6762dc67d5595612f0a21213"),

		"reviewerId": ObjectId("6762d6d9f6292fe72b752b5f"),

		"rating": 5,
		"date": ISODate("2025-01-02T15:00:00Z"),
		"text": "Шлифмашина Bosch показала себя идеально! Рекомендую."
	},
	{
		"_id": ObjectId("6762fdd947f9d95025a19271"),

		"toolId": ObjectId("6762dca1d5595612f0a21217"),

		"reviewerId": ObjectId("6762d6ebf6292fe72b752b60"),

		"rating": 4,
		"date": ISODate("2025-01-02T15:00:00Z"),
		"text": "Перфоратор мощный, но немного тяжеловат для долгой работы."
	}
]);


