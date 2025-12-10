# Product Description Generator

An intelligent web application that automatically creates high-quality product descriptions and SEO-friendly keywords using Generative AI (Google Gemini).

## Features

-   **AI-Powered Descriptions**: Generates professional, marketing-ready product descriptions in seconds.
-   **SEO Keywords**: Automatically suggests 5 relevant SEO keywords tag.
-   **Audience Suggester**: Smart feature to suggest potential target audiences based on your product details.
-   **Premium UI**: Modern, responsive interface with glassmorphism design.
-   **tone Customization**: Choose from Professional, Excited, Luxury, or Minimalist tones.

## Tech Stack

-   **Backend**: FastAPI (Python)
-   **AI Model**: Google Gemini 2.5 Flash
-   **Frontend**: HTML5, CSS3, Vanilla JavaScript
-   **Styling**: Custom CSS with Glassmorphism

## Setup Instructions

### Prerequisites
-   Python 3.8+
-   Google Gemini API Key

### Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Install dependencies:
    ```bash
    pip install fastapi uvicorn pydantic python-dotenv google-generativeai
    ```

3.  Configure API Key:
    -   Create a `.env` file in the `backend/` folder.
    -   Add your key:
        ```env
        GEMINI_API_KEY=your_api_key_here
        ```

4.  Start the server:
    ```bash
    python -m uvicorn main:app --reload
    ```
    The server will start at `http://127.0.0.1:8000`.

### Frontend Setup

1.  Navigate to the `frontend/` directory.
2.  Open `index.html` in your web browser.

## Usage

1.  **Enter Product Details**: Fill in the Product Name and Key Features.
2.  **Select Audience**: Type your own or click **"✨ Suggest"** to get AI recommendations.
3.  **Choose Tone**: Select the desired tone for the description.
4.  **Generate**: Click "Generate Content" and watch the magic happen!

## License

This project is open source.
