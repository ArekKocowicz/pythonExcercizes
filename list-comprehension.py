#!/usr/bin/env python
import numpy as np



if __name__ == "__main__":
    print("test")
    random_numbers = np.random.randint(10, size=10)
    print(random_numbers)
    even_numbers = [x for x in random_numbers if x%2==0]
    #the first x in the line above is "yield"
    #for x in random_numbers is "generator expression"
    print(even_numbers)

    people=[{"name":"Tom"},{"name":"Bob"},{"name":"Mary"}]
    print(people)
    people_with_o=[person for person in people if "o" in person["name"] ]
    print(people_with_o)


