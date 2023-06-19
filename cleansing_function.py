""" 
Function untuk membersihkan data text
"""
import re
import pandas as pd
from db import get_abusive_data, create_connection

def text_cleansing(text):
    # Bersihkan tanda baca (selain huruf dan angka)
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text) #remove tanda baca
    clean_text = re.sub(r'#\w+', '', text) # remove hastag
    clean_text = re.sub(r'@\w+', '', text) # removing user mention
    clean_text = re.sub(r'(http[s]?:\\/\\/\s\S+)',' ',text)
    clean_text = re.sub('url', '', text) # remove url
    clean_text = re.sub(r'[^\w\s]', '', text) # remove punct
    clean_text = re.sub(u'[\U0001F600-\U0001F650]|[\U0001F300-\U0001F5FF]', '', text) #remove emotion
    clean_text = re.sub(u'[\U0001F680-\U0001F6FF]|[\U0001F700-\U0001F77F]', '', text) #remove symbol
    clean_text = re.sub(r'[^\x00-\x7F]+',' ', text) # remove non ASCI
    clean_text = re.sub(r"(\(:*\))|(\[:*\])", "",text) #Remove text in bracket
    clean_text = re.sub(r"\\n", "",text) # removing extra line
    clean_text = re.sub(' +',' ',text) # remove extra space
    clean_text = re.sub('\d{8,}', 'XXX', text) # masking phone number
    clean_text = re.sub('[ð]', '', text) #remove unwanted char
    clean_text = re.sub("&amp"," ", text) # remove amp
    clean_text = re.sub("\\\\x[a-z0-9_]+", " ", text) #remove char start with x
    clean_text = re.sub('[()!?]', ' ', text)
    clean_text = re.sub('rt user',' ', text) #remove kata user
    clean_text = re.sub(r'[^0-9a-zA-Z\?!,.]+',' ',text) # remove non alpha num
    clean_text = re.sub('"','',text) # remove non alpha num
    clean_text = re.sub('\s\s+',' ',text) # remove non alpha num
    clean_text = re.sub(r'[!]{2,}','!',text) # remove non alpha num
    clean_text = re.sub(r'[\?]{2,}','?',text) # remove non alpha num
    clean_text = re.sub(';',' ',text) #remove every';'
    # yg lain
    clean_text = clean_text.lower()
    clean_text = clean_text.strip()
    # Bersihkan dengan kamus alay
    alay_words = pd.read_csv('csv_data/alay.csv', delimiter='\t')
    alay_clean = dict(zip(alay_words['alay'], alay_words['baku']))
    kamus = clean_text.split()
    alay_words = [alay_clean.get(word, word) for word in kamus]
    clean_text = ' '.join(alay_words)
    # Bersihkan dengan kamus abusive
    conn = create_connection()
    df_abusive = get_abusive_data(conn)
    abusive_words = df_abusive['word'].tolist()
    for word in abusive_words:
        clean_text = clean_text.replace(word, '*****')
    return clean_text

def cleansing_files(file_upload):
    # Read csv file upload, if there's an error with the default method, use encoding 'latin-1'
    df_upload = pd.DataFrame(file_upload.iloc[:,0])
    # Rename the column to "raw_text"
    df_upload.columns = ["raw_text"]
    # Cleanse the text using the text_cleansing function
    # Store the results in the "clean_text" column
    df_upload["clean_text"] = df_upload["raw_text"].apply(text_cleansing)
    print("Cleansing text success!")
    return df_upload