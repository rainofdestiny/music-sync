# Music Sync Application

This is a music synchronization application built with FastAPI that synchronizes liked tracks from Spotify to Yandex Music. The application uses Redis for caching and Celery for background tasks.

## Features

- Sync liked tracks from Spotify to Yandex Music.
- Supports background synchronization using Celery.
- Uses Redis for caching and rate-limiting.

## ToDo
- [ ] Add saving of synchronized tracks
- [ ] Cleanup requirements
- [ ] Add convenient logging  

## Requirements

- Docker and Docker Compose
- Python 3.10 or higher (if running locally)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/rainofdestiny/music-sync.git
cd music-sync
```

### 2. Create a .env file

Create a .env file in the project root with the following environment variables:

    SPOTIFY_CLIENT_ID=your_spotify_client_id
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIFY_REDIRECT_URI=your_spotify_redirect_uri
    YANDEX_TOKEN=your_yandex_token

Tips:
- [How to get Spotify data](https://google.com)
- [How to get Yandex data](https://yandex-music.readthedocs.io/en/main/token.html)

### 3. Build and start the Docker containers

Use Docker Compose to build and start the containers:

```bash
docker-compose up --build -d
```

### 4. Auth
Open __yourvdsip__:**8000**/auth and log in to the app through Spotify

## API Endpoints

    GET /auth: Redirects to the Spotify authentication URL.
    GET /callback: Handles the callback from Spotify and stores the access token.
    GET /sync: Triggers the synchronization of liked tracks from Spotify to Yandex Music.
    GET /sync-all: Syncs all liked tracks with pagination.

Common Commands

    Build and start services: docker-compose up --build
    Stop services: docker-compose down
