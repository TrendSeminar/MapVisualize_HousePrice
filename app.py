import streamlit as st
import pandas as pd
import pydeck as pdk
import cv2, json, math, time



def main():
    st.title("House Price Fluctuations in Seoul, South Korea")
    aptdeal_wide, ori_df = load_data()    
    df = ori_df    

    # initial_time_idx = 170
    # period = "20%02d-%02d" % ((initial_time_idx+71) // 12 , (initial_time_idx+71) % 12 + 1)

    time_slider = st.empty()
    period_info = st.empty()

    time_idx = time_slider.slider('Time Slider', 1, 177, 170, 1)
    
    period = "20%02d-%02d" % ((time_idx+71) // 12 , (time_idx+71) % 12 + 1)
    period_info.info("Period: %s" % period)
    
    cur_df = prepare_data(df, aptdeal_wide, period=period)
    st.write("**Maxium Value Area (Ave Price per 3.3 m^2): **%s (₩ %4.2f)" % \
        (cur_df['SIG_ENG_NM'][cur_df[period].idxmax()], cur_df[period].max().max()))

    view_state = pdk.ViewState(
        **{"latitude": 37.5642135, "longitude": 127.0016985, "zoom": 9, "maxZoom": 14, "pitch": 40, "bearing": 0}
        )

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

    tooltip = {"html": "<b>지역:</b> {SIG_KOR_NM} <br/><b>기간:</b> %s <br/><b>평당가격:</b> {%s}" % (str(period),str(period))}

    st.pydeck_chart(pdk.Deck(
        polygon_layer,
        initial_view_state=view_state,
        tooltip=tooltip
    ))

    if st.button('animate'):
        time_idx = time_slider.slider("slider", 1, 177, 1, 1)
        for x in range(1, 177):
            time.sleep(.2)
            time_idx = time_slider.slider("slider", 1, 177, time_idx + 1, 1)
            period_info.info("Period: %s" % period)




@st.cache(show_spinner=False, allow_output_mutation=True)
def prepare_data(df, aptdeal_wide, period='2020-09'):
    def color_scale(val):
        for i, b in enumerate(BREAKS):
            if val < b:
                return COLOR_RANGE[i]
        return COLOR_RANGE[i]

    def cal_elevation(val):
        return (val / 2)
        #return math.exp(val * 0.0013)

    df['SIG_CD']=df['SIG_CD'].astype(int)
    _df = pd.merge(df, aptdeal_wide.loc[period].to_frame(),
              how = 'left',
              left_on = 'SIG_CD',
              right_on = 'region_code'
             )
    _df["fill_color"] = _df[period].apply(color_scale)
    _df["elevation"] = _df[period].apply(cal_elevation)
    return _df


@st.cache(show_spinner=False, allow_output_mutation=True)
def load_data():
    aptdeal = pd.read_csv('./src/csv/deal_average.csv')
    aptdeal_wide = aptdeal.pivot(index='period', columns='region_code', values='price_per_pyeong').fillna(method='pad').fillna(0)

    with open('./src/SIG_geojson/sig_seoul.geojson') as f:
        sig_r = json.load(f)
    sig = pd.DataFrame(sig_r["features"])
    sig_geo, sig_prop = sig["geometry"], sig["properties"]

    # Parse the geometry out in Pandas
    df = pd.DataFrame()
    df["coordinates"] = sig_geo.apply(lambda row: row["coordinates"][0])
    df["SIG_CD"] = sig_prop.apply(lambda row: row["SIG_CD"])
    df["SIG_ENG_NM"] = sig_prop.apply(lambda row: row["SIG_ENG_NM"])
    df["SIG_KOR_NM"] = sig_prop.apply(lambda row: row["SIG_KOR_NM"])

    return aptdeal_wide, df

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

