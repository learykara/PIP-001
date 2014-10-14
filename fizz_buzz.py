
import sys


# Grab user supplied value in command line, if present & valid
# Otherwise, prompt user for upper limit value
try:
  UPPER_LIMIT = int(sys.argv[1])
except (IndexError, ValueError):
  while True:
    try:
      UPPER_LIMIT = int(raw_input('Enter an integer : '))
      break
    except ValueError:
      print 'Please enter a valid integer' 

print 'Fizz buzz counting up to ' + str(UPPER_LIMIT)

for x in range(1, UPPER_LIMIT):
  if (x % 3 == 0 and x % 5 == 0):
    print 'fizzbuzz'
  elif (x % 3 == 0):
    print 'fizz'
  elif (x % 5 == 0):
    print 'buzz'
  else:
    print x
  
