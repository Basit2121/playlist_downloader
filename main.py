import streamlit as st
import yt_dlp
import os
import zipfile
from mega import Mega
import glob

# Streamlit UI
st.image('image.png', width=200)

st.title("YouTube Playlist Downloader")

playlist_url = st.text_input("Enter YouTube Playlist URL:")

if st.button("Download Audio"):
    if playlist_url:
        # Get the current working directory where the script is located
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Create a yt-dlp instance with audio-only options
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': os.path.join(script_directory, '%(title)s.%(ext)s'),
        }

        # Create the yt-dlp downloader with the options
        ydl = yt_dlp.YoutubeDL(ydl_opts)

        # Download the playlist
        with st.spinner("Downloading..."):
            ydl.download([playlist_url])

        st.success("Download completed successfully!")

        # Create a zip file with downloaded songs
        with st.spinner("Creating zip file..."):
            zip_filename = os.path.join(script_directory, 'downloaded_songs.zip')
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                for root, _, files in os.walk(script_directory):
                    for file in files:
                        if file.endswith(".webm"):
                            zipf.write(os.path.join(root, file), os.path.basename(file))

        st.success("Zip file created successfully!")

        # Upload the zip file to Mega
        mega = Mega()
        m = mega.login("pucyleqo@afia.pro", "Basit24237")
        
        with st.spinner("Uploading to Mega..."):
            uploaded_file = m.upload(zip_filename)
            
        link = m.get_upload_link(uploaded_file)

        # Provide a link to download the uploaded file
        st.warning(f"Download Playlist : {link}")
        
        file_name = zip_filename
        
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            pass
        
        folder_path = ""

        # Create a list of all .mp3 and .webm files in the folder
        mp3_files = glob.glob(os.path.join(folder_path, "*.mp3"))
        webm_files = glob.glob(os.path.join(folder_path, "*.webm"))

        # Combine the lists
        files_to_delete = mp3_files + webm_files

        # Delete each file in the list
        for file_to_delete in files_to_delete:
            os.remove(file_to_delete)
            print(f"Deleted: {file_to_delete}")

        print("All .mp3 and .webm files have been deleted.")
        
    else:
        st.error("Please enter a valid YouTube Playlist URL.")
