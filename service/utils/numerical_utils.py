import random

class NumericalUtils:
    def get_numerical_string(n):
        ans = ''
        nums = '0123456789'
        for _ in range(n):
            ans += nums[random.randint(0, len(nums)-1)]
        
        return ans