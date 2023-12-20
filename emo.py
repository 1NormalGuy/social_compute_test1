import csv
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import dic

def plot_sentiments(good, mid, bad,filmid):
    sentiments = ['Good', 'Mid', 'Bad']
    total = len(good) + len(mid) + len(bad)
    ratios = [len(good)/total, len(mid)/total, len(bad)/total]

    plt.bar(sentiments, ratios, color=['green', 'yellow', 'red'])
    plt.xlabel('Sentiment')
    plt.ylabel('Ratio')
    plt.title(f'{filmid}--Sentiment Analysis of Comments')
    plt.show()

    
def classify_comments(filename):
    good_comments = []
    mid_comments = []
    bad_comments = []

    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            comment = row[0]
            sentiment = SnowNLP(comment).sentiments
            if sentiment > 0.6:
                good_comments.append(comment)
            elif sentiment > 0.4:
                mid_comments.append(comment)
            else:
                bad_comments.append(comment)

    return good_comments, mid_comments, bad_comments

if __name__ == '__main__':
    for key, value in dic.film_id_name.items():
        good_comments, mid_comments, bad_comments = classify_comments(f'./information/{value}_comments.csv')
        print(f"文件名：{key}")
        print(f"好评数量：{len(good_comments)}")
        print(f"中评数量：{len(mid_comments)}")
        print(f"差评数量：{len(bad_comments)}")
        plot_sentiments(good_comments, mid_comments, bad_comments, f'{key}')