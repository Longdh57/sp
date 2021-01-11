# Sale Services
Core service for manage sale-staff and sale-job
## Install and running app
```
$ git clone git@git.teko.vn:digi-life/o2o/sale-service.git
$ cd sale-service
$ virtualenv -p python3 .venv
$ source .venv/bin/active
$ pip install -r requirements.txt
$ cp .env.example .env
$ uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
## Migrations
```
$ alembic revision --autogenerate   # Create migration versions
$ alembic upgrade head              # Upgrade head migration
```

## Docker Compose
Cần cấu hình docker compose để sử dụng các service:
- Minio: Upload file...
### Minio
- Check cấu hình minio (MINIO_PORT, MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY) trong .env
- Mặc định dữ liệu trong minio đồng bộ với local ở path .docker/minio
### Run docker compose
```
$ docker-compose up -d              # Run all docker service/container
$ docker-compose down               # Stop all docker service
$ docker-compose ps                 # Show all docker service
```

## Feature

### Sale service
    - Danh sách staff
    - [ ] Synchronize staff
    - [ ] API staff list
    - Authen
    - [ ] Login with account/pass
    - [ ] Login via Google Oauth
    - Authorization
    - [ ] Mapping user-staff
    - [ ] Auto grant permission for staff
    - Mapping staff-shop
    - [ ] Import staff-shop
    - [ ] List shop with staff

### Manage Sale-Jobs
    - Danh sách Sale-Job
    - [ ] CRUD job
    - Gán job cho sale
    - [ ] Import sale job
    - Form submit job
    - [ ] CRUD form submit job
    - Notification
    - [ ] Push noti when grant shop for sale
    - [ ] Push noti when job expired date
