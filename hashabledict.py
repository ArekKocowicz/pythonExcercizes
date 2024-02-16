class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

a=hashabledict()

print(a)


a["name"]="GND"

print(a)
