# Fleshka: A Flashcard Web App

#### Video Demo:  [here](https://youtu.be/5BPaDUuEusQ?si=MASv2-2kQD_Xxok4)

---

## Description

Fleshka is a modern, full-featured flashcard web application designed to help users learn and retain information efficiently. Inspired by the best practices in spaced repetition and user-centered design, Fleshka provides a sleek, intuitive interface for creating, organizing, and practicing flashcards. The app supports user authentication, personalized libraries, deck and card management, progress tracking, and a visually engaging study experience. Built with Flask, SQLite, and Bootstrap, Fleshka is both robust and easy to deploy.

---

## Features

- **User Authentication:** Secure signup, login, and logout with password hashing and session management.
- **Personalized Libraries:** Each user can create, view, and manage their own decks and cards.
- **Deck & Card Management:** Add, edit, delete, and import cards (via CSV) within custom decks. Decks can be color-coded and assigned unique icons.
- **Practice Mode:** Study cards in a randomized order, track your progress per card, and use keyboard shortcuts for a fast, focused experience.
- **Progress Tracking:** Each card tracks a progress score (0–10), and users maintain a daily study streak, visually represented with dynamic icons.
- **Profile Customization:** Users can select from a set of profile pictures and update their username or password.
- **Responsive UI:** Clean, modern design with custom fonts, icons, and a mobile-friendly layout.

---

## File Overview

### Root Directory
- **app.py**: The main Flask application. Handles all routing, user authentication, deck/card CRUD operations, practice logic, and session management. It is the entry point of the app and coordinates database access, template rendering, and user state.
- **helpers.py**: Utility functions and decorators, including:
  - `apology`: Renders error messages in a user-friendly way.
  - `login_required`: Decorator to restrict routes to logged-in users.
- **fleshka.db**: The SQLite database file storing all persistent data (users, decks, cards, progress, sessions).
- **requirements.txt**: Lists all Python dependencies, including Flask, Flask-Session, cs50, requests, and others.
- **README.md**: This documentation file.

### Database Schema
- **static/db/schema.sql**: SQL schema defining the following tables:
  - `users`: Stores user credentials, profile picture, and streak.
  - `decks`: User-created collections of cards, each with a name, color, and icon.
  - `cards`: Individual flashcards with a question and answer, linked to a deck.
  - `progresses`: Tracks each user's progress on each card (0–10 scale).
  - `sessions`: Logs each study session for streak tracking.
  - Indexes and triggers ensure data integrity and efficient queries.

### Static Assets
- **static/style.css**: Custom CSS for the app’s modern look, including color themes, card layouts, modals, and responsive design. Integrates custom fonts and icon styles.
- **static/script.js**: JavaScript for keyboard shortcuts and modal management, enabling fast deck/card creation and practice navigation.
- **static/fonts/**: Contains custom font files (SF-Pro, Namu) for branding and improved readability.
- **static/img/**: SVG and PNG images for UI icons (e.g., streak flames, mail, plus, trash, user profile pictures). These enhance the visual feedback and personalization throughout the app.
- **static/img/user_pics/**: A set of 8 profile pictures users can choose from in their settings.

### Templates (Jinja2/HTML)
- **templates/layout.html**: The base template, includes navigation, footer, and modal containers. All other templates extend this file.
- **templates/landing.html**: The public landing page, showcasing sample flashcards and a call-to-action for new users.
- **templates/login.html**: Combined signup and login form with tabbed navigation.
- **templates/home.html**: The user’s library, displaying all decks with card counts and progress.
- **templates/deck_view.html**: Shows all cards in a selected deck, with options to practice, add, or delete cards/decks.
- **templates/card_view.html**: Edit view for individual cards, allowing question/answer updates.
- **templates/practice.html**: The main study interface, with progress bars, keyboard navigation, and immediate feedback.
- **templates/settings.html**: User profile management, including profile picture, username, password, and account deletion.
- **templates/apology.html**: Friendly error page for displaying custom error messages.

---

## Design Choices & Rationale

- **User Experience:** The app prioritizes speed and clarity. Keyboard shortcuts (e.g., 'A' to add, 'P' to practice) and modals reduce friction for power users. The interface is visually clean, with color-coded decks and progress bars for motivation.
- **Data Integrity:** The schema enforces foreign keys, unique constraints, and uses triggers to automatically create progress records for new cards. This minimizes bugs and orphaned data.
- **Security:** Passwords are hashed using Werkzeug, and all sensitive routes require authentication. Sessions are managed securely via Flask-Session.
- **Extensibility:** The codebase is modular, with helpers and templates designed for easy extension (e.g., adding new card types, analytics, or spaced repetition algorithms).
- **Accessibility:** The UI uses semantic HTML, large clickable areas, and high-contrast colors for readability.
- **Visual Identity:** Custom fonts and icons give Fleshka a unique, memorable look, while SVGs and PNGs ensure fast loading and crisp rendering on all devices.

---

## Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Set up the database:**
   ```bash
   sqlite3 fleshka.db < static/db/schema.sql
   ```
3. **Run the app:**
   ```bash
   flask run
   ```

---

## Future Improvements
- Spaced repetition algorithms for smarter practice scheduling
- Deck sharing and collaboration
- Rich media support (images, audio)
- Analytics dashboard for learning insights
- Mobile app version

---

## Credits
- Built with [Flask](https://flask.palletsprojects.com/), [Bootstrap](https://getbootstrap.com/), and [CS50 Library for Python](https://cs50.readthedocs.io/).
- Icons and fonts are either open source or custom-designed for this project.

---

Fleshka is here to help you remember more, faster, and with joy!
