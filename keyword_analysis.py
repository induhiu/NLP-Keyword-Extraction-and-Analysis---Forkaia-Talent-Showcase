''' Ian Nduhiu
    Talent Snapshot: Keyword Analysis
    5/28/2020
'''

import spacy
import pandas as pd

nlp = spacy.load("en_core_web_lg")  # use the large model!

def main():
    ''' '''
    # create dictionary that will hold counts
    snapshot_dict = {"Data Scientists/Analysts":0,
                     "Computer Scientists":0,
                     "Software Devs/Engineers":0,
                     "Web Developers":0,
                     "Marketers - Social media, Ads etc.":0,
                     "Web/Graphic Designers":0,
                     "Project Managers":0,
                     "Bachelors Degrees":0,
                     "Masters Degrees":0,
                     "PhDs and Doctorates":0,
                     "Hackathon Champions":0,
                     "Coding competition winners":0,
                     "Special Awards/Recognition/Honors":0}

    # read in extracted keywords
    keywords_extracted = pd.read_excel("Keywords.xlsx")
    keywords = keywords_extracted["talent_keywords"].values
    education = keywords_extracted["education"].values

    # call analysis by roles function
    roles_analyse(keywords, snapshot_dict)

    # call analysis by achievements function
    achievements_analyse(keywords, snapshot_dict)

    # call analysis by education function
    education_analyse(education, snapshot_dict)

    # create a series object containing snapshot created so far
    # and write to excel file
    snapshot = pd.Series(snapshot_dict)
    snapshot.to_excel("Snapshot Figures and Analysis.xlsx")

def roles_analyse(keywords, snapshot_dict):
    ''' Uses spacy library to create a list of 10 most similar words
        to roles being searched for in the keywords that would be used 
        in comparison with extracted keywords '''
    # use spacy via the most_similar function to 
    # create a vocab of about 10 most similar words for each keyword 
    scientist = [w.lower_ for w in most_similar(nlp.vocab["scientist"])]
    analytics = [w.lower_ for w in most_similar(nlp.vocab["analytics"])]
    development = [w.lower_ for w in most_similar(nlp.vocab["devs"]) 
                   if w.lower_ not in ("programmers", "coders")]
    graphic = [w.lower_ for w in most_similar(nlp.vocab["graphic"])] 
    design = [w.lower_ for w in most_similar(nlp.vocab["designer"])]
    marketing = [w.lower_ for w in most_similar(nlp.vocab["marketer"])]
    engineer = ["engineer", "engineers", "engineering"] 
    management = [w.lower_ for w in most_similar(nlp.vocab["management"]) 
                  if w.lower_ != "development"]

    # for each word in keywords group, check relation to selected roles above
    # and if similar, count as part of group
    for words in keywords:
        words_lst = words.split()
        
        # for checking graphic later
        graphic_found = False
        for word in graphic:
            if word in words_lst:
                graphic_found = True
                break

        for word in words_lst:
            if (word.lower() in scientist and "data" in words_lst) or\
                word.lower() in analytics:
                snapshot_dict["Data Scientists/Analysts"] += 1
            
            if word.lower() in scientist and "computer" in words_lst:
                snapshot_dict["Computer Scientists"] += 1
            
            if (word.lower() in development or word.lower() in engineer) \
                and "software" in words_lst:
                snapshot_dict["Software Devs/Engineers"] += 1
            
            if word.lower() in development and "web" in words_lst:
                snapshot_dict["Web Developers"] += 1
            
            if word.lower() in marketing:
                snapshot_dict["Marketers - Social media, Ads etc."] += 1
            
            if word.lower() in design and \
                (graphic_found or "web" in words_lst):
                snapshot_dict["Web/Graphic Designers"] += 1

            if word.lower() in management and "proect" in words_lst:
                snapshot_dict["Project Managers"] += 1

def most_similar(word):
    ''' Returns a sorted list of 10 most similar words to the word '''
    queries = [w for w in word.vocab if 
            w.is_lower == word.is_lower and w.prob >= -15]
    by_similarity = sorted(queries, key=lambda w: word.similarity(w), 
                           reverse=True)
    return by_similarity[:10]

def achievements_analyse(keywords, snapshot_dict):
    ''' Uses spacy library to create a list of 10 most similar words
        to achievements being searched for in the keywords that would be used 
        in comparison with extracted keywords. '''
    # create unique list of most similar words for words that will be vital
    # in search of achievements using the spacy library
    champion_vocab = set([w.lower_ for w in most_similar(nlp.vocab["winner"])] +\
        [w.lower_ for w in most_similar(nlp.vocab["champion"])])
    award_vocab = set([w.lower_ for w in most_similar(nlp.vocab["award"])] +\
         [w.lower_ for w in most_similar(nlp.vocab["winner"])] +\
         [w.lower_ for w in most_similar(nlp.vocab["recognition"])])
    coding = [w.lower_ for w in most_similar(nlp.vocab["coding"])]
    competition = ["competition", "competitions", "contest", "contests"]    

    # for each word in keywords group, check relation to achievement 
    # words above and, if similar, count as part of group 
    for words in keywords:
        words_lst = words.split()
    
        # for checking hackathon later
        hack = False
        if "hackathon" in words_lst:
            hack = True

        for word in words_lst:
            if word in champion_vocab and hack:
                snapshot_dict["Hackathon Champions"] += 1

            if word in award_vocab:
                snapshot_dict["Special Awards/Recognition/Honors"] += 1

                # checking if they are a winner of a coding competition
                code, compete = False, False
                for word in coding:
                    if word in words_lst:
                        code = True
                        break
                for word in competition:
                    if word in words_lst:
                        compete = True
                        break
                if code and compete:
                    snapshot_dict["Coding competition winners"] += 1
        
def education_analyse(education, snapshot_dict):
    ''' Checks each word in the education array and increases count in 
        appropriate education group'''
    for word in education:
        if word == "Doctor":
            snapshot_dict["PhDs and Doctorates"] += 1
        elif word == "Masters":
            snapshot_dict["Masters Degrees"] += 1
        elif word == "Bachelors":
            snapshot_dict["Bachelors Degrees"] += 1


if __name__ == "__main__":
    main()