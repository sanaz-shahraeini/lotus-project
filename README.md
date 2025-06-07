# Lotus Project

## About the Project

Lotus is a web-based dashboard application designed for managing and reporting on calls (تماس ها). It provides users with a comprehensive overview of call statistics, including total calls, incoming calls, outgoing calls, and missed calls. The application features a responsive design, ensuring a consistent user experience across various devices, and supports both light and dark themes, as well as high-contrast modes for accessibility.

## Key Features

*   **Call Management Dashboard:** Displays key call metrics and statistics.
*   **Filtering and Search:** Allows users to filter and search call records.
*   **Responsive Design:** Adapts to different screen sizes for desktop and mobile viewing.
*   **Theming:** Supports light mode, dark mode, and high-contrast themes.
*   **User Interface:** Modern and clean UI for intuitive navigation and data visualization.

## Technology Stack

### Backend
*   **Python:** The primary backend programming language.
*   **Django:** A high-level Python web framework used for building the application structure, handling requests, and managing data.

### Frontend
*   **HTML5:** For structuring the web pages.
*   **CSS3:** For styling the application. Includes custom stylesheets and potentially utility-first CSS principles (inspired by or using Tailwind CSS).
*   **JavaScript:** For client-side interactivity and dynamic content.
*   **jQuery:** A JavaScript library used to simplify HTML DOM tree traversal and manipulation, as well as event handling and animation.

### Styling & UI Components
*   **Font Awesome:** Used for scalable vector icons.
*   **Jalali Datepicker:** A JavaScript datepicker component for selecting Jalali (Persian) dates.
*   **Custom CSS:** Extensive custom CSS files for specific component styling, theming (dark/light/high-contrast), and layout fixes.
*   **Fonts:** Utilizes Persian fonts such as 'Vazir' and 'IRANSansX'.

### Development Tools & Environment
*   **Virtual Environment (`venv`):** Used to manage project dependencies and isolate the project environment.

## Running the Project (Development)

1.  **Activate the virtual environment:**
    ```bash
    # Navigate to the Scripts directory within your venv
    cd path\to\your\project\venv\Scripts
    # Activate (example for PowerShell)
    .\Activate.ps1
    ```
2.  **Navigate to the project root directory** (where `manage.py` is located):
    ```bash
    cd path\to\your\project
    ```
3.  **Run the Django development server:**
    ```bash
    python manage.py runserver
    ```
4.  Open your web browser and go to `http://127.0.0.1:8000/` (or the address shown in your terminal).
