import threading,time
i = 0
def thread_test(sz):
    global i
    print(sz[i],time.time())
    i=i+1

if __name__=='__main__':
    sz=[1,2,3,4,5,6,7,8,9,10]
    for i in range(len(sz)):
        t=threading.Thread(target=thread_test,args=(sz,))
        t.start()