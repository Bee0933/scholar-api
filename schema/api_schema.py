from turtle import st
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, StrictBool, validator
from decouple import config
from enum import Enum


# sign-in end-point schema
class signUser(BaseModel):
      username : str = Field(default=None, max_length=30, description="user unique name")
      email : EmailStr = Field(default=None, description='user email for log-in')
      password1 : str = Field(default=None, description='user password for log-in')
      password2 : str = Field(default=None, description='confirm user password')

      @validator('password2')
      def passwords_match(cls, v, values, **kwargs):
            if 'password1' in values and v != values['password1']:
                  raise ValueError('passwords do not match')
            return v
      class config:
            orm_mode=True
            schema_extra = {
                  "username" : "<username>",
                  "email" : "<user@email.com>",
                  "password" : "<password>",
            }

# log-in end-point schema 
class logUser(BaseModel):
      email : EmailStr = Field(default=None, description='user email to log-in')
      password : str = Field(default=None, description='user password for log-in')
      class config:
            orm_mode=True
            schema_extra = {
                  "email" : "<user@email.com>",
                  "password" : "<password>",
            }

# crawler input schema
class crawlInput(BaseModel):
      keyword : str = Field(default=None)
      no_of_article : int = Field(default=config('max_articles'), lt=int(config('max_articles'))+1)
      allow_links : StrictBool = Field(default=True, description="Allow scraper to extract links")
      allow_authors : StrictBool = Field(default=True, description="Allow scraper to extract authors")
      allow_summary : StrictBool = Field(default=True, description="Allow scraper to extract summary")
      class config:
            orm_mode=True
            schema_extra = {
                  "keyword" : "<search keyword>",
                  "no_of_article" : "<30>",
                  "allow_links" : "<True>",
                  "allow_authors" : "<True>",
                  "allow_summary" : "<True>",
            }
            
# jwt auth
class Settings(BaseModel):
      authjwt_secret_key : str = config('secret')

