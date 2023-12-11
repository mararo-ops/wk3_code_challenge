from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant, Customer, Review  

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    # Create some sample data
    restaurant1 = Restaurant(name='Restaurant 1', price=3)
    restaurant2 = Restaurant(name='Restaurant 2', price=2)

    customer1 = Customer(full_name='John Doe' , restaurants= [restaurant1, restaurant2])
    customer2 = Customer(full_name='Jane Smith', restaurants = [restaurant1,restaurant2])
