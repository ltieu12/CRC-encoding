# Name: Lam Tieu
# Banner ID: B00859543

import random

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
            # if the first bit in remainder is 1, quotient bit is 1, and we perform remainder XOR with divisor
            if remainder[0] == "1":
                remainder = xor(remainder, divisor)
            # otherwise, quotient bit is 0, and we perform remainder XOR with numbers of 0 equals to length of divisor
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
    print("Transmitted remainder: ", transmitRemainder)
    # the transmitted binary string is the original binary string with the calculated remainder
    transmitString = binString + transmitRemainder

    return transmitString

# Function receives a binary string and determines whether the received string has error or not
def receive_CRC(binString, polynomial):
    # perform long division on the received binary string and polynomial
    receiveRemainder = bit_division(binString, polynomial)
    print("Received remainder: ", receiveRemainder)
    # determine the remainder if received binary string is divisible by the polynomial
    zeroRemainder = "0" * (len(polynomial) - 1)

    # if the remainder of the long division is 0 (number of 0 is determined above), received message is error-free
    if receiveRemainder == zeroRemainder:
        print("Message received is error-free or undetected error")
    # otherwise, error detected in the message
    else:
        print("Error detected in message")

# Function creates burst error based on the length
def create_burst_error(message, errorLength):
    # get a list of bits in the message (string is immutable in Python)
    listOfBits = list(message)
    # randomly pick a start position for the burst error
    startErrorPosition = random.randint(0, len(listOfBits) - int(errorLength))

    # starting at the chosen position, change the bit from 0 to 1 and vice versa until the whole length of error
    for i in range(int(errorLength)):
        currentPosition = startErrorPosition + i
        if listOfBits[currentPosition] == "1":
            listOfBits[currentPosition] = "0"
        else:
            listOfBits[currentPosition] = "1"

    # put all the bits together into a string
    errorMessage = "".join(listOfBits)
    return errorMessage

# CRC-32 polynomial
genPolynomial = "100000100110000010001110110110111"
# generate a random binary string of 1520 bytes
messageLength = 1520 * 8
binaryString = ""
for i in range(messageLength):
    binaryString += str(random.randint(0, 1))

# calculate the remainder and transmitted message
transmittedMessage = transmit_CRC(binaryString, genPolynomial)
# perform the experiment 50 times
for i in range(50):
    # get user input for the length of burst error
    errorLength = input("Enter desired length of burst error: ")
    # create new message with burst error
    errorMessage = create_burst_error(transmittedMessage, errorLength)
    # determine whether error is detected or not
    receive_CRC(errorMessage, genPolynomial)