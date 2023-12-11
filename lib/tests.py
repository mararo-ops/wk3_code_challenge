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


# Add the data to the session and commit the changes
    session.add_all([restaurant1, restaurant2, customer1, customer2])
    session.commit()

    

    review1 = Review(star_rating=4, restaurant=restaurant1, customer=customer1)
    review2 = Review(star_rating=5, restaurant=restaurant2, customer=customer1)
    review3 = Review(star_rating=3, restaurant=restaurant1, customer=customer2)
