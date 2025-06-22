@echo off
echo Fixing Docker permission issues...

echo Stopping existing containers...
docker-compose down

echo Removing existing images to force rebuild...
docker rmi quiz-system 2>nul

echo Building new image with proper permissions...
docker-compose build --no-cache

echo Starting containers...
docker-compose up -d

echo Checking container logs...
timeout /t 5 >nul
docker-compose logs quiz-app

echo Done! Check if the application is running at http://localhost:5000
