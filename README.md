# 🎰 Lucky Slot Machine

A complete web-based slot machine game with user management, admin controls, and data persistence.

## ✨ Features

### 🏠 Home Page System
- **User Registration & Login**: Create accounts with usernames/passwords
- **Guest Mode**: Play without saving progress
- **Data Persistence**: All progress saved automatically in browser
- **User Dashboard**: Shows statistics and quick actions

### 🎮 Slot Machine Game
- **Smooth Animation**: Realistic slot machine scrolling from top to bottom
- **3x3 Grid**: Classic slot machine layout
- **8 Symbols**: 🍒 Cherry, 🍊 Orange, 🍋 Lemon, 💎 Diamond, ⭐ Star, 🍀 Clover, 7️⃣ Seven, 🎰 Slot
- **Win Detection**: Horizontal lines and diagonals (diagonals pay double!)
- **Betting System**: Adjustable bets with limits

### 🔐 Admin Panel
- **Access Code**: `12345##`
- **Game Controls**: Add balance, set balance, reset
- **Slot Controls**: Force win/lose, reset statistics, clear history
- **Settings**: Custom win rate, max bet limits

### 📊 History & Statistics
- **Game History**: Detailed spin history with timestamps
- **Statistics**: Total spins, wins, losses, win rate
- **Winning Odds**: Individual symbol probabilities
- **Real-time Updates**: All stats update automatically

## 🚀 How to Run

### Option 1: Direct Game (No User System)
```bash
python slotmachine_direct.py
```

### Option 2: Complete System (With User Management)
```bash
python slotmachine_home.py
```

### Option 3: Individual Components
```bash
# Create home page only
python slotmachine_home.py

# Create game only
python slotmachine_complete.py

# Create simple game only
python slotmachine_game.py
```

## 📁 Project Structure

```
autoclicker/
├── slotmachine_home.py          # Home page with user system
├── slotmachine_complete.py      # Complete slot machine with all features
├── slotmachine_direct.py        # Simple slot machine (no user system)
├── slotmachine_game.py          # Basic game file
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

## 🎯 Game Rules

### Symbols & Payouts
- 🍒 Cherry: $50
- 🍊 Orange: $100
- 🍋 Lemon: $150
- 💎 Diamond: $200
- ⭐ Star: $300
- 🍀 Clover: $750
- 7️⃣ Seven: $500
- 🎰 Slot: $1000

### Winning Combinations
- **Horizontal Lines**: 3 matching symbols in a row
- **Diagonal Lines**: 3 matching symbols diagonally (pays double!)

### Starting Balance
- **New Users**: $1,000
- **Guest Players**: $1,000
- **Admin**: Can add unlimited funds

## 🔧 Admin Features

### Access
- **Code**: `12345##`
- **Location**: Left panel in the game

### Controls Available
- **Balance Management**: Add $100, $500, $1000, or set custom amounts
- **Game Control**: Force next spin to win or lose
- **Statistics**: Reset all game statistics
- **History**: Clear all game history
- **Settings**: Adjust win rate (0-100%) and max bet (10-10,000)

## 💾 Data Storage

All data is stored locally in the browser using:
- **localStorage**: User accounts, game progress, statistics
- **Session Management**: Automatic login for returning users
- **Guest Data**: Temporary storage for guest players

## 🎨 Technical Details

### Technologies Used
- **HTML5**: Structure and layout
- **CSS3**: Styling and animations
- **JavaScript**: Game logic and user management
- **Python**: File generation and server setup

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge

### Responsive Design
- Desktop: Full three-panel layout
- Tablet: Stacked layout
- Mobile: Optimized for touch

## 🚀 Deployment

### Local Development
1. Clone the repository
2. Run any of the Python files
3. Open the generated HTML in your browser

### Web Hosting
1. Upload the generated HTML files to your web server
2. Ensure the files are in the same directory
3. Access via web browser

### GitHub Pages
1. Push to GitHub
2. Enable GitHub Pages in repository settings
3. Access via `https://username.github.io/repository-name`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🎉 Enjoy!

Have fun playing the slot machine! Remember to gamble responsibly - this is just a game! 🎰✨

---

**Created with ❤️ using Python, HTML, CSS, and JavaScript** 