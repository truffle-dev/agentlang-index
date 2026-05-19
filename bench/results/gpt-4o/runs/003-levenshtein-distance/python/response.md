```python
import sys

def levenshtein_distance(A, B):
    len_a = len(A)
    len_b = len(B)
    
    # Create a matrix to store distances
    dp = [[0] * (len_b + 1) for _ in range(len_a + 1)]
    
    # Initialize the matrix
    for i in range(len_a + 1):
        dp[i][0] = i
    for j in range(len_b + 1):
        dp[0][j] = j
    
    # Compute the distances
    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            if A[i - 1] == B[j - 1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(dp[i - 1][j] + 1,    # Deletion
                           dp[i][j - 1] + 1,    # Insertion
                           dp[i - 1][j - 1] + cost)  # Substitution
    
    return dp[len_a][len_b]

def main():
    input_data = sys.stdin.read().strip().split('\n')
    A = input_data[0] if len(input_data) > 0 else ""
    B = input_data[1] if len(input_data) > 1 else ""
    
    distance = levenshtein_distance(A, B)
    sys.stdout.write(f"{distance}\n")

if __name__ == "__main__":
    main()
```