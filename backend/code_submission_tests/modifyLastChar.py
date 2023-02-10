def formatAssertion(inputs, recieved, expected) -> str:
    return f"Error:\n\tInput: {inputs}\n\tRecieved: {recieved}\n\tExpected: {expected}"

def solution(text: str, n: int) -> str:
    """
    Finds the last char in text. 
    Appends that char to end of text N(modifyCount) amount of times
    """
    lastChar = text[-1]
    text += lastChar * n
    return text


def test(userFunction, sampleInput=None):
    if sampleInput is not None:
        return userFunction(sampleInput)
    
    # Test cases
    testCases = [

        {
            "text_": "Hello",
            "n": 5
        },
        {
            "text_": "whats up doc?",
            "n": 4
        },
        {
            "text_": "ooh la la",
            "n": 7
        },
        {
            "text_": "Bye",
            "n": 0
        },
        {
            "text_": "Python",
            "n": 0
        }
    ]

    for case in testCases:
        text_ = case.get("text_")
        n = case.get("n")
        try:
            recieved = userFunction(text_, n)
            expected = solution(text_, n)
            assert recieved == expected
        except AssertionError:
            return formatAssertion(
                inputs=f"n={n}, text={text_}", recieved=recieved, expected=expected
                )
        except Exception as e:
            return e
    return True