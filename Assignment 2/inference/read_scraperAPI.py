import urllib.request
import pandas as pd
import re

def read_scraper_API():
    datanew = pd.DataFrame()
    df = pd.read_csv(r'/Users/akshaybhoge/PycharmProjects/Edgar/inference/CompanyList.csv')
    # for i in range(len(df)):
    data=[]
    newlines=[]
    for i in range(len(df)):
        company = df.iloc[i]['Company']
        URL = "http://127.0.0.1:8081/call-transcripts/{}/2021".format(company)
        file = urllib.request.urlopen(URL)
        for line in file:
            decoded_line = line.decode("utf-8")
            doc = decoded_line.replace('\\n', '\n')
            print(len(doc))
            doc = doc.replace('Operator', '')
            doc = doc.replace('[Operator Instructions]', '')
            doc = doc.replace('Company Participants', '')
            doc = doc.replace('[ Instructions]', '')
            doc = doc.replace('Unidentified Analyst', '')
            doc = doc.replace('Company Participants', '')
            doc = doc.replace('Conference Call Participants', '')
            doc = re.sub('[^a-zA-Z0-9., \n]', '', doc)
           # doc=decoded_line['transcript']
            #docstr = ''.join(doc)
            #doc = re.sub('[^a-zA-Z\n\.]', ' ', doc)
        #print(docstr)
            sentences = (doc.splitlines())
            sentences = [x for x in sentences if x != '']
            print((len(sentences)))
            #sentence=[]
            #for s in sentences:
            #    if len(s) != 0:
            #        sentence.append(s)
            data = pd.DataFrame((sentences), columns=['sentence'])
            datanew = datanew.append(data, True)
    print(type(datanew))
    datanew.to_csv('/Users/akshaybhoge/PycharmProjects/Edgar/inference/Inference-transcript.csv', encoding='utf-8', index=False)

# if __name__ == '__main__':
#     read_scraper_API()