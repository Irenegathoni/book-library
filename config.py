#import a tool that let's me define settings(BaseSettings)
from pydantic_settings import BaseSettings ,SettingsConfigDict
from pydantic import computed_field
#define the class called 'settings' that holds the variables
class Settings(BaseSettings):
    #variable for the project name:string
    PROJECT_NAME:str="Book Library"
    #variable for secret key for jwt:string
    SECRET_KEY:str

    DB_HOST:str
    DB_DATABASE:str
    DB_USER:str
    DB_PASSWORD:str
    DB_PORT:int=5432
    ACCESS_TOKEN_EXPIRY_MINUTES:int=30
    ALGORITHM:str="HS256"
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
   
    #create a subclass(config) to tell pydantic to look into the .env file
    model_config= SettingsConfigDict(env_file=".env",extra="ignore")

 
#initialize the settings object so other files can import 'settings' 
settings=Settings()
