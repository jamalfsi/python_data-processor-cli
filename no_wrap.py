def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Decorator was here!")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def say_hello():
    """This function says hello."""
    print("Hello!")

print(say_hello.__name__)   # Output: wrapper (not say_hello)
print(say_hello.__doc__)    # Output: None (not the original docstring)
say_hello()
