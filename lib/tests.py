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

 # Add the reviews to the session and commit the changes
    session.add_all([review1, review2, review3])
    session.commit()

# Test various methods
    # Example 1: Get the fanciest restaurant
    fancy_restaurant = restaurant1.fanciest()
    print(f'The fanciest restaurant is: {fancy_restaurant.name}')

    # Example 2: Get all reviews for a restaurant
    all_reviews = restaurant1.all_reviews()
    print('All reviews for Restaurant 1:')
    print(all_reviews)

    reviewed_restaurants = customer1.restaurants
    print(f"{customer1.full_name} has reviewed the following restaurants:")
    for restaurant in reviewed_restaurants:
        print(restaurant.name)

    # Example 3: Get the favorite restaurant for a customer
    favorite = customer1.favorite_restaurant()
    print(f"{customer1.full_name}'s favorite restaurant is: {favorite.name}")

    # Example 4: Add a new review for a restaurant
    new_review = Review(star_rating=4, restaurant=restaurant2, customer=customer2)
    session.add(new_review)
    session.commit()
    print("Added a new review")

    # Example 5: Delete reviews for a restaurant by a customer
    customer1.delete_reviews(restaurant1)
    session.commit()
    print(f"Reviews for {customer1.full_name} at {restaurant1.name} have been deleted.")

    session.close()  # Close the session
