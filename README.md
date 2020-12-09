# Sale Services
Core service for manage sale-staff and sale-job
## Install and running app
```
$ git clone git@git.teko.vn:digi-life/o2o/sale-service.git
$ cd sale-service
$ virtualenv -p python3 .venv
$ source .venv/bin/active
$ pip install -r requirements.txt
$ uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
## Migrations
### Create migration versions
```
$ alembic revision --autogenerate
```
### Upgrade head migration
`alembic upgrade head`

## Dockerize
### Build image
```
$ docker build -t sale-service .
```
### Run docker with uvicorn
```
$ docker run -it -p 8000:8000 --network="host" sale-service:latest
hoặc
$ docker run -d -p 8000:8000 sale-service:latest
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
- [ ] CRUD Team
- [ ] Add team-staff
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
