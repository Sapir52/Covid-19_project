import pandas as pd
from sklearn.model_selection import train_test_split
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from sklearn.svm import SVC

df_data_covid_19 = pd.read_csv('data/preprocessing.csv')

def merge_3_columns(df):
    df['title_text_source'] = df['title'] + ' ' + df['text'] + ' ' + df['source']
    return df.dropna()

df_data_covid_19 = merge_3_columns(df_data_covid_19)



"""## TF-IDF"""


def tokenizer_porter(text):
    porter = PorterStemmer()
    return [porter.stem(word) for word in text.split()]


def tf_idf_vectors(df):
    tfidf = TfidfVectorizer(strip_accents=None,
                            lowercase=False,
                            preprocessor=None,
                            tokenizer=tokenizer_porter,
                            use_idf=True,
                            norm='l2',
                            smooth_idf=True)

    X = tfidf.fit_transform(df['title_text_source'])
    y = df_data_covid_19.label.values
    return X, y, tfidf


X, y, tfidf = tf_idf_vectors(df_data_covid_19)

"""## Save/ Show model"""


def save_model(clf_, filename):
    model = open('data/' + filename + '.sav', 'wb')
    pickle.dump(clf_, model)
    model.close()

"""## SVC"""

def svc(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=0.2, random_state=11)
    classifier = SVC(kernel='linear', random_state=0)
    classifier.fit(X_train, y_train)
    print('accuracy on train data: ', classifier.score(X_train, y_train))
    print('accuracy on test data: ', classifier.score(X_test, y_test))

    # saving model
    with open('model_fakenews.pickle', 'wb') as f:
        pickle.dump(classifier, f)

    # save model
    save_model(classifier,'SVC')
    return X_test, y_test, classifier

X_test, y_test,classifier=svc(X,y)

# saving vectorizer
with open('tfidf.pickle', 'wb') as f:
    pickle.dump(tfidf, f)
