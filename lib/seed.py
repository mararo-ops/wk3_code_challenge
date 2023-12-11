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

