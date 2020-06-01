''' Ian Nduhiu
    Talent Snapshot: Keyword Extraction
    5/28/2020
'''

from text_rank import TextRank4Keyword
import pandas as pd

def main():
    ''' Main function '''
    # read in talent snapshot data
    talent_data = pd.read_excel("Talent Snapshot.xlsx")

    # get the columns
    talent_columns = talent_data.columns

    # extract and preprocess education data
    education, non_education = education_extract(talent_data[talent_columns[1]].values)

    # combine non_education and main skills and talents column
    main_skills = talent_data[talent_columns[2]] + '. ' + pd.Series(non_education)

    # apply extractfunc to the columns: "main talents and skills", "expertise" 
    # and "main achievements"
    all_keywords = main_skills.apply(extractfunc) + ' ' \
                   + talent_data[talent_columns[3]].apply(extractfunc) + ' '\
                   + talent_data[talent_columns[11]].apply(extractfunc)
    
    # write to excel file
    pd.DataFrame({'education':education, 
                 'talent_keywords':all_keywords}).to_excel('Keywords.xlsx')  

def education_extract(education):
    ''' Preprocesses education column and simplifies content to either
        bachelors, masters, doctor or non-educataion related. The 
        non-education words are mixed together with the main talents
        and skills columns for later keyword extraction as they may
        contain useful keywords for the snapshot analysis'''
    # Extract abbreviations
    degrees_abbrevs = pd.read_excel("Degrees Abbreviations.xlsx")
    bachelors = degrees_abbrevs["Bachelors"].values
    masters = degrees_abbrevs["Masters"].values
    doctors = degrees_abbrevs["Doctors"].values

    # two empty arrays, one to hold school keywords and the other
    # for keywords not related to school
    education_related = []
    non_education_related = []
    
    for text in education:
        # put text into easier format to work with
        text = str(text).lower()
        text = text.replace(",","")
        text = text.split()

        # Check for words related to doctor
        if "doctor" in text or "doctorate" in text:
            education_related.append("Doctor")
            non_education_related.append("")
            continue
        else:
            word_found = False
            for words in doctors:
                for word in str(words).split():
                    if word.lower() in text:
                        word_found = True
                        education_related.append("Doctor")
                        non_education_related.append("")
                        break
                if word_found:
                    break
            if word_found:
                continue

        # Check for words related to Masters
        if "master" in text:
            education_related.append("Masters")
            non_education_related.append("")
            continue
        else:
            word_found = False
            for words in masters:
                for word in str(words).split():
                    if word.lower() in text:
                        word_found = True
                        education_related.append("Masters")
                        non_education_related.append("")
                        break
                if word_found:
                    break
            if word_found:
                continue
        
        # Check for anything to do with bachelors
        if "bachelor" in text:
             education_related.append("Bachelors")
             non_education_related.append("")
             continue
        else:
            word_found = False
            for words in bachelors:
                for word in str(words).split():
                    if word.lower() in text:
                        word_found = True
                        education_related.append("Bachelors")
                        non_education_related.append("")
                        break
                if word_found:
                    break
            if word_found:
                continue
        word_found = False
        for word in ['college', 'university', 'institute', 
                     'school', 'uc', 'poly', 'uchicago',
                     'ucla']:
            if word in text:
                word_found = True
                education_related.append("Bachelors")
                non_education_related.append("")
                break
        if word_found:
            continue

        # At this point, the word is probably not related to education
        education_related.append("")
        non_education_related.append(' '.join(text))

    return (education_related, non_education_related)

def extractfunc(text):
    ''' Wrapper function that initializes a TextRank4Keyword 
        object and uses it to extract the keywords from 
        a piece of text '''
    text = str(text)  # make sure text is str type
    tr4w = TextRank4Keyword()
    tr4w.analyze(text, window_size=4, lower=False)
    return ' '.join(tr4w.get_keywords())
    
if __name__ == "__main__":
    main()