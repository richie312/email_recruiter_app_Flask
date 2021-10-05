# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 09:43:40 2020

@author: CN261
"""

import PyPDF2
import os
from io import StringIO
import pandas as pd
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
from spacy.matcher import PhraseMatcher

def pdfextract(file):
    """pdfextract() functions takes the resume as argument in pdf format
       and extract the text from the resume. It returns the dictionary
       which keeps the text in corpus and page count in count key respectively.
    """
    fileReader = PyPDF2.PdfFileReader(open(file,'rb'))
    countpage = fileReader.getNumPages()
    count = 0
    corpus = []
    while count < countpage:    
        pageObj = fileReader.getPage(count)
        count +=1
        t = pageObj.extractText()
        corpus.append(t)
    return {"corpus": corpus,"page_count":count}

#function that does phrase matching and builds a candidate profile
def create_profile(file, main_dir):
    """create_profile functions takes the resume as an argument and
       returns the dataframe; which shows the count of specfic skill
       in the given resume. main_dir is the base or the root directory
       of the project.
    """
    text = pdfextract(file) 
    text = [str(text['corpus'][i]) for i in range(len(text['corpus']))]
    corpus = [text[i].replace("\n", "") for i in range(len(text))]
    corpus = [corpus[i].lower().strip() for i in range(len(corpus))]
    
    #below is the csv where we have all the keywords, you can customize your own
    keyword_df = pd.read_csv(os.path.join(main_dir,'requirements.csv'),encoding = "ISO-8859-1")
    skill_list = keyword_df.columns.values.tolist()
    # Instantiate an empty dictionary to get all the keywords for each skill
    skills_keywords_dict = {}
    for i in range(len(skill_list)):
        skills_keywords_dict[skill_list[i] + "_{}".format('words')] = [nlp(keyword) for keyword in keyword_df[skill_list[i]].dropna(axis = 0)]
    
    matcher = PhraseMatcher(nlp.vocab)
    for i in list(skills_keywords_dict.keys()):
        phrase_list = [nlp(str(words)) for words in skills_keywords_dict[i]]
        matcher.add('{}'.format(i.split('_')[0]),None, *phrase_list) 
    
    document = []
    for i in corpus:
        document.append(''.join(str(i)))
    
    
    matches = []
    for page in document:
        matches.append(matcher(nlp(page)))
        matches
    
    d = []
    keywords = []    
    for i in range(len(matches)):
        for match_id, start, end in matches[i]:
            rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
            span = nlp(document[i])[start : end]  # get the matched slice of the doc
            d.append((rule_id, span.text))      
        keywords.append("\n".join(f'{i[0]} {i[1]} ({j})' for i,j in Counter(d).items()))
        
    keyword_string = ''
    for i in keywords:
        keyword_string += i
    ## convertimg string of keywords to dataframe
    df = pd.read_csv(StringIO(keyword_string),names = ['Keywords_List'])
    df1 = pd.DataFrame(df.Keywords_List.str.split(' ',1).tolist(),columns = ['Domain','Keyword'])
    df2 = pd.DataFrame(df1.Keyword.str.split('(',1).tolist(),columns = ['Keyword', 'Count'])
    df3 = pd.concat([df1['Domain'],df2['Keyword'], df2['Count']], axis =1) 
    df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))
    base = os.path.basename(file)
    filename = os.path.splitext(base)[0]
    name = filename.split('_')
    name2 = name[0]
    name2 = name2.lower()
    ## converting str to dataframe
    name3 = pd.read_csv(StringIO(name2),names = ['Candidate Name'])
    dataf = pd.concat([name3['Candidate Name'], df3['Domain'], df3['Keyword'], df3['Count']], axis = 1)
    dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace = True)
    
    # get the domain and its corresponding matching words with the requirements.csv
    Domain_dict = {}
    for i in list(set(df3['Domain'])):
        Domain_dict[i] = list(set(df3['Keyword'][df3['Domain'] == i].values.tolist()))
    return({"domain_frequency": dataf,
            "Domain_Keywords": Domain_dict})
    
def requirement_match(profile_output):
    """requirement_match takes the profile dataframe as an argument
       and computes the weightage score of each skill based on two prime
       factor; percentage of actual match (which is usually set by the
       reviewer) and percentage of key skill match for the specfic domain(
       which is also saved by the recruiter). The expectation value for specfic domain
       is saved in local .csv file name expectation_threshold.csv
    """
    # read the expectation threshold dataframe
    exp_threshold_df = pd.read_csv('expectation_threshold.csv')
    
    # check if each skill matches the startegy laid down by
    # the recruiter/reviewer.
    profile_output.keys()
    dataf = profile_output['domain_frequency']
    domain_dict = profile_output['Domain_Keywords']
    
    # strip the spaces from both domain_dictionary and dataf
    for i in list(domain_dict.keys()):
        domain_dict[i] = [domain_dict[i][j].strip() for j in range(len(domain_dict[i]))]
    
    dataf['Keyword'] = [dataf['Keyword'].values.tolist()[i].strip() for i in range(len(dataf['Keyword']))]
    
    # Instantiate a dictonary to compute the score for key_skill
    keyskill_score_dict = {}
    for domain in list(set(dataf['Domain'])):
        for skill in domain_dict[domain]:
            try:
                if skill in exp_threshold_df['key_skill'][exp_threshold_df['Domain'] == domain].values.tolist()[0]:
                    keyskill_score_dict[domain] = len(domain_dict[domain])
                else:
                    keyskill_score_dict[domain] = 0
            except IndexError:
                keyskill_score_dict[domain] = 0
            
    # Group By operation

    profile_df2 = dataf['Keyword'].groupby([dataf['Candidate Name'], dataf['Domain']]).count().unstack()
    profile_df2.reset_index(inplace = True)

        
            
    # Instantiate a dictionary to compute the domain_threshold_score
    domain_threshold_score = {}
    for domain in list(set(dataf['Domain'])):
        count = profile_df2[domain].values.tolist()[0]
        try:
            if count >= exp_threshold_df['exp_threshold'][exp_threshold_df['Domain'] == domain].values.tolist()[0]:
                domain_threshold_score[domain] = profile_df2[domain].values.tolist()[0]
            else:
                domain_threshold_score[domain] = 0
        except IndexError:
            domain_threshold_score[domain] = 0
    
    keyskill_score_dict
    domain_threshold_score
    
    # compute the total score
    total_score = {}
    for domain in list(keyskill_score_dict.keys()):
        total_score[domain] = 0.6 *keyskill_score_dict[domain]  + 0.4 * domain_threshold_score[domain]
    
    return total_score
    
if __name__ == '__main.py__':
    pdfextract()
    create_profile()
    requirement_match()
    
    
    