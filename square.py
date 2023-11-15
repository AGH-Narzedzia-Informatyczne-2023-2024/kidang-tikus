def add_squares(a):
  #create sum = 0, is this unnecessary?
  sum=0

  #adding squares all squares of a, if a = 3 sum is 1 + 4 + 9
  
  for i in range(a):
    sum += (a+1)*(a+1)
    
  return sum
