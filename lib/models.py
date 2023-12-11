from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///restaurants.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

restaurant_customer = Table(
    'restaurant_customers',
    Base.metadata,
    Column('restaurant_id', ForeignKey('restaurants.id'), primary_key=True),
    Column('customer_id', ForeignKey('customers.id'), primary_key=True),
    extend_existing=True,
)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(Integer())

    reviews = relationship('Review', backref=backref('restaurant'))
    customers = relationship('Customer', secondary=restaurant_customer, back_populates='restaurants')

    def fanciest(self):
        fancy_restaurant = session.query(Restaurant).order_by(Restaurant.price.desc()).first()
        return fancy_restaurant

    def all_reviews(self):
        review_strings = [f'Review for {self.name} by {review.customer.full_name}: {review.star_rating} stars' for review in self.reviews]
        return '\n'.join(review_strings)

    def __repr__(self):
        return f'Restaurant(id={self.id}, ' + \
            f'name={self.name}, ' + \
            f'created_at={self.created_at})'
