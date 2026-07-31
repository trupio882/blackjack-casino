# Blackjack Casino

A console-based Blackjack game with multi-player support, multiple table limits, complete betting system, and session management.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Status](https://img.shields.io/badge/status-completed-brightgreen.svg)]()

## Project Status

**COMPLETED** – This project is feature-complete and stable. All core functionality has been implemented, tested, and is ready for use.

- **Version**: 1.0.0
- **Status**: Production-ready
- **Last Update**: July 2026
- **Stability**: All features are fully functional and tested

### Future Plans
While the project is considered complete, minor improvements may be considered:
- **Performance Optimizations**: Potential micro-optimizations for larger player counts
- **UI Enhancements**: Possible color improvements for better readability
- **Bug Fixes**: Critical bug fixes if discovered
- **Documentation**: Minor updates to documentation as needed

**Note**: No major feature additions are planned. The project is stable and ready for use.

## Features

- **Multiple Players** – Add and remove players dynamically
- **Three Table Tiers** – Low (10-1000), Mid (1000-10000), High (10000-100000)
- **Full Blackjack Mechanics**:
  - Insurance when dealer shows an Ace
  - Split hands on identical cards
  - Double down bets
  - Blackjack pays 3:2
- **Balance Management** – Deposit funds via simulated card payment
- **Session System** – Save and load game sessions with SQLite database
- **Multi-deck System** – Automatic deck replacement when cards run low
- **Clean OOP Architecture** – Easily extensible and maintainable
- **Comprehensive Testing** – Full test coverage with pytest

## Installation & Setup

### Prerequisites
- Python 3.8 or higher

### Installation
# Clone the repository
git clone https://github.com/trupio882/blackjack-casino.git
cd blackjack-casino

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
Quick Start


python main.py
Using Docker


# Build the image
docker build -t blackjack-casino .

# Run the container
docker run -it blackjack-casino

# Or using Docker Compose
docker-compose up
How to Play

Session Management

On first launch, you'll be prompted to create a session. Sessions save player data and balances.


Available sessions:
[1] Session1, 2026-07-26 14:30:00
[2] Session2, 2026-07-25 10:15:00
Main Menu


+----------------------------------------------------------+
|                      MAIN MENU                             |
+----------------------------------------------------------+
| [1] TABLE LOW    |       10 - 1000                        |
| [2] TABLE MID    |     1000 - 10000                       |
| [3] TABLE HIGH   |    10000 - 100000                      |
+----------------------------------------------------------+
| [4] ADD PLAYER                                            |
| [5] DEPOSIT BALANCE                                       |
| [6] REMOVE PLAYER                                         |
+----------------------------------------------------------+
| [0] EXIT                                                  |
+----------------------------------------------------------+

Current players: Alice ($1000), Bob ($500)
Gameplay Flow

Select a table – Choose your betting limits
Place your bet – Enter an amount within the table limits
Play your hand:

h – Hit (take another card)
s – Stand (keep your current hand)
d – Double down (double your bet, take one card)
1 – Split (if you have two identical cards)
Insurance – Offered when dealer shows an Ace (bet half your stake)
Dealer's turn – Dealer draws until 17 or higher
Results – Wins/Losses/Pushes are displayed with updated balances
Game Rules

Blackjack: Natural 21 (Ace + 10-value card) pays 3:2
Insurance: Pays 2:1 if dealer has Blackjack
Split: Only possible with two identical ranks
Double Down: Double your bet after receiving first two cards
Dealer Stands: On 17 or higher (including soft 17)
Bust: Exceeding 21 results in an automatic loss
Project Structure


blackjack-casino/
├── main.py                    # Entry point & main menu
├── game.py                    # Core game logic
├── deck_for_black_jack.py     # Deck and card management
├── player.py                  # Player, hands, and HandList
├── bet_manager.py             # Betting operations
├── balance_manager.py         # Deposit simulation
├── save_manager.py            # Session management (SQLite)
├── tests/                     # Unit tests
│   ├── test_deck.py
│   ├── test_player.py
│   ├── test_game.py
│   ├── test_bet_manager.py
│   ├── test_save_manager.py
│   └── test_balance_manager.py
├── data/                      # Database storage
│   └── game.db               # SQLite database
├── requirements.txt           # Dependencies
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Docker Compose setup
├── .gitignore                # Git ignore rules
├── LICENSE                   # MIT License
├── CONTRIBUTING.md           # Contribution guidelines
├── setup.py                  # Package setup
├── pyproject.toml            # Project configuration
└── README.md                 # This file
Architecture

The project follows a clean object-oriented design with clear separation of concerns:

Class Diagram


+-------------------------------------------------------------+
|                      CasinoApp                               |
|  - tables: Dict[str, Black_jack]                            |
|  - players: List[Player]                                    |
|  - DB: SaveManager (Singleton)                              |
|  + run()                                                    |
|  + _play_at_table()                                         |
|  + _show_session()                                          |
+---------------------+---------------------------------------+
                      |
                      v
+-------------------------------------------------------------+
|                      Black_jack                              |
|  - deck: Deck                                                |
|  - dealer: Player                                            |
|  - players: List[Player]                                     |
|  - bet_manager: BetManager                                   |
|  + start_game()                                              |
|  + play_hand()                                               |
|  + check_winner()                                            |
+------+-------------------+------------------+----------------+
       |                   |                  |
       v                   v                  v
+--------------+  +-----------------+  +------------------+
|    Deck      |  |    Player       |  |   BetManager     |
|  - cards     |  |  - name         |  |  - min_bet       |
|  + shuffle() |  |  - hands        |  |  - max_bet       |
|  + card_deal |  |  - balance      |  |  + place_bet()   |
|  + update    |  |  + deposit()    |  |  + double_bet()  |
+--------------+  |  + split()      |  |  + insurance()   |
                  |  + withdraw()   |  +------------------+
                  +--------+--------+
                           |
                           v
                  +-----------------+
                  |   HandList      |
                  |  - head: Hand   |
                  |  - tail: Hand   |
                  |  + add_hand()   |
                  +--------+--------+
                           |
                           v
                  +-----------------+
                  |   Hand          |
                  |  - cards: List  |
                  |  - bet: int     |
                  |  - insurance    |
                  |  + calculate()  |
                  |  + can_split()  |
                  +-----------------+
Data Flow

User Input -> CasinoApp processes menu selections
Session Management -> SaveManager handles database operations
Game Setup -> Black_jack initializes deck and players
Betting Phase -> BetManager handles all monetary transactions
Gameplay -> Players interact with their hands
Resolution -> BetManager calculates payouts
Balance Update -> Player balances are updated and saved
Testing

Run the test suite to ensure everything is working correctly:



# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run with coverage report
pytest --cov=. tests/

# Run specific test file
pytest tests/test_game.py

# Run with verbose output
pytest -v tests/
Test Coverage

test_deck.py – Deck initialization, shuffling, dealing
test_player.py – Player creation, deposits, withdrawals, splits
test_game.py – Game flow, winner checking, hand actions
test_bet_manager.py – Betting, doubling, insurance
test_save_manager.py – Session management, database operations
test_balance_manager.py – Deposit simulation
Development

Code Style

Follows PEP 8
Uses Black for formatting
Type hints are mandatory
Docstrings for all public methods
SQLite for session persistence
Formatting



# Format code with Black
black .

# Check style with flake8
flake8 .

# Type checking with mypy
mypy .
Adding New Features

New Table Tier: Add to CasinoApp.tables dictionary
New Game Rule: Extend Black_jack class methods
New Bet Type: Extend BetManager class
New Player Feature: Extend Player or Hand classes
New Database Feature: Extend SaveManager class
Contributing

We welcome contributions! Please see our Contributing Guide for details.

Quick Contribution Checklist

Fork the repository
Create a feature branch (git checkout -b feature/amazing)
Write clean, tested code
Update documentation
Submit a Pull Request
Reporting Issues

Use the GitHub Issues
Provide clear steps to reproduce
Include Python version and OS information
Add screenshots if applicable
Performance

Memory Usage: ~50-100MB depending on number of players
Speed: Sub-second response times for all operations
Concurrency: Currently single-threaded, designed for future parallelization
Database: SQLite for lightweight persistence
Security

No external network calls
All data stored in SQLite database locally
No sensitive data logged
Input validation on all user inputs
Card details are not stored
License

This project is licensed under the MIT License – see the LICENSE file for details.

Author

trupio882

GitHub: @trupio882
Email: trupio882@gmail.com
Acknowledgments

Classic Blackjack rules derived from standard casino games
Inspired by various open-source card game implementations
Thanks to all contributors and testers
Resources

Blackjack Rules
Python Documentation
PEP 8 Style Guide
SQLite Documentation
Quick Commands

Command	Description
python main.py	Start the game
pytest tests/	Run tests
pytest --cov=. tests/	Run tests with coverage
black .	Format code
flake8 .	Check style
mypy .	Type checking
docker build -t blackjack .	Build Docker image
docker run -it blackjack	Run in Docker
docker-compose up	Run with Docker Compose
Good luck at the tables! May the odds be ever in your favor!

Made with Python

Simple Version for GitHub Repository Overview

# Blackjack Casino
A feature-rich console Blackjack game with multi-player support, multiple betting tables, session management, and complete game mechanics.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-completed-brightgreen.svg)]()

## Project Status: COMPLETED
This project is fully functional and stable. No major features are planned – only minor improvements and bug fixes may be added in the future.

## Quick Start
git clone https://github.com/trupio882/blackjack-casino.git
cd blackjack-casino
python main.py

## Key Features
- Multiple players with individual balances
- Three table tiers (Low/Mid/High)
- Full Blackjack: Split, Double Down, Insurance
- Deposit simulation via card details
- Multi-deck system with auto-refresh
- Session management with SQLite – Save and load game progress
- Docker support
- Comprehensive test coverage

## Documentation
Full documentation is available in the detailed README.

## Testing
pip install pytest
pytest tests/

## Contributing
Bug reports and minor improvements are welcome. See CONTRIBUTING.md for guidelines.

## License
MIT License – see LICENSE file.

Star this repo if you find it useful!