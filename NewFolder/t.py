class t:
    a = 2
    def t(self,b):
        self.a = b
m = t()
b = t()
print(m.a)
print(b.a)
m.t(4)
print(m.a)
print(b.a)