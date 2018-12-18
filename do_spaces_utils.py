#coding:utf-8
import ConfigParser
import boto3
import botocore
import os
import re
import random,string
import magic

cp=ConfigParser.ConfigParser()
configname='spaces.cfg'
cp.read(configname)




URL=cp.get('basic','URL')
ACCESS_KEY=cp.get('basic','ACCESS_KEY')
SECRET_KEY=cp.get('basic','SECRET_KEY')
REGION = cp.get('basic','REGION')
BUCKET = cp.get('basic','BUCKET')


def auth(bucket=BUCKET):
    """
    Должен  возвращать объект Bucket в котором хранятся все объекты
    :param bucket:
    :return:
    """
    s3 = boto3.resource('s3',
                        region_name=REGION,
                        endpoint_url=URL,
                        aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY,
                        )
    bct = s3.Bucket(bucket)
    return bct


def checkfilename(inputstr):
    """
    смотрит насколько строка которая была получена похожа на имя файла
    :param inputstr:
    :return: True  если  похоже и   False если нет
    """
    if inputstr==u'.DS_Store':
        return True
    pattern = re.compile(u".*\.[a-zA-Z0-9]{1,4}$")
    if pattern.match(inputstr):
        return True
    else:
        return False


class MyBucket(object):
    def __init__(self,bucket=BUCKET,*args,**kwargs):
        super(MyBucket,self).__init__(*args,**kwargs)
        self.bucket = auth()

    def putfile(self,filepath,key=u'',**kwargs):
        """
        берет  файл с  заданым именем и его кладет в корзину.
        :param kwargs:
        :return:
        """

        # assert  key , "Empty key not alloowed!"
        assert type(filepath)==unicode, "Filepath {} is not unicode".format(filepath)
        abspath = os.path.abspath(filepath)
        assert os.path.isfile(abspath), u"File {} is not a file ".format(abspath)
        if not key:
            key=re.sub('\s\s+',' ',abspath)
        path = re.sub('\s\s+',' ',abspath).encode('unicode-escape')
        created = self.bucket.Object(key)
        md={'initialpath':path}
        content_type = magic.from_file(abspath, mime=True)
        # print abspath
        res = created.put(Body=open(abspath,'rb'),
                          Metadata=md,ContentType=content_type
                          )
        assert res['ResponseMetadata']['HTTPStatusCode']==200, "ERROR:  Response {}".format(res['ResponseMetadata']['HTTPStatusCode'])
        return key

    def listfiles(self,**kwargs):
        """
        вщзвращает полый список доступных ключей
        :param kwargs:
        :return:
        """
        #todo   по мере роста количества файлов надо учиться делать тут пагинацию
        res= []
        for obj in self.bucket.objects.all():
            res.append(obj.key)
        return res

    def getinitialpath(self,key):
        """
        По ключу возвращает значение поля  :return initialpath
        из метаданных  предварительно  его перекодировав
        Если объект не найден то возвращает -1
        :param key:
        :return initialpath:
        """
        try:
            meta = self.bucket.Object(key).metadata
        except botocore.exceptions.ClientError: # будем считать что это нужно тот случай когда  объект не найден.
            return '-1'
        return meta.get('initialpath','').decode('unicode-escape')

    def list_initialpath(self):
        initialpath_list=[]
        keys=[]
        for obj in self.bucket.objects.all():
            initialpath_list.append(obj.Object().metadata.get('initialpath','').decode('unicode-escape'))
            keys.append(obj.key)
        return initialpath_list,keys

        pass

    def putdir(self,dirname):
        """
        загружает  каталог на сервер вместе с подкаталогами.
        возвращает список ключей загруженных файлов
         ключ соответствует полному имени файла.
        :param: (unicode): dirname
        :return (list):list of keys (list)
        """
        assert type(dirname)==unicode,u"Dirname {}:{} is not unicode".format(type(dirname),dirname)
        assert os.path.isdir(dirname),u"{} is not a directory".format(dirname)
        keys=[]
        for i in os.listdir(dirname):
            fullp=os.path.join(dirname,i)

            if os.path.isfile(fullp):
                key=self.putfile(fullp)
                keys.append(key)
            elif os.path.isdir(fullp):
                keysdir = self.putdir(fullp)
                keys.extend(keysdir)
        return keys

    def find_object_by_string(self,pattern):
        """
        Ищет объекты по вхождению подстроки  в  названии ключа
        :param pattern:
        :return:(list): список ключей
        """
        assert type(pattern)==unicode, u"Patterrn {}:{} is not unicode".format(type(pattern),pattern)
        search = re.compile(u".*{}.*".format(pattern))
        res=[]
        for o in self.bucket.objects.all():
            if search.match(o.key):
                res.append(o.key)
        return res

    def downloadfile(self,**kwargs):
        """
        :param kwargs:
        :param key:(unicode): если не представлен то ошибка  поднимается
        :param targetdir: -  каталог в который надо записать файл.если не представлен то  текущий.
        :return:
        """
        assert kwargs.get('key',''), "No key provided with key= arg"
        key=kwargs.get('key','')
        targetdir = kwargs.get('targetdir','.')
        assert os.path.isdir(targetdir), u'Targetdir {} is not a directory'.format(targetdir)
        filename = os.path.basename(key)
        if checkfilename(filename):
            filename = os.path.join(os.path.abspath(targetdir),filename)
        else: # если Filename в Key   на имя не похож то придмываем случайное
            #todo  сделать попытку достать имя файла из метаданных.
            filename = u''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
            filename = u".".join((filename, u"tmp"))
        try:
            self.bucket.download_file(key,filename)
        except Exception as e:
            # print e
            raise AssertionError("Key not found")
        return os.path.abspath(filename)

    def deletefile(self,key='',**kwargs):
        """
        должен   Удалять файл а Если ключ  неверен то пусть падает
        :param key:
        :param kwargs:
        :return:
        """
        assert type(key)==unicode or type(key)==str,u"Key={}:{} is not unicode ro string ".format(type(key),key)
        try:
            self.bucket.Object(key).load() # нужно чтобы он падал когда ключ неправильный
        except Exception as e:
            raise AssertionError("Key not found")

        res = self.bucket.Object(key).delete()
        if 300 > res['ResponseMetadata']['HTTPStatusCode']>=200:
            return 0
        else:
            return res['ResponseMetadata']['HTTPStatusCode']

    def list_key_prefix(self,prefix=''):
        """
        Возвращает список ключей с  начинающихся с префиcа prefix.
        :param prefix:
        :return:
        """

        res = []
        # for obj in self.bucket.objects.all():
        #     if obj.key.startswith(prefix):
        #         res.append(obj.key)
        for obj in self.bucket.objects.filter(Prefix=prefix):
            res.append(obj.key)
        return res



