import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from streamlit_option_menu import option_menu
import seaborn as sns


@st.cache_data
# Load Data CSV
def load_data(url):
    df = pd.read_csv(url)
    return df


def massa_produk(df_product):
    st.header('Analisis Produk')

    st.subheader('Distribusi Kategori Produk')
    df_product_category = df_product['product_category_name'].value_counts().sort_values(ascending=False).head(5)
    st.bar_chart(df_product_category)

    df_product_weight_max_index = df_product['product_weight_g'].idxmax()
    df_product_length_max_weight = df_product.loc[df_product_weight_max_index, 'product_length_cm']
    df_product_height_max_weight = df_product.loc[df_product_weight_max_index, 'product_height_cm']
    df_product_width_max_weight = df_product.loc[df_product_weight_max_index, 'product_width_cm']
    df_product_category_max_weight = df_product.loc[df_product_weight_max_index, 'product_category_name']
    st.markdown(f"Produk yang paling berat masuk ke dalam kategori **{df_product_category_max_weight}**.")

    st.subheader('Produk Paling Berat')
    top_5_heaviest_products = df_product.nlargest(5, 'product_weight_g')
    st.bar_chart(top_5_heaviest_products.set_index('product_id')['product_weight_g'])

    st.subheader('Informasi Produk Paling Berat')
    df_product_weight_max = df_product['product_weight_g'].max()
    st.markdown(f"Produk yang paling berat dengan bobot **{df_product_weight_max} gram.**")

    st.markdown(
        f"Dimensi produk yang paling berat: Panjang **{df_product_length_max_weight} cm**, Tinggi **{df_product_height_max_weight} cm**, Lebar **{df_product_width_max_weight} cm**."
    )
    df_product_id_max_weight = df_product.loc[df_product_weight_max_index, 'product_id']
    st.markdown(f"ID produk yang paling berat adalah **{df_product_id_max_weight}**.")


def distribusi_kategori(df_products):
    st.subheader('Distribusi Kategori Produk')

    df_product_category = df_products['product_category_name']
    st.dataframe(df_product_category)

    st.text('---------------------------------------------------------------------------------------------------------')

    df_product_category_unique = df_products['product_category_name'].nunique()
    st.markdown("\n**Jumlah produk dalam dataset: {}**".format(df_product_category_unique))

    st.text('---------------------------------------------------------------------------------------------------------')
    st.set_option('deprecation.showPyplotGlobalUse', False)

    plt.figure(figsize=(12, 6))
    sns.countplot(x='product_category_name', data=df_product,
                  order=df_product['product_category_name'].value_counts().index, palette='viridis')
    plt.title('Distribusi Top 10 Kategori Produk')
    plt.xlabel('Nama Kategori Produk')
    plt.ylabel('Jumlah Produk')
    plt.xticks(rotation=45, ha='right')
    st.pyplot()

    st.markdown("Grafik di atas menunjukkan distribusi kategori produk dalam dataset. ...")


def kategori_populer(df_products):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.subheader("Kategori Paling Populer")
    top_10_kategori = df_product['product_category_name'].value_counts().head(10)

    plt.figure(figsize=(12, 6))
    sns.countplot(x='product_category_name', data=df_product,
                  order=top_10_kategori.index, palette='viridis')
    plt.title('Distribusi Top 10 Kategori Produk')
    plt.xlabel('Nama Kategori Produk')
    plt.ylabel('Jumlah Produk')
    plt.xticks(rotation=45, ha='right')
    st.pyplot()


def metode_bayar(df_payment):
    st.subheader('Penggunaan Jenis Pembayaran')

    st.write("Distribusi Jenis Pembayaran:")
    df_payment_types = df_payment['payment_type']
    st.write(df_payment_types.value_counts())

    df_payment_value_max = df_payment['payment_value'].max()
    st.write("Pembayaran Tertinggi: $", df_payment_value_max)

    st.subheader("Diagram Batang Distribusi Jenis Pembayaran:")
    plt.figure(figsize=(8, 6))
    sns.countplot(x='payment_type', data=df_payment)
    plt.title('Distribusi Jenis Pembayaran')
    st.pyplot()

    st.subheader("Informasi Pembayaran Tertinggi:")
    st.write("Pembayaran Tertinggi: $", df_payment_value_max)

    st.subheader("Kesimpulan:")
    st.write(
        "Berdasarkan diagram batang, Credit Card merupakan pembayaran yang paling umum digunakan oleh para pelanggan.")
    st.write("Untuk transaksi tertinggi yang pernah dilakukan sebesar $", df_payment_value_max)


def transaksi(df_customer):
    st.subheader("Informasi Kode Pos Pelanggan Berdasarkan Kota:")
    df_customer_code = df_customer[['customer_zip_code_prefix', 'customer_city']]
    st.write(df_customer_code)

    st.subheader("Jumlah Kode Pos Unik Berdasarkan Kota:")
    unique_zip_codes_by_city = df_customer.groupby('customer_city')['customer_zip_code_prefix'].nunique().reset_index()
    sorted_unique_zip_codes = unique_zip_codes_by_city.sort_values(by='customer_zip_code_prefix', ascending=False)
    st.write(sorted_unique_zip_codes)

    st.subheader("Jumlah Kota Unik dalam Dataset:")
    df_customer_city = df_customer['customer_city'].nunique()
    st.write("Jumlah kota dalam dataset:", df_customer_city)

    st.subheader("Jumlah Pelanggan per Kode Pos:")
    df_customer_code = df_customer['customer_zip_code_prefix'].value_counts()
    st.write(df_customer_code)

    st.subheader("Jumlah Pelanggan per Kota:")
    df_customer_city_count = df_customer['customer_city'].value_counts()
    st.write(df_customer_city_count)

    st.subheader("Distribusi Kode Pos Pelanggan:")
    distribusi_customer = df_customer['customer_zip_code_prefix'].value_counts()
    top_customer = distribusi_customer.head(10)
    plt.figure(figsize=(10, 7))
    top_customer.plot(kind='bar', color='red')
    plt.title('Distribusi Customer')
    plt.xlabel('Nama Kode Pos Customer')
    plt.ylabel('Jumlah Customer')
    st.pyplot()


def total_produk(df_order_item):
    st.subheader("Total Item dalam Data Produk:")
    df_total_item = df_product['product_id']
    st.write(df_total_item)

    st.subheader("Harga dalam Data Order Items:")
    df_order_price = df_order_item['price']
    st.write(df_order_price)

    st.subheader("Nilai Pembayaran dalam Data Payment:")
    df_payment_value = df_payment['payment_value']
    st.write(df_payment_value)

    st.subheader("Jenis Pembayaran yang Dibersihkan:")
    df_payment_cleaned = df_payment[df_payment['payment_type'] != 'not_defined']
    st.write(df_payment_cleaned['payment_type'].value_counts())

    st.subheader("Data Produk Setelah Dibersihkan dari Nilai Null:")
    df_product_cleaned = df_product.dropna()
    st.write(df_product_cleaned)

    df_total_item = df_product['product_id'].count()
    st.write("Total Item:", df_total_item)

    df_order_price = round(df_order_item['price'].mean())
    st.write("Harga rata-rata pembelian produk:", df_order_price)

    df_count = df_product.count()
    df_total_item = df_product['product_id'].count()

    st.subheader("Grafik Data Item Marketplace:")
    plt.plot(df_count, marker='o', linestyle='-', color='#0f7216')

    for i in range(len(df_count) - 1):
        if df_count.iloc[i] != df_count.iloc[i + 1]:
            plt.text(df_count.index[i], df_count.iloc[i], f'{df_count.iloc[i]}', ha='center', va='bottom')

    plt.text(df_count.index[len(df_count) - 1], df_count.iloc[len(df_count) - 1], f'{df_count.iloc[len(df_count) - 1]}',
             ha='center', va='bottom')

    plt.xticks(rotation=45, ha='right')

    plt.title('Data Item Marketplace X')
    plt.ylabel('Jumlah Data')

    st.pyplot()

    st.subheader("Kesimpulan:")
    st.write("Jumlah Produk dalam Marketplace:", df_total_item)
    st.write("Rata-rata harga pembelian produk:", df_order_price)


def freight_value(df_order_item):
    st.subheader("Freight Value dalam Data Order Items:")
    df_order_freight = df_order_item['freight_value']
    st.write(df_order_freight)

    st.subheader("Freight Value Tertinggi:")
    df_order_freight_max = df_order_item['freight_value'].max()
    st.write("Freight value tertinggi adalah sebesar: $", df_order_freight_max)

    st.subheader("Grafik Maximum, Rata-Rata, dan Minimum Freight Value:")
    freight_max_value = df_order_item['freight_value'].max()
    freight_mean_value = df_order_item['freight_value'].mean()
    freight_min_value = df_order_item['freight_value'].min()

    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x=['Max', 'Mean', 'Min'], y=[freight_max_value, freight_mean_value, freight_min_value],
                     hue=['Max', 'Mean', 'Min'],
                     palette=['#ea3033', '#ffe9a3', '#0f7216'], legend=False)

    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    plt.ylabel('Freight Value')
    plt.title('Maximum, Rata-Rata, dan Minimum Freight Value')

    st.pyplot()

    st.subheader("Kesimpulan:")
    st.write("Freight Value atau biaya transportasi tertinggi adalah sebesar $", (df_order_freight_max))


# Memuat data
df_product = load_data("https://raw.githubusercontent.com/Rexaaor/UAS/main/data/products_dataset.csv")
df_products = load_data("https://raw.githubusercontent.com/Rexaaor/UAS/main/data/product_category_name_translation.csv")
df_payment = load_data("https://raw.githubusercontent.com/Rexaaor/UAS/main/data/order_payments_dataset.csv")
df_customer = load_data("https://raw.githubusercontent.com/Rexaaor/UAS/main/data/customers_dataset.csv")
df_order_item = load_data("https://raw.githubusercontent.com/Rexaaor/UAS/main/data/order_items_dataset.csv")

with st.sidebar:
    selected = option_menu('Menu', ['Dashboard'],
                           icons=["easel2", "graph-up"],
                           menu_icon="cast",
                           default_index=0)

if (selected == 'Dashboard'):
    st.header(f"Dashboard Analisis E-Commerce")
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        ["Massa Produk", "Distribusi", "Kategori Populer", "Metode Pembayaran", "Kode Pos", "Produk", "Freight Value"])

    with tab1:
        massa_produk(df_product)
    with tab2:
        distribusi_kategori(df_products)
    with tab3:
        kategori_populer(df_products)
    with tab4:
        metode_bayar(df_payment)
    with tab5:
        transaksi(df_customer)
    with tab6:
        total_produk(df_order_item)
    with tab7:
        freight_value(df_order_item)