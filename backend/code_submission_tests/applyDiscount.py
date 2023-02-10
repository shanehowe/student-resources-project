def solution(price, discount):
    """
    Solution to be used against user submitted code
    """
    if price == 0:
        return price
    discountedPrice = price - (price * discount / 100)
    return round(discountedPrice, 2)



def test(userFunction, sampleInput: str=None):
    if sampleInput is not None:
        a, b = sampleInput.split(" ")
        return userFunction(a.replace("price",""), b.replace("discount", "")) == solution(a, b)
    
    # Test cases
    try:
        price = 100
        discount = 10
        recieved = userFunction(price, discount)
        expected = solution(price, discount)
        assert recieved == expected
    except AssertionError:
        return f"Error:\nInputs:\n\tprice={price}\n\tdiscount={discount}\nRecieved: {recieved}\nExpected: {expected}"
    except Exception as e:
        return e
    
    try:
        price = 90
        discount = 5
        recieved = userFunction(price, discount)
        expected = solution(price, discount)
        assert recieved == expected
    except AssertionError:
        return f"Error:\nInputs:\n\tprice={price}\n\tdiscount={discount}\nRecieved: {recieved}\nExpected: {expected}"
    except Exception as e:
        return e
    
    try:
        price = 17.50
        discount = 0
        recieved = userFunction(price, discount)
        expected = solution(price, discount)
        assert recieved == expected
    except AssertionError:
        return f"Error:\nInputs:\n\tprice={price}\n\tdiscount={discount}\nRecieved: {recieved}\nExpected: {expected}"
    except Exception as e:
        return e
    
    try:
        price = 11.33
        discount = 1
        recieved = userFunction(price, discount)
        expected = solution(price, discount)
        assert recieved == expected
    except AssertionError:
        return f"Error:\nInputs:\n\tprice={price}\n\tdiscount={discount}\nRecieved: {recieved}\nExpected: {expected}"
    except Exception as e:
        return e
    
    return True

