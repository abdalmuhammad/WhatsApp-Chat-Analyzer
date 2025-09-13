from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()

def create_wordcloud(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['User'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['Message'].str.cat(sep=" "))
    return df_wc

def fetch_stats(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['User'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['Message']:
        words.extend(message.split())
    num_words = len(words)

    # fetch number of media messages
    num_media_messages = df[df['Message'].str.contains("Media omitted", case=False, na=False)].shape[0]

    # fetch number of links
    Links = []
    for message in df['Message']:
        Links.extend(extractor.find_urls(message))
    num_links = len(Links)

    return num_messages, num_words, num_media_messages, num_links

def most_busy_users(df):
    x = df['User'].value_counts().head()
    df = round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'User': 'percent'})
    return x, df

def most_common_words(selected_user, df):

    if selected_user != 'All Users':
        df = df[df['User'] == selected_user]
    
    temp = df[df['User'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>']

    stop_words = {"i", "me", "my", "myself", "2", "?", "ours", "bhi", "you", "se", "koi", "b", "ab", "du", "de", "ne", "hu", "ker", "3", "123", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                  "he", "him", "his", "himself", "she", "ki", "hers", "herself", "it", "its", "itself", "they", "mai", "their", "wo", "ap", "sb", "ye", "kay", "bhej", "bht", "k", "hi","kr", "hn", "han", ",", "/", "@", "(", ")", "<", ">", "?", "aur", "toh", "thi", "the", "aap", "tum", "tumhe", "tumhara", "tumhari", "tumse", "hum", "humne", "humara", "humari", "humse", ".", "!", ":", ";", "'", "\"", "[", "]", "{", "}", "|", "\\", "#", "$", "%", "^", "&", "*", "-", "_", "+", "=", "~", "`", "😂", "hain",
                  "ny", "hen", "he.", "tah", "this", "that", "nahi", "dena", "nahin", "na", "bhai", "is", "are", "was", "were", "be", "been", "tu", "haha", "hehe", "ok", "bata", "kab", "kia", "kya", "ksi", "ny", "m", "n", "sy", "sir", "karna", "krna", "karn", "karta", "karti", "krta", "krti", "hota", "hoti", "hona", "hone", "honge", "ho", "raha", "rahi", "rahe", "rha", "rhi", "rhe", "gya", "gayi", "gye", "gya.", "gayi.", "gye.", "ja", "jaa", "jao", "jaana", "jaane", "jaoge", "jaungi", "jaunga", "chahiye", "chahie", "chahiyen", "chahiyega", "chahiyegi","kiya","kuch","kuchh","kuchhh","kuchhhh","kuchhhhh","kuchhhhhh","kuchhhhhhh","kuchhhhhhhh","kuchhhhhhhhh","kuchhhhhhhhhh","kuchhhhhhhhhhh","kuchhhhhhhhhhhh","kuchhhhhhhhhhhhh","nhi","nahi.","nahi..","nahi...","nahi....","nahi.....","nahi......","nahi.......","nahi........","nahi.........","nahi..........","nahi...........","nahi............","nahi.............","nahi..............","hain.","hain..","hain...","hain....","hain.....","hain......","hain.......","hain........","hain.........","hain..........","hain...........","hain............","hain.............",
                  "so", "nh", "ka", "ky", "s", "h", "hy","to", "hai", "ko", "par", "lekin", "or", "aur", "for", "on", "in", "at", "of", "the", "and", "a", "an", "sa", "sab", "sabhi", "hai.", "hahaha", "hahahaha", "warna", "ha", "chal", "kar", "kal", "yr"}

    words = []
    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['User'] == selected_user]

    emojis = []
    for message in df['Message']:
        emojis.extend([emo['emoji'] for emo in emoji.emoji_list(message)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year', 'Month']).size().reset_index(name='Message')
    time = []
    for i in range(timeline.shape[0]):
        time.append(f"{timeline['Month'][i]}-{timeline['Year'][i]}")

    timeline['Time'] = time
    
    return timeline

def week_activity_map(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['User'] == selected_user]

    return df['Day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['User'] == selected_user]

    return df['Month'].value_counts()
