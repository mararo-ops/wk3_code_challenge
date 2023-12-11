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


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer(), primary_key=True)
    full_name = Column(String())

    reviews = relationship('Review', backref=backref('customer'))
    restaurants = relationship('Restaurant', secondary=restaurant_customer, back_populates='customers')

    def __repr__(self):
        return f'Customer(id={self.id}, ' + \
            f'name={self.full_name})'

    def favorite_restaurant(self):
        favorite_restaurant = (
            session.query(Restaurant)
            .join(Review)
            .filter(Review.customer == self)
            .order_by(Review.star_rating.desc())
            .first()
        )
        return favorite_restaurant

    def add_review(self, restaurant, rating):
        new_review = Review(star_rating=rating, restaurant=restaurant, customer=self)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        session.query(Review).filter(Review.restaurant == restaurant, Review.customer == self).delete()


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer(), primary_key=True)
    star_rating = Column(Integer())
    created_at = Column(DateTime(), server_default=func.now())

    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))

    def full_review(self):
        return f'Review for {self.restaurant.name} by {self.customer.full_name}: {self.star_rating} stars'

    def __repr__(self):
        return f'Review(id={self.id}, ' + \
            f'star_rating={self.star_rating}, ' + \
            f'created_at={self.created_at})'