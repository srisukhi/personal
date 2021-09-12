class Solution:
    rvals = pd.Series({'M': 1000, 'D': 500, 'C': 100,
                       'L': 50, 'X': 10, 'V': 5, 'I': 1})
    def intToRoman(self, num: int) -> str:
        curnum = num
        rostr = 'M' * (curnum // digits['M'])
        curnum = curnum % digits['M']
        
        for ind in range(1, len(digits)):
            roman = digits.index[ind]
            digit = digits[roman]
            rprevnum = digits.index[ind - 1]
            rprevval = digits[rprevnum]
            if digit == rprevval / 2:
                rostr += roman * (curnum // digit)
            elif curnum >= 4 * digit:
                rostr += roman + rprevnum
            else:
                rostr += roman * (curnum // digit)
        
        
        rolist += [] 
