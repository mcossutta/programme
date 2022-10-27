def prout(a):
    return a+"x"

liste = ["1","2","3"]

print("\n\\newpage\n".join([prout(l) for l in liste]))