import os

# This code defines a function named default_secret_key that takes a class as its argument, sets the
# SECRET_KEY attribute of the class to the value of the SECRET_KEY environment variable or the 
# default value 'you-will-never-guess' if the environment variable is not set, and returns the class.
def default_secret_key(object):
    object.SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    return object

# The @default_secret_key decorator is applied to the Config class to set its SECRET_KEY attribute. 
# This allows for a more concise way of setting the SECRET_KEY attribute without explicitly calling 
# the function.
@default_secret_key
class Config:
    pass