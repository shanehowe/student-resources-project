def test(helloWorldFunc, sampleInput=None):
    if sampleInput is not None:
        return helloWorldFunc(sampleInput)
    try:
        arg = "Foo"
        expected = f"Hello {arg}"
        recieved = helloWorldFunc(arg)
        assert recieved == expected
    except AssertionError:
        return f"Error\nInput: {arg}\nRecieved: {helloWorldFunc(arg)}\nExpected: 'Hello {arg}'"
    except Exception as e:
        return e
    
    try:
        arg = "Bar"
        expected = f"Hello {arg}"
        recieved = helloWorldFunc(arg)
        assert recieved == expected
    except AssertionError:
        return f"Error\nInput: {arg}\nRecieved: {helloWorldFunc(arg)}\nExpected: 'Hello {arg}'"
    except Exception as e:
        return e
    
    return True


