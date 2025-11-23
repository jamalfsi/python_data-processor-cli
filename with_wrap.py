from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Decorator was here!")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def say_hello():
    """This function says hello is speicial string."""
    print("Hello!")

print("this is the funtion name: ",say_hello.__name__)   # Output: say_hello (now it’s correct!)
print(say_hello.__doc__)    # Output: This function says hello.
say_hello()
