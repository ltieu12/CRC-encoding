# Name: Lam Tieu
# Banner ID: B00859543


# Function simulates XOR operation on 2 binary strings (Python XOR operation does not support string)
def xor(num1, num2):
    result = ""
    # for loop starts at index 1 because the first index XOR result will always be 0 for division
    # we only need the remain bits after the first bit
    for i in range(1, len(num1)):
        # if 2 bit is different, XOR result is 1
        if num1[i] != num2[i]:
            result += "1"
        # otherwise, XOR result is 0
        else:
            result += "0"

    return result

# Function calculates long division of 2 binary string
# Using XOR operation and returns the final remainder
def bit_division(dividend, divisor):
    # determine number of bits in the dividend to be divided at a time (equals to number of bits in the divisor)
    divideLength = len(divisor)
    # create a variable for updating the remainder
    # initialize with the first n-bits of the dividend (n = number of bits in the divisor)
    # e.g.: M(x) = 1101010, G(x) = 101 => first remainder = 110
    remainder = dividend[:divideLength]
    # iterate through the dividend starting at the nth bit until the 1 index more than the length of the dividend (to cover division of the final bit)
    # e.g: M(x) = 1101010, G(x) = 101 => i starts at index 3 (bit 1; length of divisor is 3)
    for i in range(divideLength, len(dividend) + 1):
        # when i equals to the length of dividend, this means the final bit of the dividend has been put down for division
        # therefore, only calculate the remainder , no need to put down the next bit
        if i == len(dividend):
            # if the first bit in remainder is 1, quotient bit is 1 and we perform remainder XOR with divisor
            if remainder[0] == "1":
                remainder = xor(remainder, divisor)
            # otherwise, quotient bit is 0 and we perform remainder XOR with numbers of 0 equals to length of divisor
            # e.g.: G(x) = 101 => XOR with 000
            else:
                remainder = xor(remainder, "0" * divideLength)
        # otherwise, calculate the remainder and put down the next bit in dividend for the next division iteration
        else:
            # perform XOR operation similar to logic above, and put down the next bit accordingly
            if remainder[0] == "1":
                temp = xor(remainder, divisor)
                remainder = temp + dividend[i]
            else:
                temp = xor(remainder, "0" * divideLength)
                remainder = temp + dividend[i]

    return remainder

# Function determines the transmitted message of CRC, using long division to find remainder
def transmit_CRC(binString, polynomial):
    # padded binary string with number of 0 equals to the degree of polynomial
    # e.g.: polynomial is 4 bit => degree is 3 (starts at x^3) => padded 3 zeros
    paddedString = binString + "0" * (len(polynomial) - 1)
    # perform long division on the padded binary string with polynomial to get the remainder
    transmitRemainder = bit_division(paddedString, polynomial)
    print("Remainder: ", transmitRemainder)
    # the transmitted binary string is the original binary string with the calculated remainder
    transmitString = binString + transmitRemainder

    return transmitString

# Function receives a binary string and determines whether the received string has error or not
def receive_CRC(binString, polynomial):
    # perform long division on the received binary string and polynomial
    receiveRemainder = bit_division(binString, polynomial)
    # determine the remainder if received binary string is divisible by the polynomial
    zeroRemainder = "0" * (len(polynomial) - 1)

    # if the remainder of the long division is 0 (number of 0 is determined above), received message is error-free
    if receiveRemainder == zeroRemainder:
        print("Message received is error-free")
    # otherwise, error detected in the message
    else:
        print("Error detected in message")

# get input from users for the binary string and polynomial
binaryString = input("Enter a binary string: ")
genPolynomial = input("Enter a polynomial (in binary string): ")

transmittedMessage = transmit_CRC(binaryString, genPolynomial)
# print the results of the transmitted message
print("Transmitted message: ", transmittedMessage)
receive_CRC(transmittedMessage, genPolynomial)