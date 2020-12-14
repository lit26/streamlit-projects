import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title("Streamlit Yfinance")
input_tickers = st.sidebar.text_input(label='Tickers')
period = st.sidebar.selectbox('Period',['1d','5d','1mo','3mo','6mo',
                                        '1y','2y','5y','10y','ytd','max'],index=5)
interval = st.sidebar.selectbox('Interval',['1m','2m','5m','15m','30m',
                                            '60m','90m','1h','1d','5d',
                                            '1wk','1mo','3mo'],index=8)
prepost = st.sidebar.checkbox('Prepost',value=True)

if input_tickers != '':
    tickers = input_tickers.split()
    data = yf.download(
        tickers=input_tickers,
        period=period,
        interval=interval,
        group_by='ticker',
        auto_adjust=True,
        prepost=prepost,
        threads=True,
    )
    if len(data) == 0:
        st.error('Failed download.')
    else:
        ticker = st.selectbox('Select', tickers)
        if len(tickers) > 1:
            df = data[ticker]
        else:
            df = data
        st.dataframe(df)
        click = st.button('Export csv')
        if click:
            df.to_csv('{}.csv'.format(ticker))
        margin = go.layout.Margin(
            b=50,t=50,l=0,r=0
        )
        layout = go.Layout(
            margin=margin
        )
        data = [go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name="Candlestick",
            showlegend=False
        )]
        fig = go.Figure(
            data=data,
            layout=layout
        )
        st.plotly_chart(fig)
