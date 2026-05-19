```python
import sys

def levenshtein_distance(A, B):
    len_A = len(A)
    len_B = len(B)
    
    if len_A == 0:
        return len_B
    if len_B == 0:
        return len_A
    
    dp = [[0] * (len_B + 1) for _ in range(len_A + 1)]
    
    for i in range(len_A + 1):
        dp[i][0] = i
    for j in range(len_B + 1):
        dp[0][j] = j
    
    for i in range(1, len_A + 1):
        for j in range(1, len_B + 1):
            cost = 0 if A[i - 1] == B[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,      # Deletion
                           dp[i][j - 1] + 1,      # Insertion
                           dp[i - 1][j - 1] + cost)  # Substitution
    
    return dp[len_A][len_B]

def main():
    input_data = sys.stdin.read().strip().splitlines()
    if len(input_data) < 2:
        A = input_data[0] if len(input_data) > 0 else ""
        B = ""
    else:
        A, B = input_data[0], input_data[1]
    
    distance = levenshtein_distance(A, B)
    sys.stdout.write(f"{distance}\n")

if __name__ == "__main__":
    main()
```