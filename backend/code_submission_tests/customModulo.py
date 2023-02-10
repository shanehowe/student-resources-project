def formatAssertion(inputs, recieved, expected) -> str:
    return f"Error:\n\tInput: {inputs}\n\tRecieved: {recieved}\n\tExpected: {expected}"

def solution(num, divisor):
    n = num // divisor
    x = n * divisor
    return num - x


test_cases = [
    {
        "num": 10,
        "divisor": 2
    },
    {
        "num": 14,
        "divisor": 3
    },
    {
        "num": 99,
        "divisor": 87
    },
    {
        "num": 699,
        "divisor": 66
    },
    {
        "num": 11,
        "divisor": 2
    }
]

def test(userFunction, sampleInput=None):
    if sampleInput is not None:
        return userFunction(sampleInput)
    
    for case in test_cases:
        num = case.get("num")
        divisor = case.get("divisor")
        try:
            recieved = userFunction(num, divisor)
            expected = solution(num, divisor)
            assert recieved == expected
        except AssertionError:
            return formatAssertion(
                inputs=f"num={num}, divisor={divisor}", recieved=recieved, expected=expected
                )
        except Exception as e:
            return e
    
    return True