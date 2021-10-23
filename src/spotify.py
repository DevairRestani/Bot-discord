import requests

class Spotify:
    def __init__(self) -> None:
        self.clientId = '3353b17038be43a4a725a72829f7fc14'
        self.clientSecret = 'c65fe893b66b41d1853f4a310095dfb1'
        self.redirectUri = 'http://localhost:8888/callback'