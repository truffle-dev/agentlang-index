```python
import sys

def sieve_of_eratosthenes(n):
    if n < 2:
        return 0
    
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    for start in range(2, int(n**0.5) + 1):
        if is_prime[start]:
            for multiple in range(start*start, n + 1, start):
                is_prime[multiple] = False
    
    return sum(is_prime)

def main():
    input_data = sys.stdin.read().strip()
    N = int(input_data)
    prime_count = sieve_of_eratosthenes(N)
    sys.stdout.write(f"{prime_count}\n")

if __name__ == "__main__":
    main()
```