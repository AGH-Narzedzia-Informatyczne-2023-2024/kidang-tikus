class Math:
    def suma(a, b):
        return a + b

    def roznica(a,b):
        return a - b

if __name__ == "__main__":
    print("Program do sumowania")
    deg = 123
    math = Math()
    print("Suma to %d" % math.suma(deg, 5))
