from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from schema.api_schema import crawlInput
from crawler.crawler import dyn_crawl
from db.database import Session, engine
from db.models import History
import datetime


# create db session 
session = Session(bind=engine)


# creatte crawler router instance for web crawler
crawler_router = APIRouter(
      prefix='/crawl',
      tags=['CRAWL']
)

# crawl route
@crawler_router.get('/crawl' ,status_code=status.HTTP_200_OK)
async def crawl(crawl_values: crawlInput, Authorize: AuthJWT=Depends()): 
      try:
            # request access token from authorized user
            Authorize.jwt_required()

      except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='unauthorized token')

      # crawl google scholar with user defined requirements
      result = dyn_crawl(keyword=crawl_values.keyword, no_articles=int(crawl_values.no_of_article),
                        links=crawl_values.allow_links, author=crawl_values.allow_authors, 
                        summary=crawl_values.allow_summary)
      
      current_user = Authorize.get_jwt_subject()
      
      # record user crawler history to db
      new_history=History(
            username=current_user,
            keyword=crawl_values.keyword,
            date=datetime.datetime.now(datetime.timezone.utc)
      )
      session.add(new_history)

      session.commit()
      return {"result": result }
      

# history route 
@crawler_router.get('/history' ,status_code=status.HTTP_200_OK)
async def history(Authorize: AuthJWT=Depends()): 
      try:
            # request access token from authorized user
            Authorize.jwt_required()

      except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='unauthorized token')
      
      current_user = Authorize.get_jwt_subject()

      # query db for specific user's crawler history
      hist_data = session.query(History.date, History.keyword).filter(History.username == current_user).all()

      return {f"history data for {current_user}": hist_data}
      

