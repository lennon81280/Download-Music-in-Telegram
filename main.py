import os
import logging
import subprocess
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from telegram import InputFile
import io 


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)


load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
CHANNEL_ID = os.getenv("CHANNEL_ID")
WATERMARK_CHANNEL_ID = os.getenv("WATERMARK_CHANNEL_ID")
ADMINS = os.getenv('ADMINS')

ADMINS = [int(chat_id.strip()) for chat_id in ADMINS.split(',')]

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def get_song_metadata(sp, song_id):
    try:
        track_info = sp.track(song_id)
        artist_id = track_info['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        genres = artist_info['genres']

        genre_tags = ['#' + genre.replace(' ', '_').replace('-', '_').replace('&', '_') for genre in genres]

        audio_features = sp.audio_features(song_id)
        danceability = audio_features[0]['danceability']

        if danceability > 0.7:
            genre_tags.append('#dance')

        metadata = {
            'track_name': track_info['name'],
            'artist': track_info['artists'][0]['name'],
            'album': track_info['album']['name'],
            'release_date': track_info['album']['release_date'],
            'genres': genre_tags
        }

        return metadata

    except Exception as e:
        logger.error(f"Error while fetching song metadata: {e}")

    return None


def start(update, context):
    update.message.reply_text('Hello! I am your music bot.')

def dl(update, context):
    sender_chat_id = update.message.chat.id
    if sender_chat_id in ADMINS:
        if len(context.args) == 0:
            update.message.reply_text('Please provide a search string after /dl')
            return
        
        search_query = " ".join(context.args)
        
        # Use spotipy to search for the track on Spotify
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))
        results = sp.search(q=search_query, limit=1, type='track')
        
        if len(results['tracks']['items']) == 0:
            update.message.reply_text('No matching tracks found on Spotify.')
            return
        
        track = results['tracks']['items'][0]
        spotify_link = track['external_urls']['spotify']
        
        try:
            spotdl_download_command = [
                'spotdl',
                spotify_link,
                '--format',
                'mp3',
                '--bitrate',
                '320k',
                '--overwrite',
                'skip',
                '--output',
                './mp3',
            ]
            subprocess.run(spotdl_download_command, check=True)

            logger.info("Song downloaded successfully.")

        except Exception as e:
            logger.error(f"Error while downloading the song: {e}")
            update.message.reply_text(f"Error while downloading the song: {e}")

        for filename in os.listdir('./mp3'):
            if filename.endswith('.mp3'):
                file_path = os.path.join('./mp3', filename)
                metadata = get_song_metadata(sp, spotify_link)

                caption = (
                    f"Track Name: {metadata['track_name']}\n"
                    f"Artist: {metadata['artist']}\n"
                    f"Album: {metadata['album']}\n"
                    f"Release Date: {metadata['release_date']}\n"
                    f"Genres: {' '.join(metadata['genres'])}\n"
                    f"\n"
                    f"Channel : {WATERMARK_CHANNEL_ID}"
                )

                with open(file_path, 'rb') as audio_file:
                    audio_data = audio_file.read()
                audio_stream = io.BytesIO(audio_data)
                context.bot.send_audio(
                    chat_id=CHANNEL_ID,
                    audio=InputFile(audio_stream, filename=file_path), 
                    caption=caption
                )

                os.remove(file_path)
                logger.info(f"File '{filename}' sent and removed successfully.")
                update.message.reply_text(f"Downloaded '{filename}' and sent to channel.")
    else:
        update.message.reply_text("Unauthorized")

    

start_handler = CommandHandler('start', start)
dl_handler = CommandHandler('dl', dl)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(dl_handler)

updater.start_polling()
updater.idle()

