# House Price Fluctuations in Seoul, South Korea
[[Seongyong Kim](http://syoi92.github.io)], [[Rightstone](https://)]


This project demonstrates the house price fluctuations in units of 25 administrative districts in Seoul, South Korea, into an interactive app using [Pydeck](https://deckgl.readthedocs.io/en/latest/) and [Streamlit](https://streamlit.io). The unit is KRW/3.3m^2 (3.3m^2 = 1 pyeong, Korean unit of land).


![Making-of Animation](https://raw.githubusercontent.com/TrendSeminar/MapVisualize_HousePrice/main/src/streamlit-app.gif "Making-of Animation")


#### How to run this demo
```
pip install --upgrade streamlit pydeck pandas
streamlit run https://raw.githubusercontent.com/TrendSeminar/MapVisualize_HousePrice/main/app.py
```


#### Reference
Data: [[Apartment Transaction Price API](https://www.data.go.kr/data/15057511/openapi.do)] from MOLIT of Korea.
