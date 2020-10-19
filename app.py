import streamlit as st
import pandas as pd
import pydeck as pdk
import math, time


def main():
    st.title("House Price Fluctuations in Seoul, South Korea")
    st.sidebar.markdown("## **Controller**")

    period_slide_info = st.sidebar.empty()
    time_slider = st.sidebar.empty()
    period_info = st.empty()
    deck = st.empty()
    description = st.empty()
    animate = st.sidebar.button('animate')    
    st.sidebar.markdown("From this period, sliding to the end")

    time_idx = time_slider.slider('[2006-01 ~ 2020-09]', 1, 177, 88, 1)
    period, cur_df = update(time_idx, period_info, period_slide_info, description)
    deck.pydeck_chart(generate_layer(period, cur_df))

    if animate:
        time_idx = 75 if time_idx > 170 else time_idx
        for x in range(1, 177):
            time.sleep(.005)
            time_idx = time_slider.slider("[2006-01 ~ 2020-09]", 1, 177, time_idx + 1, 1)
            period, cur_df = update(time_idx, period_info, period_slide_info, description)
            deck.pydeck_chart(generate_layer(period, cur_df))

            if time_idx >= 177:
                break

    
    st.markdown("Reference  \n*Apartment Transaction Price API* from Ministry of Land, Infrastructure and Transport")


def update(time_idx, period_info, period_slide_info, description):
    period = "20%02d-%02d" % ((time_idx+71) // 12 , (time_idx+71) % 12 + 1)
    cur_df = prepare_data(df, aptdeal_wide, period=period)

    des1 = "**Total Average in Seoul:** %4.2f 만원/평" % cur_df[period].mean()
    des2 = "**Maximum Value Area (Price):** %s (%4.2f 만원/평)" % \
        (cur_df['SIG_KOR_NM'][cur_df[period].idxmax()], cur_df[period].max().max())

    period_info.info("**Period: %s**" % period)
    period_slide_info.markdown("**Period: %s**" % period)
    description.markdown("%s  \n%s" % (des1, des2))
    return period, cur_df



@st.cache(show_spinner=False, allow_output_mutation=True)
def generate_layer(period, cur_df):
    polygon_layer = pdk.Layer(
        "PolygonLayer",
        cur_df,
        id="geojson",
        opacity=0.9,
        stroked=False,
        get_polygon="coordinates",
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation="elevation",
        get_fill_color="fill_color",
        get_line_color=[255, 255, 255],
        auto_highlight=True,
        pickable=True,
        )   
    
    tooltip = {"html": "<b>지역:</b> {SIG_KOR_NM} <br/><b>기간:</b> %s <br/><b>평당가격:</b> {ave_price} 만원" % str(period)}
    cur_deck = pdk.Deck(
        polygon_layer,
        initial_view_state=view_state,
        tooltip=tooltip
        )
    return cur_deck


@st.cache(show_spinner=False, allow_output_mutation=True)
def prepare_data(df, aptdeal_wide, period='2020-09'):
    def color_scale(val):
        for i, b in enumerate(BREAKS):
            if val < b:
                return COLOR_RANGE[i]
        return COLOR_RANGE[i]

    def cal_elevation(val):
        return max((val-500)/1.5, 0) + math.exp(val * 0.0011)
        #return max((val-500)/10 + math.exp(val * 0.0003), 0)

    #df['SIG_CD']=df['SIG_CD'].astype(int)
    _df = pd.merge(df, aptdeal_wide.loc[period].to_frame(),
              how = 'left',
              left_on = 'SIG_CD',
              right_on = 'region_code'
             )
    _df["fill_color"] = _df[period].apply(color_scale)
    _df["elevation"] = _df[period].apply(cal_elevation)
    _df["ave_price"] = _df[period].apply(round)
    return _df


@st.cache(show_spinner=False, allow_output_mutation=True)
def load_data():
    aptdeal = pd.read_csv('https://raw.githubusercontent.com/TrendSeminar/MapVisualize_HousePrice/main/sample_data/deal_average.csv')
    aptdeal_wide = aptdeal.pivot(index='period', columns='region_code', values='price_per_pyeong').fillna(method='pad').fillna(0)

    import requests, json
    sig_r = json.loads(requests.get('https://raw.githubusercontent.com/TrendSeminar/MapVisualize_HousePrice/main/sample_data/sig_seoul.geojson').text)
    sig = pd.DataFrame(sig_r["features"])
    sig_geo, sig_prop = sig["geometry"], sig["properties"]

    # Parse the geometry out in Pandas
    df = pd.DataFrame()
    df["coordinates"] = sig_geo.apply(lambda row: row["coordinates"][0])
    df["SIG_CD"] = sig_prop.apply(lambda row: row["SIG_CD"])
    df['SIG_CD']=df['SIG_CD'].astype(int)
    df["SIG_ENG_NM"] = sig_prop.apply(lambda row: row["SIG_ENG_NM"])
    df["SIG_KOR_NM"] = sig_prop.apply(lambda row: row["SIG_KOR_NM"])
    return aptdeal_wide, df

aptdeal_wide, df = load_data() 
view_state = pdk.ViewState(
    **{"latitude": 37.5642135,
     "longitude": 127.0016985,
      "zoom": 9, "maxZoom": 14, "pitch": 60, "bearing": 0}
    )
COLOR_RANGE = [
    [65, 182, 196],
    [127, 205, 187],
    [199, 233, 180],
    [237, 248, 177],
    [255, 255, 204],
    [255, 237, 160],
    [254, 217, 118],
    [254, 178, 76],
    [253, 141, 60],
    [252, 78, 42],
    [227, 26, 28],
    [189, 0, 38],
    [128, 0, 38],
]
BREAKS = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500]



if __name__ == "__main__":
    main()

