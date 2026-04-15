from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for index creation
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample data
        users = [
            {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
            {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
            {"name": "Spider-Man", "email": "spiderman@marvel.com", "team": "Marvel"},
        ]
        db.users.insert_many(users)

        teams = [
            {"name": "Marvel", "members": ["Iron Man", "Captain America", "Spider-Man"]},
            {"name": "DC", "members": ["Superman", "Batman", "Wonder Woman"]},
        ]
        db.teams.insert_many(teams)

        activities = [
            {"user": "Superman", "activity": "Flight", "duration": 60},
            {"user": "Batman", "activity": "Martial Arts", "duration": 45},
            {"user": "Iron Man", "activity": "Suit Training", "duration": 50},
        ]
        db.activities.insert_many(activities)

        leaderboard = [
            {"team": "Marvel", "points": 300},
            {"team": "DC", "points": 250},
        ]
        db.leaderboard.insert_many(leaderboard)

        workouts = [
            {"user": "Spider-Man", "workout": "Web Swinging", "duration": 30},
            {"user": "Wonder Woman", "workout": "Lasso Practice", "duration": 40},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
