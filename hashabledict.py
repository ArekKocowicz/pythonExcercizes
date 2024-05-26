class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

a=hashabledict() #create hashable dictionary using constructor

a["name"]="GND" #give is key-value pair
print(a)

b=hashabledict({"name" : "VCC"}) #create hashable dictionary and give it key-value pair
print(b)

print("type(a) is {}".format(type(a)))

#now it will be possible to create a set of dictionaries
myset={a,b}

#now let's try the same with unnamed dictionaries
myset2={hashabledict({"name" : "VDD"}), hashabledict({"name" : "PGND"})}
