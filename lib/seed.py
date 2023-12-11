from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant, Customer, Review
from faker import Faker

# Initialize Faker
fake = Faker()

# Create the database engine and bind it to your SQLAlchemy models
engine = create_engine('sqlite:///restaurants.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def create_fake_restaurant():
    return Restaurant(
        name=fake.company(),
        price=fake.random_int(min=1, max=5)
    )

def create_fake_customer():
    return Customer(
        full_name=fake.name()
    )

def create_fake_review(restaurant, customer):
    return Review(
        star_rating=fake.random_int(min=1, max=5),
        restaurant=restaurant,
        customer=customer
    )


if __name__ == '__main__':
    # Generate fake data and add it to the database
    for _ in range(10):  # Change the number to control the number of records
        restaurant = create_fake_restaurant()
        customer = create_fake_customer()
        session.add_all([restaurant, customer])
        session.commit()

        review = create_fake_review(restaurant, customer)
        session.add(review)
        session.commit()

    session.close()