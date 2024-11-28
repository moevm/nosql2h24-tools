# nosql_template


## Предварительная проверка заданий

<a href=" ./../../../actions/workflows/1_helloworld.yml" >![1. Согласована и сформулирована тема курсовой]( ./../../actions/workflows/1_helloworld.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/2_usecase.yml" >![2. Usecase]( ./../../actions/workflows/2_usecase.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/3_data_model.yml" >![3. Модель данных]( ./../../actions/workflows/3_data_model.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/4_prototype_store_and_view.yml" >![4. Прототип хранение и представление]( ./../../actions/workflows/4_prototype_store_and_view.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/5_prototype_analysis.yml" >![5. Прототип анализ]( ./../../actions/workflows/5_prototype_analysis.yml/badge.svg)</a> 

<a href=" ./../../../actions/workflows/6_report.yml" >![6. Пояснительная записка]( ./../../actions/workflows/6_report.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/7_app_is_ready.yml" >![7. App is ready]( ./../../actions/workflows/7_app_is_ready.yml/badge.svg)</a>

## Run dev using docker
```
cd deployment/dev/
```
```
docker-compose up -d
```
**Frontend**
```
http://localhost:5173/
```
**Backend**
```
http://localhost:8000/
```
**Swagger UI**
```
http://localhost:8000/docs
```
## Default credentials

### Worker
- **email**: `worker@example.com`
- **password**:  `worker_123`

### Client
- **email**: `client@example.com`
- **password**:  `client_123`



## Run backend tests using docker
```sh
cd deployment/test/
```
```
docker-compose up -d
```
**Expected output** `======================= 110 passed, 44 warnings in 5.28s =======================`
