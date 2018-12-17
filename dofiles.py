#coding:utf-8
import argparse
import  do_spaces_utils
def readargs():
    parser = argparse.ArgumentParser(description='Digital Ocean Spaces Files')
    parser.add_argument('-l','--list',dest='list', action='store_true', default=False,
                        help="list all files"
                        )

    parser.add_argument('-u','--upload',
                        action='store',
                        nargs='?',
                        dest = 'filepath',
                        help = "Upload file"
                        )
    parser.add_argument('-k','--key',
                        action='store',
                        nargs='?',
                        dest='key',
                        default="-",
                        help='Remote key file',)

    # subparser = parser.add_subparsers(help="Command to do")
    # parser_lists=subparser.add_parser('list',help='List files')
    # parser_upload=subparser.add_parser('upload',help='Upload files')
    # parser_download=subparser.add_parser('download',help='Upload files')


    # parser_lists.add_argument('-l','--list',action='store_true',dest='listfiles',help="list all files")
    # parser_upload.add_argument('download',action='append',nargs='*',help="downloads <key> file into target <dir> ")
    # subparser.add_parser('CP')
    # subparser.add_parser('Download')

    res = parser.parse_args()
    print "RES:{}".format(res)



    if res.list:
        print "LISTING FILES and exit"


    if res.filepath:
        print u"uploading file \'{}\' with key {} ".format(res.upload,res.key)

    # res = parser_lists.parse_args()
    # print res
    # if res.listfiles:
    #     res=do_spaces_utils.MyBucket().listfiles()
    #     for item in res:
    #         print u"{}".format(item)
    #     print "-"*10
    #     print u"Total {} items".format(len(res))
    #     exit(0)
    # if res.download:
    #     print res.download[1]
    #     print res.download[2]
    #

    # print "Hello"

if __name__=='__main__':
    readargs()