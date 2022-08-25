from fastapi import FastAPI 
from decouple import config
import uvicorn
from api.auth_routes import auth_router
from api.crawl_routes import crawler_router
from fastapi_jwt_auth import AuthJWT
from schema.api_schema import Settings

# app instance
app = FastAPI()

# JWT config
@AuthJWT.load_config
def get_config():
      return Settings()



# include routers 
app.include_router(auth_router)
app.include_router(crawler_router)


if __name__ == '__main__':
      uvicorn.run(app, host=config('host'), port=config('port'))