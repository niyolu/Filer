# Filer

### Installation

##### Backend

1. make sure you have python >= 3.10 installed
2. navigate to `app/backend`
3. in sperate terminals execute:
   - db: `docker-compose up`
   - wait for it db startup
   - webserver: `uvicorn app.main:app`

##### Frontend

1. install npm
2. navigate to `app/frontend`
3. run `npm i`
4. run `npm start`