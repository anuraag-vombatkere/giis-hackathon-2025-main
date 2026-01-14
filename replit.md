# Overview

Pixel Wellness is a gamified wellness application built with Flask that encourages users to complete wellness tasks and manage their screen time. The app features a retro pixel-art aesthetic and rewards users with points for completing activities like meditation, reading, and taking walks. Users can unlock avatar companions as they progress through their wellness journey.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **Styling**: Bootstrap 5 for responsive layout combined with custom pixel-art CSS
- **JavaScript**: Vanilla JavaScript for timer functionality and interactive elements
- **Design Pattern**: Retro gaming aesthetic with pixel fonts and gradients

## Backend Architecture
- **Framework**: Flask web framework with modular route organization
- **Session Management**: Flask-Session with filesystem storage for user state persistence
- **Configuration**: Environment-based configuration with fallback defaults
- **Middleware**: ProxyFix for proper header handling in deployment environments

## Data Storage
- **User Data**: Session-based storage (no persistent database)
- **Static Data**: In-memory Python data structures for avatars and wellness tasks
- **Session Configuration**: Filesystem-based sessions with security signing

## Authentication & User Management
- **Registration Flow**: Simple form-based user creation without passwords
- **Session Security**: Signed sessions with configurable secret keys
- **User State**: All user progress stored in Flask sessions including points, unlocked avatars, and profile data

## Core Features
- **Wellness Tasks**: Five predefined activities (reading, meditation, walking, hydration, breathing exercises)
- **Timer System**: JavaScript-based countdown timers for task completion
- **Gamification**: Point-based progression system with avatar unlocking
- **Avatar System**: 10 total avatars (3 free, 7 unlockable with points)

# External Dependencies

## Frontend Libraries
- **Bootstrap 5.1.3**: CSS framework for responsive design and components
- **Google Fonts**: Press Start 2P font for pixel-art typography

## Python Packages
- **Flask**: Core web framework
- **Flask-Session**: Session management extension
- **Werkzeug**: ProxyFix middleware for deployment

## Deployment Considerations
- **Host Configuration**: Configured for 0.0.0.0 binding on port 5000
- **Debug Mode**: Enabled for development environments
- **Session Security**: Uses environment variable SESSION_SECRET with fallback