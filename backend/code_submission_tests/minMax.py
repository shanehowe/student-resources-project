def solution(nums):
    """
    Find the minumum and maximum numbers in list
    Returns the sum of them
    With out the use of built in min/max functions
    if length of nums is 0 returns 0
    """
    if not nums:
        return 0
    return sum([min(nums), max(nums)])


def test(userFunction, sampleInput=None):
    testCases = [[59, 71, 13, 91, 80, 43, 75, 54, 35, 62], [73, 9, 52, 38, -12, -8, 47, 21, 96, 55], [33, 3, 54, -6, 36, 26, 27, 67, 89, 63], [57, -6, 54, 90, 33, -13, 36, 51, 97, 36], [56, 84, 37, -13, 13, 44, 23, 43, 22, -2], [96, 67, 29, 22, 60, 51, 26, 81, 48, 35], [80, 91, 24, -7, 18, 58, 8, 100, 2, 66], [6, 58, 94, 78, 0, 65, 10, 83, 37, 70], [], [1]]
    if sampleInput is not None:
        return userFunction(testCases[0])
    
    # Test Cases
    for case in testCases:
        try:
            recieved = userFunction(case)
            expected = solution(case)
            assert recieved == expected
        except AssertionError:
            return f"Error:\n\tInput: {case}\n\tRecieved: {recieved}\n\tExpected: {expected}"
        except Exception as e:
            return f"Error:\n{e}"
    return True