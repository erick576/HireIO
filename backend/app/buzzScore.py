import PyPDF2
import os
from os import listdir
from os.path import isfile, join
from io import StringIO
import pandas as pd
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
from spacy.matcher import PhraseMatcher

class buzzScore:
    def __init__(self):
        self.mypath='../../resumes' #enter your path here where you saved the resumes
        self.onlyfiles = [os.path.join(self.mypath, f) for f in os.listdir(self.mypath) if os.path.isfile(os.path.join(self.mypath, f))]


    #Function to read resumes from the folder one by one

    def pdfextract(self,file):
        fileReader = PyPDF2.PdfFileReader(open(file,'rb'))
        countpage = fileReader.getNumPages()
        count = 0
        text = []
        while count < countpage:    
            pageObj = fileReader.getPage(count)
            count +=1
            t = pageObj.extractText()
            # print (t)
            text.append(t)
        return text

    #function to read resume ends


    #function that does phrase matching and builds a candidate profile
    def create_profile(self,file):
        text = self.pdfextract(file) 
        text = str(text)
        text = text.replace("\\n", "")
        text = text.lower()
        #below is the csv where we have all the keywords, you can customize your own
        keyword_dict = pd.read_csv('./buzzwords.csv')
        ml_engineer = [nlp(text) for text in keyword_dict['machine learning engineering'].dropna(axis = 0)]
        r_dev = [nlp(text) for text in keyword_dict['r developer'].dropna(axis = 0)]
        py_dev = [nlp(text) for text in keyword_dict['python developer'].dropna(axis = 0)]
        nlp_dev = [nlp(text) for text in keyword_dict['nlp developer'].dropna(axis = 0)]
        java_dev = [nlp(text) for text in keyword_dict['java developer'].dropna(axis = 0)]
        cloud = [nlp(text) for text in keyword_dict['cloud engineer'].dropna(axis = 0)]
        devops = [nlp(text) for text in keyword_dict['devops'].dropna(axis = 0)]
        data_eng =[nlp(text) for text in keyword_dict['data engineer'].dropna(axis = 0)]
        
        matcher = PhraseMatcher(nlp.vocab)
        matcher.add('Machine_Learning', None, *ml_engineer)
        matcher.add('R', None, *r_dev)
        matcher.add('Python', None, *py_dev)
        matcher.add('NLP', None, *nlp_dev)
        matcher.add('Java', None, *java_dev)
        matcher.add('Cloud', None, *cloud)
        matcher.add('Devops', None, *devops)
        matcher.add('Data_Engineering', None, *data_eng)
        doc = nlp(text)
        
        d = []  
        matches = matcher(doc)
        for match_id, start, end in matches:
            rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
            span = doc[start : end]  # get the matched slice of the doc
            d.append((rule_id, span.text))      
        keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i,j in Counter(d).items())
        
        ## convertimg string of keywords to dataframe
        df = pd.read_csv(StringIO(keywords),names = ['Keywords_List'])
        df1 = pd.DataFrame(df.Keywords_List.str.split(' ',1).tolist(),columns = ['Subject','Keyword'])
        df2 = pd.DataFrame(df1.Keyword.str.split('(',1).tolist(),columns = ['Keyword', 'Count'])
        df3 = pd.concat([df1['Subject'],df2['Keyword'], df2['Count']], axis =1) 
        df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))
        
        base = os.path.basename(file)
        filename = os.path.splitext(base)[0]
        
        name = filename.split('_')
        name2 = name[0]
        name2 = name2.lower()
        ## converting str to dataframe  
        name3 = pd.read_csv(StringIO(name2),names = ['Candidate Name'])
        
        dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis = 1)
        dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace = True)

        return(dataf)
            
    #function ends
            
    #code to execute/call the above functions


    # sample2=new_data.to_csv('candidates.csv')

    def compute(self):
        final_database=pd.DataFrame()
        i = 0 
        while i < len(self.onlyfiles):
            file = self.onlyfiles[i]
            dat = self.create_profile(file)
            final_database = final_database.append(dat)
            i +=1
            # print(final_database)

            
        #code to count words under each category and visulaize it through Matplotlib

        final_database2 = final_database['Keyword'].groupby([final_database['Candidate Name'], final_database['Subject']]).count().unstack()
        final_database2.reset_index(inplace = True)
        final_database2.fillna(0,inplace=True)
        new_data = final_database2.iloc[:,1:]
        new_data.index = final_database2['Candidate Name']
        return new_data
# print(new_data['Java'])