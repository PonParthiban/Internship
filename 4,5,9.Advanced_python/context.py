class mycontect:
    def __enter__(self):
        print("Entering the block")
        return "Resource"
    
    def __exit__(Self,exc_type, exc_value,traceback):
        print("Exiting the block")
        if exc_type:
            print("An exception occurred: ", exc_value)
        return True #prevent crash
    
with mycontect() as res:
    print("Inside the block with: ", res)