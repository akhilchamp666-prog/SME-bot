import pandas as pd
import re

def load_updates(file_path):
    df = pd.read_excel(file_path, engine="openpyxl")
    df.columns = df.columns.str.strip().str.replace('\xa0','')
    df['Update_ID_str'] = df['Update_ID'].astype(str).str.lower()
    df['Description_str'] = df['Description'].astype(str).str.lower()
    df['Status'] = df['Status'].fillna("Active")
    return df

def search_updates(df, user_input):
    STOPWORDS = {'what','is','the','on','please','give','me','update','of','for',
                 'can','be','with','a','how','i','you','we','are','my','do','billed','updates'}
    GREETINGS = {'hi','hello','hey','goodmorning','goodafternoon'}

    user_input_clean = re.sub(r'[^\w\s]', '', user_input.lower())
    user_words = [w for w in user_input_clean.split() if w not in STOPWORDS]

    if any(word in GREETINGS for word in user_words):
        return "greeting"

    numbers = re.findall(r'\d+', user_input_clean)
    result_rows = []

    for _, row in df.iterrows():
        row_id = str(row['Update_ID']).lower()
        desc_words = row['Description_str'].split()

        if numbers:
            if any(num == row_id for num in numbers):
                if len(user_words) > 0:
                    keywords = [w for w in user_words if not w.isdigit()]
                    if all(kw in desc_words for kw in keywords):
                        result_rows.append(row)
                else:
                    result_rows.append(row)
        else:
            if all(kw in desc_words for kw in user_words):
                result_rows.append(row)

    return result_rows

