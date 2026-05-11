#import the create engine
from sqlmodel import Session,create_engine
#import the settings from the config.py
from config import settings

#create the engine
engine=create_engine(
    settings.DATABASE_URL,
    echo=True
)

#define the generator function
  #1.opens the connection 
  #2.hands it to the api route
  #3.closes it automatically once the api response is done 
def get_session():
    with Session(engine) as session:
        yield session 