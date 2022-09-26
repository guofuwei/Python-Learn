sum = 0


def main():
    find(4)
    global sum
    print("All methods:%d" % (sum))


def find(n):
    if n == 0:
        global sum
        sum += 1
        return
    elif n < 0:
        return
    else:
        find(n-1)
        find(n-2)


if __name__ == "__main__":
    main()
