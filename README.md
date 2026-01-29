# YouTube Sentiment AI Assistant

A feature-rich Flask web application designed to help content creators understand and manage audience sentiment on YouTube. It leverages machine learning to classify comments, tracks video performance, and provides AI-powered guidance for channel growth and content strategy.

## [Deployed App (Placeholder - Update with your link)](https://your-render-app-url.onrender.com)

## Features

*   **User Authentication:** Secure signup and login with hashed passwords for personalized experience.
*   **AI Sentiment Analysis:** Classify YouTube comments as "Hope" (positive) or "Hate" (negative) speech using a pre-trained ML model.
*   **YouTube Video Tracking:** Monitor key video statistics (views, likes, subscribers) over custom intervals, with visualized trends.
*   **AI Chatbot Assistant:** Get personalized, actionable advice on content strategy, optimization, and growth directly from a Gemini AI-powered assistant.
*   **Prediction History:** Keep a record of all your sentiment analysis results for easy review.
*   **Interactive Dashboard:** Visualize overall sentiment statistics, review past predictions, and manage your video tracking history.
*   **Modern UI:** Responsive and intuitive user interface for a seamless experience.
*   **Secure Sessions:** Session-based authentication ensures protected routes and user data integrity.

## Tech Stack

*   **Backend:** Python, Flask
*   **Database:** SQLite
*   **ML/AI:** `scikit-learn` (for sentiment model), `transformers`, `torch`, Google Gemini API (`google-genai`), `google-api-python-client` (for YouTube Data API), `langdetect`
*   **Frontend:** Jinja2 templates, Custom CSS (`style.css`), JavaScript for dynamic interactivity
*   **Security:** `werkzeug` password hashing, session management
*   **Data Processing:** `pandas`

## Project Structure

```
.
├── app.py                  # Main Flask application
├── database.py             # SQLite database setup and ORM functions
├── requirements.txt        # Python dependencies
├── .env.example            # Example for environment variables
├── models/
│   └── hope_hate_model.pkl # Pre-trained ML model for sentiment analysis
├── services/               # Core application logic modules
│   ├── gemini_chat.py      # Handles interactions with the Gemini AI chatbot
│   ├── hate_classifier.py  # ML model loading and prediction for hope/hate speech
│   ├── youtube.py          # YouTube Data API interactions (comment fetching, video ID extraction)
│   └── youtube_tracker.py  # Logic for tracking and plotting YouTube video statistics
├── static/                 # Static assets
│   ├── css/                # Custom CSS files
│   ├── images/             # Images, including dynamically generated tracker plots
│   └── js/                 # JavaScript files for frontend interactivity
└── templates/              # HTML templates for all application pages
    ├── base.html           # Base layout template
    ├── home.html           # Landing page
    ├── login.html          # User login form
    ├── signup.html         # User registration form
    ├── predict.html        # YouTube comment sentiment prediction page
    ├── dashboard.html      # User dashboard with stats and history
    ├── chatbot.html        # AI Assistant chat interface
    ├── youtube_tracker.html# YouTube video tracking interface
    └── about.html          # About page
```

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/BhavishyaKatariya/youtube-sentiment-ai-assistant.git # Update with your repo
    cd youtube-sentiment-ai-assistant # Update with your repo name
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set Environment Variables:**
    Create a `.env` file in the root directory of your project.
    ```env
    GEMINI_API_KEY="your_gemini_api_key_here"
    YOUTUBE_API_KEY="your_youtube_data_api_key_here"
    SESSION_SECRET="a_strong_random_secret_key"
    ```
    *   **`GEMINI_API_KEY`**: Obtain your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
    *   **`YOUTUBE_API_KEY`**: Obtain your API key from the [Google Cloud Console](https://console.cloud.google.com/apis/credentials). Ensure the "YouTube Data API v3" is enabled for your project.
    *   **`SESSION_SECRET`**: A strong, random secret key for Flask session management. You can generate one using `python -c 'import os; print(os.urandom(24))'`.
    *   For deployment (e.g., on Render), set these variables directly in your hosting platform's environment settings.

4.  **Run the Application:**
    ```bash
    python app.py
    ```
    The application will be available in your browser at `http://0.0.0.0:5005`.

## Usage

*   **First Time Setup:**
    *   **Sign Up:** Create a new user account with a unique username, email, and password.
    *   **Login:** Use your credentials to access the application's features.
*   **Analyze YouTube Comments:**
    *   Navigate to the "Predict" page.
    *   Enter a YouTube video ID or a full YouTube video URL.
    *   The system will fetch comments, classify them, and display a breakdown of "Hope" and "Hate" speech.
    *   Your analysis results are automatically saved to your dashboard.
*   **Track Video Statistics:**
    *   Go to the "YouTube Tracker" page.
    *   Input a YouTube video ID, specify the tracking `interval` (in seconds), and the number of `samples` to collect.
    *   View dynamically generated plots showing trends in views, likes, and subscribers over the tracking period.
*   **Get AI Assistant Help:**
    *   Visit the "Chatbot" page.
    *   Engage with the Gemini AI assistant, asking questions about YouTube content strategy, channel growth, sentiment management, or anything else related to content creation.
    *   Receive personalized and actionable advice.
*   **View Dashboard:**
    *   Access the "Dashboard" page to see a summary of your sentiment predictions, overall sentiment statistics, and a history of your tracked YouTube videos.

## Database Schema

*   **`users` Table:**
    *   `id`: Primary key, integer
    *   `username`: Unique username, string
    *   `email`: Unique email address, string
    *   `password_hash`: Hashed password, string
    *   `created_at`: Account creation timestamp, datetime
*   **`predictions` Table:**
    *   `id`: Primary key, integer
    *   `user_id`: Foreign key to `users` table, integer
    *   `video_id`: YouTube video ID, string
    *   `sentiment`: Overall sentiment ('Positive', 'Negative', 'Neutral'), string
    *   `timestamp`: Prediction timestamp, datetime
*   **`tracker_history` Table:**
    *   `id`: Primary key, integer
    *   `user_id`: Foreign key to `users` table, integer
    *   `video_id`: YouTube video ID, string
    *   `plots_data`: JSON string containing paths to generated plot images, string
    *   `timestamp`: Tracking timestamp, datetime

## ML Model Features

*   **Model:** A pre-trained machine learning model (stored in `hope_hate_model.pkl`) using a `transformers`-based architecture.
*   **Input:** Raw text comments extracted from YouTube videos.
*   **Process:** The model first classifies the emotion of the text into categories like `sadness`, `joy`, `love`, `anger`, `fear`, `surprise`. These emotions are then mapped to a broader "Hope" or "Hate" sentiment.

## Security Features

*   **Password Hashing:** User passwords are securely stored as hashes using `werkzeug.security`.
*   **Session-Based Authentication:** Users are authenticated and their sessions are managed securely.
*   **Protected Routes:** Access to core application features (prediction, dashboard, tracker, chatbot) requires user login.
*   **Environment Variables:** Sensitive API keys and secret keys are managed through environment variables, preventing hardcoding.
*   **Input Validation:** User inputs are validated to prevent common vulnerabilities.

## Developer

**Bhavishya Katariya**
Full-Stack Developer & ML Engineer

## Color Scheme

Based on `static/css/style.css`:

*   **Primary:** `#4a90a4` (Teal/Blue)
*   **Secondary:** `#e85d75` (Reddish-Pink)
*   **Accent:** `#f4a261` (Orange)
*   **Text (Dark):** `#1a1a2e` (Very Dark Blue/Purple)
*   **Text (Light):** `#6b7280` (Grey)
*   **Background:** `#f0f4f8` (Light Grey/Blue)
*   **Card Background:** `#ffffff` (White)

## Future Enhancements

*   **Advanced ML Models:** Integrate more sophisticated sentiment analysis models, potentially fine-tuned for specific YouTube niches or slang.
*   **Social Media Integration:** Extend sentiment analysis and tracking to other social media platforms beyond YouTube.
*   **Real-time Monitoring:** Implement real-time sentiment analysis for live streams or newly posted comments.
*   **Data Visualization & Reporting:** Enhance the dashboard with more interactive charts, graphs, and exportable reports.
*   **Customizable AI Chatbot:** Allow users to customize the AI assistant's persona or focus areas.
*   **User-Defined Categories:** Enable users to define and train their own sentiment or keyword categories.

## License

This project is intended for educational purposes.

Built with Flask, Google Gemini AI, scikit-learn, and more.
