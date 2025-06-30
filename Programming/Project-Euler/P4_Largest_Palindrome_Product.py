def is_palindrome(n):
    if str(n)[::-1] == str(n):
        return True
    else:
        return False

max_palindrome = 0
for i in range(999, 99, -1):
    for j in range(i, 99, -1):  # Avoid repeating lower pairs
        product = i * j
        if product <= max_palindrome:
            break  # No need to check further
        if is_palindrome(product):
            max_palindrome = product

print(max_palindrome)
