import string
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from emo_unicode import EMOTICONS
from unicode_emo import UNICODE_EMO
from chat_words import chat_words_str
from spellchecker import SpellChecker
spell = SpellChecker()
stemer = PorterStemmer()
lemma = WordNetLemmatizer()

def text_preprocessing(data, lower_case = True, \
    punc = True, stopwards = True, stem = True, lemmat = True,\
    rm_emoj = True, rm_emticon = True,\
    cn_emticon = False, cn_emoj = False,\
    urls = True, htmltags = True, chat_con = True, spell_chec = True):
    
    # Change to Lowercase
    if(lower_case):
        data = data.lower()
    
    # Chat Words Conversion
    if(chat_con):
        chat_words_map_dict = {}
        chat_words_list = []
        for line in chat_words_str.split("\n"):
            if line != "":
                cw = line.split("=")[0]
                cw_expanded = line.split("=")[1]
                chat_words_list.append(cw)
                chat_words_map_dict[cw] = cw_expanded
        chat_words_list = set(chat_words_list)

        new_text = []
        for w in data.split():
            if w.upper() in chat_words_list:
                new_text.append(chat_words_map_dict[w.upper()])
            else:
                new_text.append(w)

        data = " ".join(new_text)

    # Remove Emojis
    if(rm_emoj):
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)

        data =  emoji_pattern.sub(r'', data)
    
    # Remove Emoticons
    if(rm_emticon):
        emoticon_pattern = re.compile(u'(' + u'|'.join(k for k in EMOTICONS) + u')')
        data =  emoticon_pattern.sub(r'', data)
    
    # Convert Emoji to Words
    if(cn_emoj):
        for emot in UNICODE_EMO:
            data = re.sub(r'('+emot+')', "_".join(UNICODE_EMO[emot].replace(",","").replace(":","").split()), data)
    
    # Convert Emoticons to Words
    if(cn_emticon):
        for emot in EMOTICONS:
            data = re.sub(u'('+emot+')', "_".join(EMOTICONS[emot].replace(",","").split()), data)
    
    # Remove URLs
    if(urls):
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        data = url_pattern.sub(r'', data)

    # Remove HTML Tags
    if(htmltags):
        html_pattern = re.compile('<.*?>')
        data = html_pattern.sub(r'', data)

    # Spelling Checker
    if(spell_chec):
        corrected_text = []
        misspelled_words = spell.unknown(data.split())
        for word in data.split():
            if word in misspelled_words:
                corrected_text.append(spell.correction(word))
            else:
                corrected_text.append(word)
        data = " ".join(corrected_text)

    # Remove Punctuation
    if(punc): 
        data = data.translate(str.maketrans('', '', string.punctuation))

    # Remove Stopwards
    if(stopwards):
        data = ' '.join([word for word in word_tokenize(data) if not word in list(stopwords.words('english'))])
    
    # Stemming
    if(stem):
        data = " ".join([stemer.stem(word) for word in word_tokenize(data)])
    
    # Lemmatization
    if(lemmat):
        data = ' '.join([lemma.lemmatize(word) for word in word_tokenize(data)])
    
    
    return data

data = """Cake is a form of sweet food made from flour, sugar, and other ingredients, that is usually baked.
In their oldest forms, cakes were modifications of bread, but caakes now cover a wide range of preparations 
that can be simple or elaborate, and that share features with other desserts such as pastries, meringues, custards, 
and pies BRB :-) 🔥"""

data_ = text_preprocessing(data)
print(data_)
# cake form sweet food made flour sugar ingredi usual bake oldest form cake modif bread cake cover wide rang prepar simpl elabor share featur dessert pastri meringu custard pie be right back happyfacesmiley fire
