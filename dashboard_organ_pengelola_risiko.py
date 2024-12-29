import streamlit as st
import pandas as pd
from plotly import express as px
import numpy as np
from io import StringIO

st.set_page_config(page_title="Dashboard Organ Pengelola Risiko", layout="wide")
st.title("Dashboard Komposisi dan Kualifikasi Organ Pengelola Risiko PT Pelindo Terminal Petikemas")

# Upload file Excel
data = st.file_uploader("Upload data komposisi dan kualifikasi organ pengelola risiko", type=["xlsx"])

if data is not None:
    try:
        # Membaca hanya sheet bernama "Data_Clean"
        df = pd.read_excel(data, sheet_name="Data_Clean")
        st.success("Data berhasil dimuat!")
        
        # Sidebar untuk filter
        st.sidebar.title("Filter Data")
        organ_selected = st.sidebar.selectbox(
            "Pilih Nama Organ Pengelola Risiko:",
            options = df["Nama organ pengelola risiko"].unique().tolist()
        )

        # Filter data berdasarkan pilihan
        filtered_data = df[df["Nama organ pengelola risiko"] == organ_selected]
        
        # Tampilkan hasil analisis
        st.title("Dashboard Analisis")
        st.write(f"Analisis untuk Organ Pengelola Risiko: **{organ_selected}**")

        # Jumlah Sertifikasi
        st.subheader("Jumlah Sertifikasi")
        fig_sertifikasi = px.bar(
            filtered_data,
            x="Nama pejabat",
            y="jumlah sertifikasi",
            text="jumlah sertifikasi",
            title="Jumlah Sertifikasi per Pejabat",
            labels={"jumlah sertifikasi": "Jumlah Sertifikasi", "Nama pejabat": "Pejabat"},
            color="jumlah sertifikasi",
            color_continuous_scale="Blues",
        )
        fig_sertifikasi.update_traces(textposition="outside")
        fig_sertifikasi.update_layout(
            xaxis_title="Nama Pejabat",
            yaxis_title="Jumlah Sertifikasi",
            title_x=0.5,
            title_font_size=20,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=50, b=50)
        )
        st.plotly_chart(fig_sertifikasi, use_container_width=True)

        # Jumlah Pelatihan
        st.subheader("Jumlah Pelatihan")
        fig_pelatihan = px.bar(
            filtered_data,
            x="Nama pejabat",
            y="jumlah pelatihan",
            text="jumlah pelatihan",
            title="Jumlah Pelatihan per Pejabat",
            labels={"jumlah pelatihan": "Jumlah Pelatihan", "Nama pejabat": "Pejabat"},
            color="jumlah pelatihan",
            color_continuous_scale="Oranges",
        )
        fig_pelatihan.update_traces(textposition="outside")
        fig_pelatihan.update_layout(
            xaxis_title="Nama Pejabat",
            yaxis_title="Jumlah Pelatihan",
            title_x=0.5,
            title_font_size=20,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=50, b=50)
        )
        st.plotly_chart(fig_pelatihan, use_container_width=True)

        # Pie Chart Komposisi Kualifikasi Sertifikasi
        st.subheader("Komposisi Kualifikasi Sertifikasi")
        kualifikasi_sertifikasi_counts = filtered_data["Keterangan Pemenuhan Kualifikasi Sertifikasi"].value_counts()

        fig_sertifikasi = px.pie(
            names=kualifikasi_sertifikasi_counts.index,
            values=kualifikasi_sertifikasi_counts.values,
            title="Kualifikasi Sertifikasi",
            color_discrete_sequence=px.colors.qualitative.Set2,  # Warna yang konsisten
            hole=0.4  # Membuat pie chart berbentuk donat
        )
        fig_sertifikasi.update_traces(textinfo='percent+label', pull=[0.1 if v > 20 else 0 for v in kualifikasi_sertifikasi_counts.values])
        fig_sertifikasi.update_layout(
            title_x=0.5,
            title_font_size=18,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        st.plotly_chart(fig_sertifikasi, use_container_width=True)

        # Pie Chart Komposisi Kualifikasi Pelatihan
        st.subheader("Komposisi Kualifikasi Pelatihan")
        kualifikasi_pelatihan_counts = filtered_data["Keterangan Pemenuhan Kualifikasi Pelatihan"].value_counts()

        fig_pelatihan = px.pie(
            names=kualifikasi_pelatihan_counts.index,
            values=kualifikasi_pelatihan_counts.values,
            title="Kualifikasi Pelatihan",
            color_discrete_sequence=px.colors.qualitative.Pastel,  # Warna lembut untuk pelatihan
            hole=0.4  # Membuat pie chart berbentuk donat
        )
        fig_pelatihan.update_traces(textinfo='percent+label', pull=[0.1 if v > 20 else 0 for v in kualifikasi_pelatihan_counts.values])
        fig_pelatihan.update_layout(
            title_x=0.5,
            title_font_size=18,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        st.plotly_chart(fig_pelatihan, use_container_width=True)

        # Tambahkan opsi untuk menampilkan atau menyembunyikan pie chart seluruh data
        st.subheader("Komposisi Sertifikasi dan Pelatihan untuk Seluruh Organ Pengelola Risiko")
        show_pie_chart = st.checkbox("Tampilkan Pie Chart")

        if show_pie_chart:
            # Pie chart untuk seluruh data sertifikasi
            st.subheader("Komposisi Kualifikasi Sertifikasi")
            kualifikasi_sertifikasi_counts = df["Keterangan Pemenuhan Kualifikasi Sertifikasi"].value_counts()
            fig_sertifikasi = px.pie(
                names=kualifikasi_sertifikasi_counts.index,
                values=kualifikasi_sertifikasi_counts.values,
                title="Kualifikasi Sertifikasi",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_sertifikasi, use_container_width=True)

            # Pie chart untuk seluruh data pelatihan
            st.subheader("Komposisi Kualifikasi Pelatihan")
            kualifikasi_pelatihan_counts = df["Keterangan Pemenuhan Kualifikasi Pelatihan"].value_counts()
            fig_pelatihan = px.pie(
                names=kualifikasi_pelatihan_counts.index,
                values=kualifikasi_pelatihan_counts.values,
                title="Kualifikasi Pelatihan",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_pelatihan, use_container_width=True)

        # Filter Individu (Setelah Chart)
        st.subheader("🔍Detail Sertifikasi dan Pelatihan Per Pejabat")
        individu_options = filtered_data["Nama pejabat"].unique().tolist()  # Hanya pilihan individu
        individu_selected = st.multiselect(
            "Pilih Nama Pejabat:",
            options=individu_options
        )

        # Filter data berdasarkan individu yang dipilih
        if individu_selected:
            individu_data = filtered_data[filtered_data["Nama pejabat"].isin(individu_selected)]
            st.write(f"Detail untuk Pejabat: **{', '.join(individu_selected)}**")

            # Pilihan detail dengan st.radio
            detail_option = st.radio(
                "Pilih Detail yang Ingin Dilihat:",
                options=["Detail Sertif", "Detail Pelatihan", "Detail Pejabat"],
                horizontal=True  # Opsi horizontal untuk efisiensi tampilan
            )

            if detail_option == "Detail Sertif":
                # Data sertifikasi
                detail_sertif_data = individu_data[
                    [
                        "Nama pejabat",
                        "bidang sertif 1", "nama sertif 1", "lembaga sertif 1", "berlaku sertif 1","Masa Berlaku Sertifikasi 1",
                        "bidang sertif 2", "nama sertif 2", "lembaga sertif 2", "berlaku sertif 2","Masa Berlaku Sertifikasi 2",
                        "bidang sertif 3", "nama sertif 3", "lembaga sertif 3", "berlaku sertif 3","Masa Berlaku Sertifikasi 3",
                        "bidang sertif 4", "nama sertif 4", "lembaga sertif 4", "berlaku sertif 4","Masa Berlaku Sertifikasi 4",
                        "Keterangan Pemenuhan Kualifikasi Sertifikasi"
                    ]
                ]

                st.write("### 🏆 **Detail Sertifikasi**")

                for index, row in detail_sertif_data.iterrows():
                    with st.expander(f"Detail Sertifikasi untuk {row['Nama pejabat']}"):
                        # Tentukan warna tampilan berdasarkan isi keterangan
                        if "Jumlah topik sertifikasi sudah terpenuhi" in row["Keterangan Pemenuhan Kualifikasi Sertifikasi"]:
                            warna = "#4CAF50"  # Hijau
                        else:
                            warna = "#FF4C4C"  # Merah

                        # Tampilkan keterangan dengan highlight warna sesuai isi teks
                        st.markdown(
                            f"""
                            <div style="padding: 10px; border: 2px solid {warna}; border-radius: 5px; background-color: #f9f9f9; color: {warna}; font-weight: bold;">
                                Keterangan Pemenuhan Kualifikasi Sertifikasi: {row['Keterangan Pemenuhan Kualifikasi Sertifikasi']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        # Tambahkan pemisah setelah keterangan
                        st.markdown("<hr style='border: 1px solid #ccc; margin: 20px 0;'>", unsafe_allow_html=True)
                        sertifikasi_valid = False  # Default jika tidak ada sertifikasi valid

                        for i in range(1, 5):
                            # Ambil data sertifikasi untuk indeks tertentu
                            bidang = row[f"bidang sertif {i}"]
                            nama = row[f"nama sertif {i}"]
                            lembaga = row[f"lembaga sertif {i}"]
                            berlaku = row[f"berlaku sertif {i}"]
                            masa_berlaku = row[f"Masa Berlaku Sertifikasi {i}"]

                            # Periksa apakah semua data kosong atau bernilai nol
                            if (
                                (pd.isna(bidang) or bidang == 0) and
                                (pd.isna(nama) or nama == 0) and
                                (pd.isna(lembaga) or lembaga == 0)
                            ):
                                continue  # Skip ke iterasi berikutnya jika semua kosong

                            # Jika ada data valid, tampilkan detailnya
                            sertifikasi_valid = True
                            st.write(f"**Sertifikasi {i}:**")
                            st.write(f"Bidang: {bidang if pd.notna(bidang) and bidang != 0 else '-'}")
                            st.write(f"Nama: {nama if pd.notna(nama) and nama != 0 else '-'}")
                            st.write(f"Lembaga: {lembaga if pd.notna(lembaga) and lembaga != 0 else '-'}")
                            st.write(f"Berlaku Hingga: {berlaku if pd.notna(berlaku) and berlaku != 0 else '-'}")
                            st.write(f"Masa Berlaku Sertifikasi: {masa_berlaku if pd.notna(masa_berlaku) and masa_berlaku != 0 else '-'}")
                            st.write("---")
                        

                        # Jika tidak ada data valid, tampilkan pesan tidak ada sertifikasi
                        if not sertifikasi_valid:
                            st.write("Belum ada sertifikasi yang terdaftar.")

            elif detail_option == "Detail Pelatihan":
                # Data pelatihan
                detail_pelatihan_data = individu_data[
                    [
                        "Nama pejabat",
                        "bidang pelatihan 1", "nama pelatihan 1", "penyelenggara pelatihan 1", "masa berlaku pelatihan 1", "waktu pelaksanaan pelatihan 1","jumlah jam pelatihan 1",
                        "bidang pelatihan 2", "nama pelatihan 2", "penyelenggara pelatihan 2", "masa berlaku pelatihan 2", "waktu pelaksanaan pelatihan 2","jumlah jam pelatihan 2",
                        "bidang pelatihan 3", "nama pelatihan 3", "penyelenggara pelatihan 3", "masa berlaku pelatihan 3", "waktu pelaksanaan pelatihan 3","jumlah jam pelatihan 3",
                        "bidang pelatihan 4", "nama pelatihan 4", "penyelenggara pelatihan 4", "masa berlaku pelatihan 4", "waktu pelaksanaan pelatihan 4","jumlah jam pelatihan 4",
                        "Keterangan Pemenuhan Kualifikasi Pelatihan"
                    ]
                ]

                st.write("### 📚**Detail Pelatihan**")

                for index, row in detail_pelatihan_data.iterrows():
                    with st.expander(f"Detail Pelatihan untuk {row['Nama pejabat']}"):
                        # Tentukan warna tampilan berdasarkan isi keterangan
                        if "Jumlah jam pelatihan sudah terpenuhi" in row["Keterangan Pemenuhan Kualifikasi Pelatihan"]:
                            warna = "#4CAF50"  # Hijau
                        else:
                            warna = "#FF4C4C"  # Merah

                        # Tampilkan keterangan dengan highlight warna sesuai isi teks
                        st.markdown(
                            f"""
                            <div style="padding: 10px; border: 2px solid {warna}; border-radius: 5px; background-color: #f9f9f9; color: {warna}; font-weight: bold;">
                                Keterangan Pemenuhan Kualifikasi Pelatihan: {row['Keterangan Pemenuhan Kualifikasi Pelatihan']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        # Tambahkan pemisah setelah keterangan
                        st.markdown("<hr style='border: 1px solid #ccc; margin: 20px 0;'>", unsafe_allow_html=True)

                        pelatihan_valid = False  # Default jika tidak ada pelatihan valid

                        for i in range(1, 5):
                            # Ambil data pelatihan untuk indeks tertentu
                            bidang = row[f"bidang pelatihan {i}"]
                            nama = row[f"nama pelatihan {i}"]
                            penyelenggara = row[f"penyelenggara pelatihan {i}"]
                            waktu_pelaksanaan = row[f"waktu pelaksanaan pelatihan {i}"]
                            masa = row[f"masa berlaku pelatihan {i}"]
                            jumlah_jam = row[f"jumlah jam pelatihan {i}"]

                            # Periksa apakah semua data kosong atau bernilai nol
                            if (
                                (pd.isna(bidang) or bidang == 0) and
                                (pd.isna(nama) or nama == 0) and
                                (pd.isna(penyelenggara) or penyelenggara == 0)
                            ):
                                continue  # Skip ke iterasi berikutnya jika semua kosong

                            # Jika ada data valid, tampilkan detailnya
                            pelatihan_valid = True
                            st.write(f"**Pelatihan {i}:**")
                            st.write(f"Bidang: {bidang if pd.notna(bidang) and bidang != 0 else '-'}")
                            st.write(f"Nama: {nama if pd.notna(nama) and nama != 0 else '-'}")
                            st.write(f"Penyelenggara: {penyelenggara if pd.notna(penyelenggara) and penyelenggara != 0 else '-'}")
                            st.write(f"Waktu Pelaksanaan: {waktu_pelaksanaan if pd.notna(waktu_pelaksanaan) and waktu_pelaksanaan != 0 else '-'}")
                            st.write(f"Jumlah Jam: {jumlah_jam if pd.notna(jumlah_jam) and jumlah_jam != 0 else '-'} jam")
                            st.write(f"Masa Berlaku: {masa if pd.notna(masa) and masa != 0 else '-'}")
                            st.write("---")

                        # Jika tidak ada data valid, tampilkan pesan tidak ada pelatihan
                        if not pelatihan_valid:
                            st.write("Belum ada pelatihan yang terdaftar.")
                            
                            

            elif detail_option == "Detail Pejabat":
                # Data pejabat
                detail_pejabat_data = individu_data[
                    [
                        "Nama pejabat",
                        "Jabatan Di Dalam Organ Pengelola Risiko",
                        "Tanggal Pengangkatan Sebagai Organ Pengelola Risiko",
                        "Periode Menjabat",
                        "Tempat Tanggal Lahir",
                        "Pendidikan Terakhir",
                        "Pengalaman Kerja 5 Tahun Terakhir"
                    ]
                ]

                st.write("### 🧑‍💼**Detail Pejabat**")

                for index, row in detail_pejabat_data.iterrows():
                    with st.expander(f"Detail Pejabat: {row['Nama pejabat']}"):
                        # Informasi utama pejabat
                        st.write(f"**Jabatan:** {row['Jabatan Di Dalam Organ Pengelola Risiko']}")
                        st.write(f"**Tanggal Pengangkatan:** {row['Tanggal Pengangkatan Sebagai Organ Pengelola Risiko']}")
                        st.write(f"**Tempat, Tanggal Lahir:** {row['Tempat Tanggal Lahir']}")
                        st.write(f"**Pendidikan Terakhir:** {row['Pendidikan Terakhir']}")

                        # Tampilan pengalaman kerja dan periode menjabat dalam dua kolom
                        pengalaman_kerja = row["Pengalaman Kerja 5 Tahun Terakhir"]
                        periode_menjabat = row["Periode Menjabat"]

                        if (pd.notna(pengalaman_kerja) and pengalaman_kerja != 0) or (pd.notna(periode_menjabat) and periode_menjabat != 0):
                            st.write("**Pengalaman dan Periode Menjabat:**")
                            col1, col2 = st.columns(2)

                            # Kolom 1: Pengalaman kerja
                            with col1:
                                st.markdown("##### Pengalaman Kerja")
                                if pd.notna(pengalaman_kerja) and pengalaman_kerja != 0:
                                    pengalaman_list = pengalaman_kerja.split(", ")
                                    for pengalaman in pengalaman_list:
                                        st.write(f"- {pengalaman}")
                                else:
                                    st.write("Tidak ada data.")

                            # Kolom 2: Periode menjabat
                            with col2:
                                st.markdown("##### Periode Menjabat")
                                if pd.notna(periode_menjabat) and periode_menjabat != 0:
                                    periode_list = periode_menjabat.split(", ")
                                    for periode in periode_list:
                                        st.write(f"- {periode}")
                                else:
                                    st.write("Tidak ada data.")
                        else:
                            st.write("**Pengalaman dan Periode Menjabat:** Tidak ada data.")
        else:
            st.write("Silakan pilih individu untuk melihat detailnya.")

        
    except Exception as e:
        st.error(f"Gagal membaca sheet 'Data_Clean': {e}")
else:
    st.info("Silakan unggah file Excel untuk memulai.")
