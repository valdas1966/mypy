from ._factory import Storage, Factory

# Set up factory pattern integration
Storage.Factory = Factory
print(Storage.Factory)
