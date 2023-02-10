def formatAssertion(inputs, recieved, expected) -> str:
    return f"Error:\n\tInput: {inputs}\n\tRecieved: {recieved}\n\tExpected: {expected}"

def solution(string: str) -> str:
    return string[::-1]


def test(userFunction, sampleInput=None):
    if sampleInput is not None:
        return userFunction(sampleInput)
    
    # Test Cases
    testCases = [
        "Hello World",
        "The quick fox jumped over the moon",
        "",
        "Z",
        "ZzZ",
        "Hows it going?",
        "Where am I?",
        "123456789"
    ]

    for case in testCases:
        try:
            recieved = userFunction(case)
            expected = solution(case)
            assert recieved == expected
        except AssertionError:
            return formatAssertion(
                inputs=case, recieved=recieved, expected=expected
            )
        except Exception as e:
            return e
    return True
