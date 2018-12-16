#coding:utf-8
import argparse
import  do_spaces_utils
def readargs():
    parser = argparse.ArgumentParser(description='Digital Ocean Spaces Files')
    parser.add_argument('-l','--list',action='store_true',dest='listfiles',help="list all files")
    parser.add_argument('download',nargs=2,help="downloads file into target dir ")
    res = parser.parse_args()
    if res.listfiles:
        res=do_spaces_utils.MyBucket().listfiles()
        for item in res:
            print u"{}".format(item)
        print "-"*10
        print u"Total {} items".format(len(res))
        exit(0)
    print res.download[1]

    # print "Hello"

if __name__=='__main__':
    readargs()