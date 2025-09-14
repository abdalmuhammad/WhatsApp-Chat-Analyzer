import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer")
uploader_file = st.sidebar.file_uploader("Upload WhatsApp Chat File")
if uploader_file is not None:
    bytes_data = uploader_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['User'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "All Users")
    selected_users = st.sidebar.selectbox("Select User", user_list)

    if st.sidebar.button("Show Analysis"):str

        # helper.fetch_stats returns: (num_messages, num_words, num_media_messages)
        num_messages, num_words, num_media_messages, num_links = helper.fetch_stats(selected_users, df)
        
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
        
    timeline = helper.monthly_timeline(selected_users, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['Time'], timeline['Message'], color='green')
    plt.xticks(rotation='vertical')
    st.title("Monthly Timeline")
    st.pyplot(fig)

    st.title("Activity Map")
    col1, col2 = st.columns(2)
    with col1:
        st.header("Most Busy Day")
        busy_day = helper.week_activity_map(selected_users, df)
        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values)
        st.pyplot(fig)
    
    with col2:
        st.header("Most Busy Month")
        busy_month = helper.month_activity_map(selected_users, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values, color='orange')
        st.pyplot(fig)
    
    if selected_users == 'All Users':
        st.title("Most Busy Users")
        x,new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)
        
    st.title("WordCloud")
    df_wc = helper.create_wordcloud(selected_users, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    st.title("Most Common Words")
    most_common_df = helper.most_common_words(selected_users, df)

    fig,ax = plt.subplots()
    ax.barh(most_common_df[0], most_common_df[1])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    emoji_df = helper.emoji_helper(selected_users, df)
    st.title("Emoji Analysis")
    st.dataframe(emoji_df)

    st.title("Activity Heatmap")
    user_heatmap = helper.activity_heatmap(selected_users, df)
    fig, ax = plt.subplots()
    ax = plt.imshow(user_heatmap, cmap='YlGnBu')
    plt.yticks(rotation='vertical')
    st.pyplot(fig)