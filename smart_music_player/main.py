import cv2
from deepface import DeepFace
import pygame
import os

# Function to capture image from webcam
def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame

# Function to detect emotion from an image
def detect_emotion(image):
    try:
        results = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
        if results:
            emotion = results[0]['dominant_emotion']  # Access the first result
            return emotion
        else:
            print("No faces detected in the image.")
            return "unknown"
    except ValueError as e:
        print("Error analyzing image:", e)
        return "unknown"

# Function to map emotion to genre
def get_genre(emotion):
    emotion_to_genre = {
        'happy': 'pop_happy',
        'sad': 'classical_sad',
        'angry': 'rock_angry',
        'surprise': 'electronic_surprise',
        'neutral': 'jazz_neutral',
        'fear': 'metal_fear',
        'disgust': 'blues_disgust',
        'contempt': 'folk_contempt',
        'unknown': 'jazz_unknown'  # Default genre for unknown emotions
    }
    return emotion_to_genre.get(emotion, 'jazz')

# Function to play music from a directory
def play_music(directory):
    songs = os.listdir(directory)
    if songs:
        song = os.path.join(directory, songs[0])  # Play the first song
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
    else:
        print("No songs found in the directory.")

# Function to display image with emotion
def display_image_with_emotion(image, emotion):
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 0, 0)  # Red color for the text
    font_scale = 1
    thickness = 2
    
    text = f"Emotion: {emotion}"
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_x = 10
    text_y = image.shape[0] - 10
    cv2.putText(image, text, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)
    
    cv2.imshow('Captured Image', image)
    cv2.waitKey(3000)  # Display the window for 3000 ms (3 seconds)
    cv2.destroyAllWindows()

# Main function
def main():
    pygame.mixer.init()

    # Capture image
    image = capture_image()

    # Detect emotion
    emotion = detect_emotion(image)
    print(f"Detected emotion: {emotion}")

    # Display the captured image with emotion
    display_image_with_emotion(image, emotion)

    # Get recommended genre
    genre = get_genre(emotion)
    print(f"Recommended genre: {genre}")

    # Play music
    music_directory = f'./music/{genre}'
    play_music(music_directory)

    # Keep the program running until the music stops
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__ == "__main__":
    main()
