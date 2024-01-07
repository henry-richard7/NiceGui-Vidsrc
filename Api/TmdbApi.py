from httpx import AsyncClient


class TmdbAPI:
    def __init__(self) -> None:
        self.tmdb_api_key = "da63548086e399ffc910fbc08526df05"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
        self.image_base_url_original = "https://image.tmdb.org/t/p/original"
        self.http_client = AsyncClient()

    async def external_id_tv(self, tmdb_id: int) -> str:
        url = f"https://api.themoviedb.org/3/tv/{tmdb_id}/external_ids"
        params = {"api_key": self.tmdb_api_key}

        response = await self.http_client.get(url, params=params)
        response = response.json()

        return response.get("imdb_id")

    async def discover_movies(self, page_no: int = 1) -> dict:
        results = list()

        url = "https://api.themoviedb.org/3/movie/now_playing"
        params = {
            "include_adult": True,
            "include_video": False,
            "language": "en-US",
            "sort_by": "popularity.desc",
            "api_key": self.tmdb_api_key,
            # "region": "IN",
            "page": page_no,
        }

        response = await self.http_client.get(url, params=params)
        response = response.json()

        max_pages = response.get("total_pages")
        items = response.get("results", [])

        for item in items:
            results.append(
                {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "banner": f"{self.image_base_url_original}{item.get('backdrop_path')}",
                    "poster": f"{self.image_base_url}{item.get('poster_path')}",
                    "ratings": item.get("vote_average"),
                    "release_date": item.get("release_date"),
                    "adult": item.get("adult"),
                }
            )

        return {"max_pages": max_pages, "items": results}

    async def discover_shows(self, page_no: int = 1) -> dict:
        results = list()

        url = "https://api.themoviedb.org/3/tv/on_the_air"
        params = {
            "include_adult": True,
            "include_video": False,
            "language": "en-US",
            "sort_by": "popularity.desc",
            "api_key": self.tmdb_api_key,
            "page": page_no,
        }

        response = await self.http_client.get(url, params=params)
        response = response.json()

        max_pages = response.get("total_pages")
        items = response.get("results", [])

        for item in items:
            results.append(
                {
                    "id": item.get("id"),
                    "title": item.get("name"),
                    "banner": f"{self.image_base_url_original}{item.get('backdrop_path')}",
                    "poster": f"{self.image_base_url}{item.get('poster_path')}",
                    "ratings": item.get("vote_average"),
                    "release_date": item.get("first_air_date"),
                    "adult": item.get("adult"),
                }
            )

        return {"max_pages": max_pages, "items": results}

    async def get_movie_details(self, tmdb_id: int) -> dict:
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
        params = {
            "language": "en-US",
            "append_to_response": "credits",
            "api_key": self.tmdb_api_key,
        }

        response = await self.http_client.get(url, params=params)
        response = response.json()

        imdb_id = response.get("imdb_id")
        title = response.get("title")
        plot = response.get("overview")
        banner = f"{self.image_base_url_original}{response.get('backdrop_path')}"
        poster = f"{self.image_base_url_original}{response.get('poster_path')}"
        genres = [x["name"] for x in response.get("genres", [])]
        ratings = response.get("vote_average")
        casts = [
            {
                "name": x["name"],
                "photo": f"{self.image_base_url_original}{x['profile_path']}"
                if x["profile_path"] != None
                else "https://cdn-icons-png.flaticon.com/512/3177/3177440.png",
            }
            for x in response["credits"]["cast"]
        ]
        release_date = response.get("release_date")

        return {
            "imdb_id": imdb_id,
            "title": title,
            "plot": plot,
            "banner": banner,
            "poster": poster,
            "genres": genres,
            "casts": casts,
            "ratings": ratings,
            "release_date": release_date,
        }

    async def get_show_details(self, tmdb_id: int) -> dict:
        url = f"https://api.themoviedb.org/3/tv/{tmdb_id}"
        params = {
            "language": "en-US",
            "append_to_response": "credits",
            "api_key": self.tmdb_api_key,
        }

        response = await self.http_client.get(url, params=params)
        response = response.json()

        imdb_id = response.get("imdb_id")
        title = response.get("name")
        plot = response.get("overview")
        banner = f"{self.image_base_url_original}{response.get('backdrop_path')}"
        poster = f"{self.image_base_url}{response.get('poster_path')}"
        genres = [x["name"] for x in response.get("genres")]
        ratings = response.get("vote_average")
        casts = [
            {
                "name": x["name"],
                "photo": f"{self.image_base_url}{x['profile_path']}",
            }
            for x in response["credits"]["cast"]
        ]
        release_date = response.get("first_air_date")

        imdb_id = imdb_id if imdb_id else await self.external_id_tv(tmdb_id)

        return {
            "imdb_id": imdb_id,
            "title": title,
            "plot": plot,
            "banner": banner,
            "poster": poster,
            "genres": genres,
            "casts": casts,
            "ratings": ratings,
            "release_date": release_date,
        }

    async def search(self, mode: str, query: str) -> list:
        results = list()

        url = f"https://api.themoviedb.org/3/search/{mode}"
        params = {"api_key": self.tmdb_api_key, "query": query}

        response = await self.http_client.get(url, params=params)
        response = response.json()

        items = response.get("results", [])

        for item in items:
            results.append(
                {
                    "id": item.get("id"),
                    "title": item["title" if mode == "movie" else "name"],
                    "banner": f"{self.image_base_url_original}{item.get('backdrop_path')}",
                    "poster": f"{self.image_base_url}{item.get('poster_path')}",
                    "ratings": item.get("vote_average"),
                    "release_date": item[
                        "release_date" if mode == "movie" else "first_air_date"
                    ],
                }
            )

        return results
