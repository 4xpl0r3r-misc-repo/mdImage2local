import os,re ,requests, logging, shutil

LOG_FORMAT = "%(lineno)d - %(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

SAVE_PATH = ''
HOST = ''

os.chdir(SAVE_PATH)
fileList = os.popen("find . -name '*.md'").read().split('\n')

for writeupPath in fileList:
    if not writeupPath:
        continue
    imageURLs = []
    writeContent = ''
    with open(writeupPath,'r') as f:
        writeContent=f.read()
        imageURLs = re.findall(r'\!\[\]\((.+)\)',writeContent)
    if imageURLs:
        assetDirectory = writeupPath[:writeupPath.rindex('/')]+'/writeup.asset/'
        if(os.path.exists(assetDirectory)):
            shutil.rmtree(assetDirectory)
        os.makedirs(assetDirectory)
        for url in imageURLs:
            imageName = url.split('/')[-1]
            writeContent = writeContent.replace(url,'./writeup.asset/'+imageName)
            with open(assetDirectory + imageName, 'wb') as f:
                f.write(requests.get(HOST + url).content)
    with open(writeupPath,'w') as f:
        f.write(writeContent)
    logging.info('[Success] {}'.format(writeupPath))
    