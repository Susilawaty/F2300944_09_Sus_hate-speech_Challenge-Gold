""" 
Function untuk membersihkan data text
"""
import re
import pandas as pd

def text_cleansing(text):
    # Bersihkan tanda baca (selain huruf dan angka)
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # yg lain
    clean_text = clean_text.lower()
    # Bersihkan dengan kamus alay
    
    # Bersihkan dengan kamus abusive
    return clean_text

def cleansing_files(file_upload):
    # Read csv file upload, jika error dengan metode biasa, gunakan encoding latin-1
    try:
        df_upload = pd.read_csv(file_upload)
    except:
        df_upload = pd.read_csv(file_upload, encoding="latin-1")
    print("Read dataframe from Upload success!")
    # Ambil hanya kolom pertama saja 
    df_upload = pd.DataFrame(df_upload.iloc[:,0])
    # Rename kolom menjadi "raw_text"
    df_upload.columns = ["raw_text"]
    # Bersihkan text menggunakan fungsi text_cleansing
    # Simpan di kolom "clean_text"
    df_upload["clean_text"] = df_upload["raw_text"].apply(text_cleansing)
    print("Cleansing text success!")
    return df_upload