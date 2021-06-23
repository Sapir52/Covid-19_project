from flask import Flask, render_template, request, url_for, Markup, jsonify
import pickle
from nltk.stem.porter import PorterStemmer
import re
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def data_clearing(text):
    print(type(text))
    # Lowering letters
    text = text.lower()
    # Removing html tags
    text = re.sub(r'<[^>]*>', '', text)
    # Removing twitter usernames
    text = re.sub(r'@[A-Za-z0-9]+', '', text)
    # Removing urls
    text = re.sub('https?://[A-Za-z0-9]', '', text)
    # Removing numbers
    text = re.sub('[^a-zA-Z]', ' ', text)
    # distribution of tokens
    word_tokens = word_tokenize(text)
    # remove stopwords
    filtered_sentence = [word_token for word_token in word_tokens if word_token not in stop_words]
    # Joining words
    text = (' '.join(filtered_sentence))
    return text

def tokenizer_porter(text):
    # Returns a list of tokens for the inserted input post
    porter = PorterStemmer()
    return [porter.stem(word) for word in text.split()]

app = Flask(__name__)
# Import pickle files that allow data to be predicted
pickle_in = open('model_fakenews.pickle','rb')
pac = pickle.load(pickle_in)
tfid = open('tfidf.pickle','rb')
tfidf_vectorizer = pickle.load(tfid)

@app.route('/')
def home():
 	return render_template("index.html")

@app.route('/newscheck')
def newscheck():
    #  A function that receives one post and allows you to predict whether it is true or false.
	temp = request.args.get('news')
	input_data = [temp.rstrip()]
	# transforming input- tfidf vector
	tfidf_test = tfidf_vectorizer.transform(input_data)
	# predicting the input
	y_pred = pac.predict(tfidf_test)
	print(y_pred[0])
	return jsonify(result = y_pred[0])

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    #A function that allows you to import file contents
    if request.method == 'POST':
        df_all_tw = pd.read_csv(request.files.get('file'))
        # Call show_tables function
        df_all_tw=show_tables(df_all_tw)
        # render a template
        return render_template('upload.html', tables=[df_all_tw.to_html(classes='tweets_covid19')],
                               titles=['na', 'Predict SVC'])
    return render_template('upload.html')


def show_tables(df_all_tw):
    '''
    A function that allows you to make predictions for the data of the post file and
    adds a column with the prediction results
    '''
    temp_predict=[]
    # Change the type of data in the inserted file
    df_all_tw_clearing=df_all_tw.astype(str)
    # Perform data clearing in the file
    for col_name in df_all_tw_clearing.columns:
       df_all_tw_clearing[col_name] = df_all_tw_clearing[col_name].apply(data_clearing)
    for abc in df_all_tw_clearing.values.tolist():
        input_data = [', '.join(abc).rstrip()]
        # transforming input tfidf vector
        tfidf_test = tfidf_vectorizer.transform(input_data)
        # predicting the input
        y_pred = pac.predict(tfidf_test)
        #print(y_pred[0])
        temp_predict.append(y_pred[0])
    df_all_tw['predict']=temp_predict
    return df_all_tw


if __name__=='__main__':
	app.run(debug=True)
