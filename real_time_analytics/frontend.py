import streamlit as st
import redis
import time
import pandas as pd
import altair as alt

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Reset all relevant data
r.delete("total_messages", "user_message_counts")
for key in r.scan_iter("active_user:*"):
    r.delete(key)

st.set_page_config(page_title="Live Chat Analytics", layout="wide")
st.title("📊 Live Chat Analytics Dashboard")

def get_stats():
    total_messages = int(r.get("total_messages") or 0)
    top_users = r.zrevrange("user_message_counts", 0, 9, withscores=True)
    active_users = r.keys("active_user:*")
    return total_messages, [(u.decode(), int(s)) for u, s in top_users], len(active_users)

# Live update loop
placeholder = st.empty()

while True:
    with placeholder.container():
        total_messages, top_users, active_count = get_stats()

        col1, col2 = st.columns(2)
        col1.metric("📨 Total Messages", total_messages)
        col2.metric("🟢 Active Users (last 1 min)", active_count)

        if top_users:
            df = pd.DataFrame(top_users, columns=["User", "Messages"])

            # Sort descending for top -> bottom in bar chart
            df = df.sort_values("Messages", ascending=True)

            st.subheader("🏆 Top 10 Users by Message Count")

            chart = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    x=alt.X("Messages:Q", title="Messages Sent"),
                    y=alt.Y("User:N", sort="-x", title="User"),
                    tooltip=["User", "Messages"]
                )
                .properties(height=400)
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No messages yet!")

    time.sleep(1)
