from litprinter import LIT
def calculate_total(a, b):
    LIT(a, b, includeContext=True)  # Shows: LIT| [script.py:3] in calculate_total() >>> a: 10, b: 20
    return a + b
# Example usage
if __name__ == "__main__":
    result = calculate_total(10, 20)
