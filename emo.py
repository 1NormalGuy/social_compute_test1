import csv
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import dic
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
from tqdm import tqdm
import matplotlib
import json
import os

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号

def classify_comments(filename):
    sentiments = {'好评': 0, '中评': 0, '差评': 0}

    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            comment = row[0]
            sentiment = SnowNLP(comment).sentiments
            if sentiment > 0.6:
                sentiments['好评'] += 1
            elif sentiment > 0.4:
                sentiments['中评'] += 1
            else:
                sentiments['差评'] += 1

    return sentiments


def save_sentiments(sentiments, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(sentiments, f, ensure_ascii=False)

def load_sentiments(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def plot_sentiments(filename):
    all_sentiments = load_sentiments(filename)

    sentiments = list(all_sentiments.keys())
    good_ratios = [value['好评'] for value in all_sentiments.values()]
    mid_ratios = [value['中评'] for value in all_sentiments.values()]
    bad_ratios = [value['差评'] for value in all_sentiments.values()]

    r = np.arange(len(good_ratios))

    plt.bar(r, good_ratios, color='green', edgecolor='grey', label='Good')
    plt.bar(r, mid_ratios, bottom=good_ratios, color='yellow', edgecolor='grey', label='Neutral')
    plt.bar(r, bad_ratios, bottom=np.array(good_ratios)+np.array(mid_ratios), color='red', edgecolor='grey', label='Bad')

    plt.xlabel('Movie', fontweight='bold')
    plt.xticks(r, sentiments, rotation=90)  # Add rotation parameter to avoid label overlap
    plt.ylabel('Ratio')
    plt.title('Sentiment Analysis of All Movies')

    plt.legend()
    plt.show()

if __name__ == '__main__':
    start_time = time.time()
    # all_sentiments = {}
    # for key, key in tqdm(dic.film_id_name.items()):
    #     sentiments = classify_comments(f'./information/{key}_comments.csv')
    #     total = sum(sentiments.keys())
    #     ratios = {k: v/total for k, v in sentiments.items()}
    #     all_sentiments[dic.film_id_name[key]] = ratios

    # save_sentiments(all_sentiments, './sentiments/all_sentiments.json')

    plot_sentiments('./sentiments/all_sentiments.json')
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")