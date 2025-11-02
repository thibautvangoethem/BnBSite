def test(input: int):
    sum_value = 3 + int((input - 1) * 24 / 1999)
    base = sum_value // 3
    remainder = sum_value % 3
    digits = [base] * 3
    for i in range(remainder):
        digits[i] += 1
    for i in range(3):
        if digits[i] < 1:
            digits[i] = 1
        elif digits[i] > 9:
            digits[i] = 9
    print(f"{input}: {digits}")


if __name__ == "__main__":
    for i in range(2099):
        test(i + 1)
