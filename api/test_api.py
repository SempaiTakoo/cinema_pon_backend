from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from movies.models import Genre, Director, Movie, Comment
from users.models import User

class APITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.genre = Genre.objects.create(name="Comedy")
        self.director = Director.objects.create(first_name="John", last_name="Doe")
        self.movie = Movie.objects.create(title="Test Movie", description="Test Description")
        self.movie.genres.add(self.genre)
        self.movie.directors.add(self.director)
        self.comment1 = Comment.objects.create(author=self.user, movie=self.movie, text="Great movie!")
        self.comment2 = Comment.objects.create(author=self.user, movie=self.movie, text="Amazing film!")
        self.comment3 = Comment.objects.create(author=self.user, movie=self.movie, text="Not bad")

    def test_create_genre(self):
        url = reverse("genre-list")
        data = {"name": "Drama"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 2)
        self.assertEqual(Genre.objects.last().name, "Drama")

    def test_create_director(self):
        url = reverse("director-list")
        data = {"first_name": "Jane", "last_name": "Smith"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Director.objects.count(), 2)
        self.assertEqual(Director.objects.last().first_name, "Jane")

    def test_create_movie(self):
        url = reverse("movie-list")
        data = {
            "title": "New Movie",
            "description": "New Description",
            "genres": [self.genre.id],
            "directors": [self.director.id]
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)
        self.assertEqual(Movie.objects.last().title, "New Movie")

    def test_delete_genre(self):
        url = reverse("genre-detail", args=[self.genre.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.count(), 0)

    def test_delete_director(self):
        url = reverse("director-detail", args=[self.director.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Director.objects.count(), 0)

    def test_delete_movie(self):
        url = reverse("movie-detail", args=[self.movie.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)

    def test_create_comment(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("comment-list")
        data = {
            "author": self.user.id,
            "movie": self.movie.id,
            "text": "Great movie!"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 4)
        self.assertEqual(Comment.objects.last().text, "Great movie!")
    
    def test_get_comments(self):
        url = reverse("comment-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comments = response.data.get('results', [])
        self.assertEqual(len(comments), 3)
        self.assertEqual(comments[0]["text"], "Not bad")
        self.assertEqual(comments[1]["text"], "Amazing film!")
        self.assertEqual(comments[2]["text"], "Great movie!")
        
        
    def test_update_comment(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("comment-detail", args=[self.comment1.id])
        data = {
            "text": "Updated comment"
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment1.refresh_from_db()
        self.assertEqual(self.comment1.text, "Updated comment")

    def test_delete_comment(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("comment-detail", args=[self.comment1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 2)

    def test_get_movie_with_comments(self):
        url = reverse("movie-detail", args=[self.movie.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["comments"]), 3)
        self.assertEqual(response.data["comments"][0]["text"], "Not bad")
        self.assertEqual(response.data["comments"][1]["text"], "Amazing film!")
        self.assertEqual(response.data["comments"][2]["text"], "Great movie!")

    def test_get_genre(self):
        url = reverse("genre-detail", args=[self.genre.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Comedy")

    def test_get_director(self):
        url = reverse("director-detail", args=[self.director.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "John")
        self.assertEqual(response.data['last_name'], "Doe")

    def test_get_movie(self):
        url = reverse("movie-detail", args=[self.movie.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Movie")
        self.assertEqual(len(response.data['genres']), 1)
        self.assertEqual(len(response.data['directors']), 1)
        self.assertEqual(len(response.data['comments']), 3)
