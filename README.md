# Telegram Music Downloader Bot

This is a Telegram bot that can search for songs on Spotify and send them as music messages to a Telegram channel. The bot is built using Python and utilizes the Telegram Bot API and Spotify API.

## Features

- Search for songs on Spotify.
- Download the selected song using the `spotdl` command-line tool.
- Send the downloaded song with metadata provided by Spotify as a music message to a specified Telegram channel.

## Requirements

Install this packages.

- Python 3.7+
- `python-telegram-bot` library
- `spotipy` library
- `spotdl` command-line tool
- Spotify API credentials (client ID and client secret)
- Telegram Bot Token

## Setup

1. Clone the repository:

    `git clone https://github.com/lennon81280/lennon81280-Download-Music-in-Telegram.git`
  
    `cd telegram-music-downloader`

2. Obtain Spotify API credentials:
 - Create a Spotify developer account: [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
 - Create a new app to get the client ID and client secret.

4. Create a `.env` file in the project directory and add your environment variables:

```
TELEGRAM_TOKEN=your_telegram_bot_token
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
CHANNEL_ID=@your_channel_username
WATERMARK_CHANNEL_ID=@watermark_username_at_caption
ADMINS=authorized_users_chat_id_seperated_by_comma
```

5. Run the bot:

`python3 main.py`


## Usage

1. Invite your bot to your Telegram channel and give it appropriate permissions.

2. In the channel, use the `/dl` command followed by the song name to download and share the song. For example:

    `/dl Live in the Moment Portugal. The Man`


## Acknowledgments

- This project utilizes the `spotdl` command-line tool for downloading songs from Spotify: [spotdl GitHub Repository](https://github.com/spotDL/spotify-downloader)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
