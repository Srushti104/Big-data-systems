import boto3
import re
import pandas as pd
import scaling

#comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
def cleaning_files():
    k = []
    Sent_m=[]
    Score_m=[]
    data_m = pd.DataFrame()

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('textfiles2')

    for obj in bucket.objects.all():
        key = obj.key
        k.append(key)

    files = list(k)
    print(files)

    for file in files:
        if file != 'call_transcripts/.DS_Store' and file != 'LabeledData/Labeled.csv' and file != 'Model/model.bin':
            with open( file, 'r') as f:
                doclist = [line for line in f]
                docstr = ''.join(doclist)
                docstr = re.sub('[^a-zA-Z\n\.-]', ' ', docstr)
                sentences = (docstr.splitlines())
                sentences = [x for x in sentences if x != '']
                Score = []
                Sentence = []
                Score1 = []
                for s in sentences:
                    if len(s) != 0:
                        res = scaling.get_sentiment(s)
                        #Score = (res["Sentiment"])
                        Score1.append(res["sentiment_score"])
                        Sentence.append(s)
                        Score.append(res["sentiment"])  # Remove once testing done
                        data = pd.DataFrame(list(zip(Sentence, Score1)), columns=['Sentence', 'Score'])#,'Sentiment'])
                data_m = data_m.append(data, True)


    data_m.to_csv('Labeled.csv', encoding='utf-8', index=False)
    print("Labeled csv created!")


# cleaning_files()


