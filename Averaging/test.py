class t:
    def __init__(self) -> None:
        self.a = [1,2]

    def update(self,a):
        self.a.append(a)

b1 = t()
print(b1.a)
b1.update(3)
print(b1.a)
b2 = t()
print(b2.a)
b2.update(4)
print(b2.a)
print(b1.a)