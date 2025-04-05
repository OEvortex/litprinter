
def test_will_fail():
    expected = 42
    actual = 41
    assert expected == actual, f"Expected {expected}, but got {actual}"

if __name__ == '__main__':
    test_will_fail()