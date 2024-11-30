from flask import Flask, render_template,request
import csv
import pandas as pd

app = Flask(__name__, template_folder='./templates')
   
def paginate(data, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]



@app.route('/')
def index():
    csv_file = 'C:\\Users\\Enes\\Desktop\\TwitterScrape\\results\\CreateLabellingResult.csv'
    df = pd.read_csv(csv_file)
    
    data_tweets = df[df['address'].isnull()][['tweet_date', 'username', 'content_no_rare_words', 'content', 'final_label']].to_dict(orient='records')
    data_heatmap = df[df['latitude_city'].notnull()][['tweet_date', 'username', 'content', 'content_no_rare_words','city','final_label']].to_dict(orient='records')
    data_address = df[df['address'].notnull()][['tweet_date', 'username','content','content_no_rare_words','address', 'final_label']].to_dict(orient='records')

    return render_template(
        'index.html', 
        data_tweets=data_tweets, 
        data_heatmap=data_heatmap, 
        data_address=data_address
    )

if __name__ == '__main__':
    app.run(debug=True)
