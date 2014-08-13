ret = 0
def a(s):
    global ret
    cnt = 0
    for i in s:
	ret = ret + i
	yield cnt
	cnt = cnt + 1

for i in a([4,5,6]):
    print i
print ret
ret = 0
a([3,4,5])
print ret


