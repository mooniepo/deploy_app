#import library
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

#atur page tab
st.set_page_config(
    page_title="Brazil E-commerce 2016-2018",
    page_icon="🦄",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#masukan dataset result
df = pd.read_csv(r'main_data.csv',encoding='unicode_escape')

#bersihkan dataset result dari outlier feature price
# Definisikan kondisi
kondisi1 = df['price'] > 0
kondisi2 = df['price'] < 277.4

# gabungkan kondisi tersebut menggunakan '&' (AND)
df_clean = df[kondisi1 & kondisi2]

#ubah column order_purchase_date dari object menjadi timestamp
df_clean['order_purchase_date_dt'] = pd.to_datetime(df_clean['order_purchase_date'])
df_clean.drop(columns=['order_purchase_date'], inplace=True)

#buat sidebar
with st.sidebar:
    st.title('🌍 Dataset konsumen E-commerce di Brazil 2016-2018')

    #memilih tema
    color_theme_list = ['skyblue','turquoise','indigo','tomato','springgreen']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    
    #memilih state
    state_list = list(df_clean.customer_state.unique())[::-1]
    additional_state = "all state"
    state_list.append(additional_state)
    selected_state = st.selectbox('Pilih state', state_list, index=len(state_list)-1)
    df_selected_state = df_clean[df_clean.customer_state == selected_state]

    #memilih tahun


#mengdefinisikan fungsi untuk visualisasi pada all state

#definisikan fungsi untuk scatter plot pada all state
def scatterplot_none():
    y_min = 0
    y_max = 500
    fig, ax = plt.subplots()
    ax.scatter(df_clean['order_purchase_date_dt'], df_clean['price'], color=selected_color_theme, label='Values')
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('tanggal pembelian')
    ax.set_ylabel('harga barang')
    ax.set_title('Scatter Plot untuk harga barang per tanggal pembelian dari 2016 - 2018')
    ax.legend()
    st.pyplot(fig)

#definisikan fungsi untuk scatter plot pada state tertentu
def scatter_price_state():
    y_min = 0
    y_max = 500
    fig, ax = plt.subplots()
    ax.scatter(df_selected_state['order_purchase_date_dt'], df_selected_state['price'], color=selected_color_theme, label='Values')
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('tanggal pembelian')
    ax.set_ylabel('harga barang')
    ax.set_title('Scatter Plot untuk harga barang pada state {} per tanggal pembelian dari 2016 - 2018'.format(selected_state))
    ax.legend()
    st.pyplot(fig)



#definisikan fungsi untuk bar chart 10 barang teratas pada all state
def productbar_none():
  fig, ax = plt.subplots()  # Create a figure and axis
  df_clean.product_category_name_english.value_counts().nlargest(10).plot(kind="bar", ax=ax, color=selected_color_theme)
  ax.set_title("Bar Chart untuk 10 produk dengan frekuensi terbanyak")
  ax.set_xlabel("Kategori Produk")
  ax.set_ylabel("Frekuensi")
  st.pyplot(fig)

#definisikan fungsi untuk bar chart 10 barang teratas pada state tertentu
def productbar_state():
    fig, ax = plt.subplots()  # Create a figure and axis
    df_selected_state.product_category_name_english.value_counts().nlargest(10).plot(kind="bar", ax=ax, color=selected_color_theme)
    ax.set_title("Bar Chart untuk 10 produk dengan frekuensi terbanyak pada state {}".format(selected_state))
    ax.set_xlabel("Kategori Produk")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)


#definisikan fungsi untuk pie chart pembayaran terbanyak pada all state
def piechart_payment_types_none():
    payment_type_counts = df_clean.payment_type.value_counts()
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(payment_type_counts, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'orange', 'green', 'red', 'purple'])
    ax.legend(wedges, payment_type_counts.index, title="Payment Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_title("Pie Chart untuk metode pembayaran yang digunakan di Brazil")
    st.pyplot(fig)

#definisikan fungsi untuk pie chart pembayaran terbanyak pada state tertentu
def piechart_payment_types_state():
    payment_type_counts = df_selected_state.payment_type.value_counts()
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(payment_type_counts, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'orange', 'green', 'red', 'purple'])
    ax.legend(wedges, payment_type_counts.index, title="Payment Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_title("Pie Chart untuk metode pembayaran yang digunakan di state {}".format(selected_state))
    st.pyplot(fig)   


#definisikan fungsi untuk state dengan jumlah customer terbanyak pada all satet
def customer_state_none():
    state_terbanyak = df_clean.groupby('customer_state')['customer_id'].nunique().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    state_terbanyak.plot(kind = 'bar', color = selected_color_theme)
    plt.title('10 states dengan jumlah customer terbanyak')
    plt.xlabel('State')
    plt.ylabel('jumlah customer')
    st.pyplot(fig)


#definisikan fungsi untuk city dengan jumlah customer terbanyak pada state tertentu
def customer_city_state():
    state_terbanyak = df_selected_state.groupby('customer_city')['customer_id'].nunique().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    state_terbanyak.plot(kind = 'bar', color = selected_color_theme)
    plt.title('10 city dengan jumlah customer terbanyak pada state {}'.format(selected_state))
    plt.xlabel('city')
    plt.ylabel('jumlah customer')
    st.pyplot(fig)

#mari kita atur konten kolomnya
col = st.columns((4,4), gap='medium')

#kolom pertama
with col[0]:
    if selected_state == 'all state':
        st.markdown('#### harga pembelian tahun 2016-2018')
        scatterplot_none()
    else:
        st.markdown('### harga pembelian tahun 2016-2018 pada state {}'.format(selected_state))
        scatter_price_state()

    if selected_state == 'all state':
        st.markdown('#### 10 produk dengan frekuensi terbanyak')
        productbar_none()
    else:
        st.markdown('### 10 produk dengan frekuensi terbanyak pada state {}'.format(selected_state))
        productbar_state()
 
with col[1]:
    if selected_state == 'all state':
        st.markdown('#### Metode pembayaran terbanyak')
        piechart_payment_types_none()
    else:
        st.markdown('### Metode pembayaran terbanyak pada state {}'.format(selected_state))
        piechart_payment_types_state()
     
    if selected_state == 'all state':
        st.markdown('### 10 state dengan jumlah customer terbanyak')
        customer_state_none()
    else:
        st.markdown('### 10 kota dengan jumlah customer terbanyak pada state {}'.format(selected_state))
        customer_city_state()





