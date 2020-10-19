# House Price Fluctuations in Seoul, South Korea
[[Seongyong Kim](http://syoi92.github.io)], [[Rightstone](https://)]


This project demonstrates the house price fluctuations in units of 25 administrative districts in Seoul, South Korea into an interactive [Streamlit](https://streamlit.io) app. The unit is KRW/3.3m^2 (3.3m^2 = 1 pyeong, Korean unit of land).


![Making-of Animation](https://raw.githubusercontent.com/TrendSeminar/MapVisualize_HousePrice/main/src/streamlit-app.mp4 "Making-of Animation")


#### How to run this demo
```
git clone https://github.com/TrendSeminar/MapVisualize_HousePrice.git
cd MapVisualize_HousePrice
pip install --upgrade streamlit pydeck pandas
streamlit run app.py
```


### Reference
Data from [Apartment Transaction Price API](https://www.data.go.kr/data/15057511/openapi.do) from Ministry of Land, Infrastructure and Transport.
