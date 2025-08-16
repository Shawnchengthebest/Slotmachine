import webbrowser
import os

# Complete slot machine with all features
COMPLETE_GAME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎰 Lucky Slot Machine - Complete</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #2C3E50, #34495E);
            min-height: 100vh;
            color: white;
        }
        .main-container {
            display: flex;
            gap: 20px;
            max-width: 1400px;
            width: 100%;
            margin: 0 auto;
            padding: 20px;
        }
        .admin-panel {
            background: rgba(44, 62, 80, 0.95);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            flex: 0 0 300px;
            max-height: 600px;
            overflow-y: auto;
            border: 2px solid #E74C3C;
        }
        .game-panel {
            background: rgba(52, 73, 94, 0.9);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            text-align: center;
            flex: 1;
            min-width: 400px;
        }
        .history-panel {
            background: rgba(52, 73, 94, 0.9);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            flex: 1;
            min-width: 350px;
            max-height: 600px;
            overflow-y: auto;
        }
        .title { font-size: 2.5em; color: #F39C12; margin-bottom: 30px; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); }
        .info-panel { display: flex; justify-content: space-between; margin-bottom: 30px; gap: 20px; }
        .balance, .bet { flex: 1; padding: 15px; border-radius: 10px; font-size: 1.2em; font-weight: bold; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2); }
        .balance { background: linear-gradient(45deg, #27AE60, #2ECC71); }
        .bet { background: linear-gradient(45deg, #E74C3C, #C0392B); }
        .slot-machine { background: #34495E; border: 5px solid #F39C12; border-radius: 15px; padding: 20px; margin-bottom: 30px; box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5); }
        .reels { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 20px; }
        .reel-container { background: #2C3E50; border: 3px solid #F39C12; border-radius: 10px; padding: 5px; min-height: 120px; position: relative; overflow: hidden; box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3); }
        .reel { display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 2.5em; min-height: 120px; transition: all 0.3s ease; }
        .reel.spinning { animation: slotSpin 0.03s linear infinite; }
        @keyframes slotSpin { 0% { transform: translateY(0px); } 100% { transform: translateY(-40px); } }
        .reel-window { position: absolute; top: 50%; left: 0; right: 0; height: 40px; transform: translateY(-50%); background: linear-gradient(to bottom, transparent 0%, rgba(52, 73, 94, 0.8) 20%, rgba(52, 73, 94, 0.8) 80%, transparent 100%); pointer-events: none; z-index: 2; }
        .reel-symbols { display: flex; flex-direction: column; align-items: center; gap: 5px; }
        .controls { display: flex; justify-content: center; align-items: center; gap: 20px; margin-bottom: 20px; }
        .spin-btn { background: linear-gradient(45deg, #E74C3C, #C0392B); color: white; border: none; padding: 15px 30px; font-size: 1.3em; font-weight: bold; border-radius: 10px; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3); }
        .spin-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4); }
        .spin-btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
        .bet-controls { display: flex; align-items: center; gap: 10px; }
        .bet-btn { background: #95A5A6; color: white; border: none; width: 40px; height: 40px; font-size: 1.2em; border-radius: 50%; cursor: pointer; transition: all 0.3s ease; }
        .bet-btn:hover { background: #7F8C8D; transform: scale(1.1); }
        .bet-amount { font-size: 1.2em; font-weight: bold; color: #F39C12; min-width: 60px; }
        .win-message { font-size: 1.5em; font-weight: bold; margin-top: 20px; padding: 15px; border-radius: 10px; opacity: 0; transition: opacity 0.5s ease; }
        .win-message.show { opacity: 1; }
        .win { background: linear-gradient(45deg, #27AE60, #2ECC71); color: white; }
        .lose { background: linear-gradient(45deg, #E74C3C, #C0392B); color: white; }
        .paytable { background: rgba(52, 73, 94, 0.8); border-radius: 10px; padding: 15px; margin-top: 20px; font-size: 0.9em; }
        .paytable h3 { color: #F39C12; margin-bottom: 10px; }
        .paytable-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 5px; }
        .paytable-item { display: flex; justify-content: space-between; padding: 2px 0; }
        .admin-title { color: #E74C3C; font-size: 1.3em; margin-bottom: 15px; text-align: center; font-weight: bold; }
        .admin-section { background: rgba(52, 73, 94, 0.8); border-radius: 10px; padding: 15px; margin-bottom: 15px; }
        .admin-section h3 { color: #F39C12; margin-bottom: 10px; font-size: 1em; text-align: center; }
        .admin-input { width: 100%; padding: 8px; border: 1px solid #95A5A6; border-radius: 5px; background: #2C3E50; color: white; margin-bottom: 10px; font-size: 0.9em; }
        .admin-input:focus { outline: none; border-color: #F39C12; }
        .admin-btn { background: linear-gradient(45deg, #E74C3C, #C0392B); color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; font-weight: bold; margin: 2px; font-size: 0.8em; transition: all 0.3s ease; }
        .admin-btn:hover { transform: translateY(-1px); box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3); }
        .admin-btn.success { background: linear-gradient(45deg, #27AE60, #2ECC71); }
        .admin-btn.warning { background: linear-gradient(45deg, #F39C12, #E67E22); }
        .admin-status { font-size: 0.8em; padding: 5px; border-radius: 3px; margin-bottom: 10px; text-align: center; }
        .admin-status.success { background: rgba(39, 174, 96, 0.3); color: #2ECC71; }
        .admin-status.error { background: rgba(231, 76, 60, 0.3); color: #E74C3C; }
        .admin-hidden { display: none; }
        .admin-visible { display: block; }
        .history-title { color: #F39C12; font-size: 1.5em; margin-bottom: 20px; text-align: center; }
        .history-item { background: rgba(44, 62, 80, 0.8); border-radius: 10px; padding: 15px; margin-bottom: 10px; border-left: 4px solid #F39C12; transition: all 0.3s ease; }
        .history-item:hover { transform: translateX(5px); box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3); }
        .history-item.win { border-left-color: #27AE60; }
        .history-item.lose { border-left-color: #E74C3C; }
        .history-time { font-size: 0.8em; color: #BDC3C7; margin-bottom: 5px; }
        .history-result { font-weight: bold; margin-bottom: 5px; }
        .history-details { font-size: 0.9em; color: #ECF0F1; }
        .stats { background: rgba(44, 62, 80, 0.8); border-radius: 10px; padding: 15px; margin-bottom: 20px; }
        .stats h3 { color: #F39C12; margin-bottom: 10px; text-align: center; }
        .stat-item { display: flex; justify-content: space-between; margin-bottom: 5px; }
        .odds-panel { background: rgba(44, 62, 80, 0.8); border-radius: 10px; padding: 15px; margin-bottom: 20px; }
        .odds-panel h3 { color: #F39C12; margin-bottom: 10px; text-align: center; }
        .odds-item { display: flex; justify-content: space-between; margin-bottom: 8px; padding: 5px 0; border-bottom: 1px solid rgba(189, 195, 199, 0.2); }
        .odds-symbol { font-size: 1.2em; }
        .odds-probability { color: #F39C12; font-weight: bold; }
        .odds-payout { color: #27AE60; font-weight: bold; }
        .clear-history-btn { background: linear-gradient(45deg, #E74C3C, #C0392B); color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; margin-top: 10px; transition: all 0.3s ease; }
        .clear-history-btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3); }
        .back-btn { background: #95A5A6; margin-top: 20px; }
        @media (max-width: 1200px) { .main-container { flex-direction: column; gap: 20px; } .admin-panel, .game-panel, .history-panel { min-width: auto; } }
        @media (max-width: 600px) { .main-container { margin: 20px; } .title { font-size: 2em; } .info-panel { flex-direction: column; } .reel { font-size: 2em; min-height: 80px; } }
    </style>
</head>
<body>
    <div class="main-container">
        <!-- Admin Panel (Left Side) -->
        <div class="admin-panel">
            <h2 class="admin-title">🔐 ADMIN PANEL</h2>
            
            <!-- Access Code Section -->
            <div class="admin-section" id="accessSection">
                <h3>🔑 Access Code</h3>
                <input type="password" class="admin-input" id="accessCode" placeholder="Enter access code" maxlength="10">
                <button class="admin-btn" onclick="checkAccess()">🔓 Login</button>
                <div class="admin-status" id="accessStatus"></div>
            </div>
            
            <!-- Admin Controls (Hidden by default) -->
            <div class="admin-section admin-hidden" id="adminControls">
                <h3>🎮 Game Controls</h3>
                <button class="admin-btn success" onclick="addBalance(100)">+$100 Balance</button>
                <button class="admin-btn success" onclick="addBalance(500)">+$500 Balance</button>
                <button class="admin-btn success" onclick="addBalance(1000)">+$1000 Balance</button>
                <button class="admin-btn warning" onclick="setBalance(1000)">Reset Balance</button>
                <button class="admin-btn warning" onclick="setBalance(10000)">Set $10,000</button>
            </div>
            
            <div class="admin-section admin-hidden" id="adminControls2">
                <h3>🎰 Slot Controls</h3>
                <button class="admin-btn" onclick="forceWin()">🎯 Force Win</button>
                <button class="admin-btn" onclick="forceLose()">💀 Force Lose</button>
                <button class="admin-btn warning" onclick="resetStats()">📊 Reset Stats</button>
                <button class="admin-btn warning" onclick="clearAllHistory()">🗑️ Clear All</button>
            </div>
            
            <div class="admin-section admin-hidden" id="adminControls3">
                <h3>⚙️ Settings</h3>
                <label style="font-size: 0.8em; color: #BDC3C7;">Win Rate (%)</label>
                <input type="number" class="admin-input" id="winRate" placeholder="15.6" min="0" max="100" step="0.1">
                <button class="admin-btn" onclick="setWinRate()">Set Win Rate</button>
                
                <label style="font-size: 0.8em; color: #BDC3C7; margin-top: 10px; display: block;">Max Bet</label>
                <input type="number" class="admin-input" id="maxBet" placeholder="100" min="10" max="10000">
                <button class="admin-btn" onclick="setMaxBet()">Set Max Bet</button>
            </div>
            
            <div class="admin-section admin-hidden" id="adminControls4">
                <h3>🔒 Logout</h3>
                <button class="admin-btn" onclick="logout()">🚪 Logout</button>
            </div>
        </div>

        <!-- Game Panel (Center) -->
        <div class="game-panel">
            <h1 class="title">🎰 Lucky Slot Machine 🎰</h1>
            
            <div class="info-panel">
                <div class="balance" id="balance">💰 Balance: $1000</div>
                <div class="bet" id="bet">🎯 Bet: $10</div>
            </div>
            
            <div class="slot-machine">
                <div class="reels" id="reels">
                    <div class="reel-container">
                        <div class="reel" id="reel1">
                            <div class="reel-symbols">
                                <div>🎰</div><div>🎰</div><div>🎰</div><div>🎰</div>
                                <div>🎰</div><div>🎰</div><div>🎰</div><div>🎰</div>
                            </div>
                        </div>
                        <div class="reel-window"></div>
                    </div>
                    <div class="reel-container">
                        <div class="reel" id="reel2">
                            <div class="reel-symbols">
                                <div>🎰</div><div>🎰</div><div>🎰</div><div>🎰</div>
                                <div>🎰</div><div>🎰</div><div>🎰</div><div>🎰</div>
                            </div>
                        </div>
                        <div class="reel-window"></div>
                    </div>
                    <div class="reel-container">
                        <div class="reel" id="reel3">
                            <div class="reel-symbols">
                                <div>🎰</div><div>🎰</div><div>🎰</div><div>🎰</div>
                                <div>🎰</div><div>🎰</div><div>🎰</div><div>🎰</div>
                            </div>
                        </div>
                        <div class="reel-window"></div>
                    </div>
                </div>
            </div>
            
            <div class="controls">
                <button class="spin-btn" id="spinBtn" onclick="spin()">🎰 SPIN! 🎰</button>
                <div class="bet-controls">
                    <button class="bet-btn" onclick="changeBet(-10)">➖</button>
                    <div class="bet-amount" id="betAmount">$10</div>
                    <button class="bet-btn" onclick="changeBet(10)">➕</button>
                </div>
            </div>
            
            <div class="win-message" id="winMessage"></div>
            
            <div class="paytable">
                <h3>💰 Paytable</h3>
                <div class="paytable-grid">
                    <div class="paytable-item"><span>🍒 Cherry</span><span>$50</span></div>
                    <div class="paytable-item"><span>🍊 Orange</span><span>$100</span></div>
                    <div class="paytable-item"><span>🍋 Lemon</span><span>$150</span></div>
                    <div class="paytable-item"><span>💎 Diamond</span><span>$200</span></div>
                    <div class="paytable-item"><span>⭐ Star</span><span>$300</span></div>
                    <div class="paytable-item"><span>🍀 Clover</span><span>$750</span></div>
                    <div class="paytable-item"><span>7️⃣ Seven</span><span>$500</span></div>
                    <div class="paytable-item"><span>🎰 Slot</span><span>$1000</span></div>
                </div>
                <p style="margin-top: 10px; font-size: 0.8em; color: #BDC3C7;">Diagonals pay double! 🎯</p>
            </div>
            
            <button class="spin-btn back-btn" onclick="goHome()">🏠 Back to Home</button>
        </div>

        <!-- History Panel (Right Side) -->
        <div class="history-panel">
            <h2 class="history-title">📊 Game History</h2>
            
            <div class="odds-panel">
                <h3>🎯 Winning Odds</h3>
                <div class="odds-item">
                    <span class="odds-symbol">🍒 Cherry</span>
                    <span class="odds-probability">12.5%</span>
                    <span class="odds-payout">$50</span>
                </div>
                <div class="odds-item">
                    <span class="odds-symbol">🍊 Orange</span>
                    <span class="odds-probability">12.5%</span>
                    <span class="odds-payout">$100</span>
                </div>
                <div class="odds-item">
                    <span class="odds-symbol">🍋 Lemon</span>
                    <span class="odds-probability">12.5%</span>
                    <span class="odds-payout">$150</span>
                </div>
                <div class="odds-item">
                    <span class="odds-symbol">💎 Diamond</span>
                    <span class="odds-probability">12.5%</span>
                    <span class="odds-payout">$200</span>
                </div>
                <div class="odds-item">
                    <span class="odds-symbol">⭐ Star</span>
                    <span class="odds-probability">12.5%</span>
                    <span class="odds-payout">$300</span>
                </div>
                <div class="odds-item">
                    <span class="odds-symbol">🍀 Clover</span>
                    <span class="odds-probability">12.5%</span>
                    <span class="odds-payout">$750</span>
                </div>
                <div class="odds-item">
                    <span class="odds-symbol">7️⃣ Seven</span>
                    <span class="odds-probability">12.5%</span>
                    <span class="odds-payout">$500</span>
                </div>
                <div class="odds-item">
                    <span class="odds-symbol">🎰 Slot</span>
                    <span class="odds-probability">12.5%</span>
                    <span class="odds-payout">$1000</span>
                </div>
                <div style="margin-top: 10px; padding-top: 10px; border-top: 2px solid #F39C12; text-align: center; font-weight: bold; color: #E74C3C;">
                    Overall Win Rate: ~15.6%
                </div>
            </div>

            <div class="stats">
                <h3>📈 Statistics</h3>
                <div class="stat-item">
                    <span>Total Spins:</span>
                    <span id="totalSpins">0</span>
                </div>
                <div class="stat-item">
                    <span>Wins:</span>
                    <span id="totalWins">0</span>
                </div>
                <div class="stat-item">
                    <span>Losses:</span>
                    <span id="totalLosses">0</span>
                </div>
                <div class="stat-item">
                    <span>Win Rate:</span>
                    <span id="winRate">0%</span>
                </div>
                <div class="stat-item">
                    <span>Total Won:</span>
                    <span id="totalWon">$0</span>
                </div>
                <div class="stat-item">
                    <span>Total Lost:</span>
                    <span id="totalLost">$0</span>
                </div>
            </div>
            
            <div id="historyList">
                <!-- History items will be added here -->
            </div>
            
            <button class="clear-history-btn" onclick="clearHistory()">🗑️ Clear History</button>
        </div>
    </div>

    <script>
        // Game state
        let balance = 1000;
        let bet = 10;
        let isSpinning = false;
        let maxBet = 100;
        let customWinRate = 15.6;
        const symbols = ['🍒', '🍊', '🍋', '💎', '7️⃣', '🎰', '🍀', '⭐'];
        const payouts = {
            '🍒': 50, '🍊': 100, '🍋': 150, '💎': 200,
            '7️⃣': 500, '🎰': 1000, '🍀': 750, '⭐': 300
        };

        // Admin state
        let isAdminLoggedIn = false;
        const ADMIN_CODE = '12345##';

        // History tracking
        let gameHistory = [];
        let totalSpins = 0;
        let totalWins = 0;
        let totalLosses = 0;
        let totalWon = 0;
        let totalLost = 0;

        // Load user data
        let currentUser = JSON.parse(localStorage.getItem('slotMachineCurrentUser')) || {
            username: 'Guest Player',
            balance: 1000,
            totalSpins: 0,
            totalWins: 0,
            totalLosses: 0,
            totalWon: 0,
            totalLost: 0,
            gameHistory: []
        };

        // Initialize game
        function initGame() {
            balance = currentUser.balance;
            totalSpins = currentUser.totalSpins;
            totalWins = currentUser.totalWins;
            totalLosses = currentUser.totalLosses;
            totalWon = currentUser.totalWon;
            totalLost = currentUser.totalLost;
            gameHistory = currentUser.gameHistory || [];
            
            updateDisplay();
            updateHistoryDisplay();
        }

        function updateDisplay() {
            document.getElementById('balance').textContent = `💰 Balance: $${balance}`;
            document.getElementById('bet').textContent = `🎯 Bet: $${bet}`;
            document.getElementById('betAmount').textContent = `$${bet}`;
            updateStats();
        }

        function updateStats() {
            document.getElementById('totalSpins').textContent = totalSpins;
            document.getElementById('totalWins').textContent = totalWins;
            document.getElementById('totalLosses').textContent = totalLosses;
            document.getElementById('winRate').textContent = totalSpins > 0 ? `${((totalWins / totalSpins) * 100).toFixed(1)}%` : '0%';
            document.getElementById('totalWon').textContent = `$${totalWon}`;
            document.getElementById('totalLost').textContent = `$${totalLost}`;
        }

        function addToHistory(wins, payout, betAmount) {
            const now = new Date();
            const timeString = now.toLocaleTimeString();
            const dateString = now.toLocaleDateString();
            
            const isWin = wins.length > 0;
            const historyItem = {
                time: `${dateString} ${timeString}`,
                result: isWin ? 'WIN' : 'LOSS',
                bet: betAmount,
                payout: payout,
                wins: wins,
                isWin: isWin
            };
            
            gameHistory.unshift(historyItem);
            if (gameHistory.length > 50) {
                gameHistory.pop();
            }
            
            updateHistoryDisplay();
        }

        function updateHistoryDisplay() {
            const historyListEl = document.getElementById('historyList');
            historyListEl.innerHTML = '';
            
            gameHistory.forEach((item, index) => {
                const historyItem = document.createElement('div');
                historyItem.className = `history-item ${item.isWin ? 'win' : 'lose'}`;
                
                const winDetails = item.wins.map(win => {
                    if (win.type === 'horizontal') {
                        return `${win.symbol} ${win.symbol} ${win.symbol} - Line ${win.row + 1}`;
                    } else {
                        return `${win.symbol} ${win.symbol} ${win.symbol} - Diagonal`;
                    }
                }).join(', ');
                
                historyItem.innerHTML = `
                    <div class="history-time">${item.time}</div>
                    <div class="history-result">${item.isWin ? '🎉 WIN' : '😔 LOSS'} - Bet: $${item.bet}</div>
                    <div class="history-details">
                        ${item.isWin ? `Won: $${item.payout} | ${winDetails}` : 'No winning combinations'}
                    </div>
                `;
                
                historyListEl.appendChild(historyItem);
            });
        }

        function clearHistory() {
            if (confirm('Are you sure you want to clear all game history?')) {
                gameHistory = [];
                updateHistoryDisplay();
                saveUserData();
            }
        }

        // Admin Functions
        function checkAccess() {
            const inputCode = document.getElementById('accessCode').value;
            const statusEl = document.getElementById('accessStatus');
            
            if (inputCode === ADMIN_CODE) {
                isAdminLoggedIn = true;
                statusEl.textContent = '✅ Access granted!';
                statusEl.className = 'admin-status success';
                
                document.getElementById('adminControls').classList.remove('admin-hidden');
                document.getElementById('adminControls').classList.add('admin-visible');
                document.getElementById('adminControls2').classList.remove('admin-hidden');
                document.getElementById('adminControls2').classList.add('admin-visible');
                document.getElementById('adminControls3').classList.remove('admin-hidden');
                document.getElementById('adminControls3').classList.add('admin-visible');
                document.getElementById('adminControls4').classList.remove('admin-hidden');
                document.getElementById('adminControls4').classList.add('admin-visible');
                
                document.getElementById('accessSection').classList.add('admin-hidden');
                document.getElementById('accessCode').value = '';
            } else {
                statusEl.textContent = '❌ Invalid access code!';
                statusEl.className = 'admin-status error';
                document.getElementById('accessCode').value = '';
            }
        }

        function logout() {
            isAdminLoggedIn = false;
            
            document.getElementById('adminControls').classList.add('admin-hidden');
            document.getElementById('adminControls2').classList.add('admin-hidden');
            document.getElementById('adminControls3').classList.add('admin-hidden');
            document.getElementById('adminControls4').classList.add('admin-hidden');
            
            document.getElementById('accessSection').classList.remove('admin-hidden');
            document.getElementById('accessStatus').textContent = '';
        }

        function addBalance(amount) {
            if (!isAdminLoggedIn) return;
            balance += amount;
            updateDisplay();
            showAdminMessage(`✅ Added $${amount} to balance`);
        }

        function setBalance(amount) {
            if (!isAdminLoggedIn) return;
            balance = amount;
            updateDisplay();
            showAdminMessage(`✅ Balance set to $${amount}`);
        }

        function forceWin() {
            if (!isAdminLoggedIn) return;
            window.forceNextWin = true;
            showAdminMessage('🎯 Next spin will be a win!');
        }

        function forceLose() {
            if (!isAdminLoggedIn) return;
            window.forceNextLose = true;
            showAdminMessage('💀 Next spin will be a loss!');
        }

        function resetStats() {
            if (!isAdminLoggedIn) return;
            if (confirm('Are you sure you want to reset all statistics?')) {
                totalSpins = 0;
                totalWins = 0;
                totalLosses = 0;
                totalWon = 0;
                totalLost = 0;
                updateStats();
                showAdminMessage('📊 Statistics reset!');
            }
        }

        function clearAllHistory() {
            if (!isAdminLoggedIn) return;
            if (confirm('Are you sure you want to clear all game history?')) {
                gameHistory = [];
                updateHistoryDisplay();
                showAdminMessage('🗑️ All history cleared!');
            }
        }

        function setWinRate() {
            if (!isAdminLoggedIn) return;
            const newRate = parseFloat(document.getElementById('winRate').value);
            if (newRate >= 0 && newRate <= 100) {
                customWinRate = newRate;
                showAdminMessage(`⚙️ Win rate set to ${newRate}%`);
            } else {
                showAdminMessage('❌ Invalid win rate! Use 0-100');
            }
        }

        function setMaxBet() {
            if (!isAdminLoggedIn) return;
            const newMax = parseInt(document.getElementById('maxBet').value);
            if (newMax >= 10 && newMax <= 10000) {
                maxBet = newMax;
                if (bet > maxBet) {
                    bet = maxBet;
                    updateDisplay();
                }
                showAdminMessage(`⚙️ Max bet set to $${newMax}`);
            } else {
                showAdminMessage('❌ Invalid max bet! Use 10-10000');
            }
        }

        function showAdminMessage(message) {
            const statusEl = document.getElementById('accessStatus');
            statusEl.textContent = message;
            statusEl.className = 'admin-status success';
            setTimeout(() => {
                statusEl.textContent = '';
            }, 3000);
        }

        function changeBet(amount) {
            if (isSpinning) return;
            
            const newBet = bet + amount;
            if (newBet >= 10 && newBet <= maxBet && newBet <= balance) {
                bet = newBet;
                updateDisplay();
                
                const btn = event.target;
                btn.style.transform = 'scale(0.9)';
                setTimeout(() => btn.style.transform = '', 100);
            }
        }

        function getRandomSymbol() {
            return symbols[Math.floor(Math.random() * symbols.length)];
        }

        function checkWin(results) {
            const wins = [];
            
            // Check horizontal lines
            for (let row = 0; row < 3; row++) {
                const symbols = [results[0][row], results[1][row], results[2][row]];
                if (symbols[0] === symbols[1] && symbols[1] === symbols[2]) {
                    wins.push({type: 'horizontal', row: row, symbol: symbols[0]});
                }
            }
            
            // Check diagonals
            if (results[0][0] === results[1][1] && results[1][1] === results[2][2]) {
                wins.push({type: 'diagonal', direction: 'TL-BR', symbol: results[0][0]});
            }
            if (results[0][2] === results[1][1] && results[1][1] === results[2][0]) {
                wins.push({type: 'diagonal', direction: 'TR-BL', symbol: results[0][2]});
            }
            
            return wins;
        }

        function calculatePayout(wins) {
            if (wins.length === 0) return 0;
            
            let totalPayout = 0;
            wins.forEach(win => {
                const basePayout = payouts[win.symbol] || 50;
                const multiplier = win.type === 'diagonal' ? 2 : 1;
                totalPayout += basePayout * multiplier;
            });
            
            return totalPayout;
        }

        function showWinMessage(wins, payout) {
            const winMessageEl = document.getElementById('winMessage');
            if (wins.length > 0) {
                winMessageEl.textContent = `🎉 WINNER! 🎉 You won $${payout}!`;
                winMessageEl.className = 'win-message win show';
                
                setTimeout(() => {
                    let details = wins.map(win => {
                        if (win.type === 'horizontal') {
                            return `${win.symbol} ${win.symbol} ${win.symbol} - Line ${win.row + 1}`;
                        } else {
                            return `${win.symbol} ${win.symbol} ${win.symbol} - Diagonal`;
                        }
                    }).join('\\n');
                    
                    alert(`🎉 CONGRATULATIONS! 🎉\\n\\nYou won $${payout}!\\n\\nWinning combinations:\\n${details}`);
                }, 500);
            } else {
                winMessageEl.textContent = '😔 No win this time. Try again!';
                winMessageEl.className = 'win-message lose show';
            }
            
            setTimeout(() => {
                winMessageEl.className = 'win-message';
            }, 3000);
        }

        async function spin() {
            if (isSpinning || balance < bet) {
                if (balance < bet) {
                    alert('❌ Not enough balance to place this bet!');
                }
                return;
            }

            isSpinning = true;
            balance -= bet;
            updateDisplay();
            
            const spinBtn = document.getElementById('spinBtn');
            spinBtn.disabled = true;
            spinBtn.textContent = '🎰 SPINNING... 🎰';
            
            const winMessageEl = document.getElementById('winMessage');
            winMessageEl.className = 'win-message';
            
            const spinDuration = 2500;
            const frameDuration = 20;
            const totalFrames = spinDuration / frameDuration;
            
            const reels = [
                document.getElementById('reel1'),
                document.getElementById('reel2'),
                document.getElementById('reel3')
            ];
            
            reels.forEach(reel => reel.classList.add('spinning'));
            
            const animationFrames = [];
            for (let frame = 0; frame < totalFrames; frame++) {
                const frameSymbols = [];
                for (let reel = 0; reel < 3; reel++) {
                    const reelSymbols = [];
                    for (let symbol = 0; symbol < 8; symbol++) {
                        reelSymbols.push(getRandomSymbol());
                    }
                    frameSymbols.push(reelSymbols);
                }
                animationFrames.push(frameSymbols);
            }
            
            for (let frame = 0; frame < totalFrames; frame++) {
                reels.forEach((reel, reelIndex) => {
                    const symbolsContainer = reel.querySelector('.reel-symbols');
                    if (symbolsContainer) {
                        const symbols = symbolsContainer.children;
                        const frameSymbols = animationFrames[frame][reelIndex];
                        for (let i = 0; i < symbols.length; i++) {
                            symbols[i].textContent = frameSymbols[i];
                        }
                    }
                });
                
                const progress = frame / totalFrames;
                const delay = frameDuration + (progress * progress * 100);
                await new Promise(resolve => setTimeout(resolve, delay));
            }
            
            reels.forEach(reel => reel.classList.remove('spinning'));
            
            let finalResults;
            
            if (window.forceNextWin) {
                const winningSymbol = getRandomSymbol();
                finalResults = [
                    [winningSymbol, winningSymbol, winningSymbol],
                    [winningSymbol, winningSymbol, winningSymbol],
                    [winningSymbol, winningSymbol, winningSymbol]
                ];
                window.forceNextWin = false;
            } else if (window.forceNextLose) {
                finalResults = [
                    [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()],
                    [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()],
                    [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()]
                ];
                while (checkWin(finalResults).length > 0) {
                    finalResults = [
                        [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()],
                        [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()],
                        [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()]
                    ];
                }
                window.forceNextLose = false;
            } else {
                const shouldWin = Math.random() * 100 < customWinRate;
                
                if (shouldWin) {
                    const winningSymbol = getRandomSymbol();
                    const winType = Math.random() < 0.7 ? 'horizontal' : 'diagonal';
                    
                    if (winType === 'horizontal') {
                        const row = Math.floor(Math.random() * 3);
                        finalResults = [
                            [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()],
                            [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()],
                            [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()]
                        ];
                        finalResults[0][row] = winningSymbol;
                        finalResults[1][row] = winningSymbol;
                        finalResults[2][row] = winningSymbol;
                    } else {
                        finalResults = [
                            [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()],
                            [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()],
                            [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()]
                        ];
                        if (Math.random() < 0.5) {
                            finalResults[0][0] = winningSymbol;
                            finalResults[1][1] = winningSymbol;
                            finalResults[2][2] = winningSymbol;
                        } else {
                            finalResults[0][2] = winningSymbol;
                            finalResults[1][1] = winningSymbol;
                            finalResults[2][0] = winningSymbol;
                        }
                    }
                } else {
                    finalResults = [
                        [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()],
                        [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()],
                        [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()]
                    ];
                }
            }
            
            for (let i = 0; i < 3; i++) {
                const symbolsContainer = reels[i].querySelector('.reel-symbols');
                if (symbolsContainer) {
                    const symbols = symbolsContainer.children;
                    for (let j = 0; j < 3; j++) {
                        symbols[j].textContent = finalResults[i][j];
                    }
                }
            }
            
            const wins = checkWin(finalResults);
            const payout = calculatePayout(wins);
            balance += payout;
            
            totalSpins++;
            if (wins.length > 0) {
                totalWins++;
                totalWon += payout;
            } else {
                totalLosses++;
                totalLost += bet;
            }
            
            addToHistory(wins, payout, bet);
            showWinMessage(wins, payout);
            
            spinBtn.disabled = false;
            spinBtn.textContent = '🎰 SPIN! 🎰';
            
            isSpinning = false;
            updateDisplay();
            saveUserData();
        }

        function saveUserData() {
            currentUser.balance = balance;
            currentUser.totalSpins = totalSpins;
            currentUser.totalWins = totalWins;
            currentUser.totalLosses = totalLosses;
            currentUser.totalWon = totalWon;
            currentUser.totalLost = totalLost;
            currentUser.gameHistory = gameHistory;
            
            if (currentUser.username !== 'Guest Player') {
                const users = JSON.parse(localStorage.getItem('slotMachineUsers')) || {};
                users[currentUser.username] = currentUser;
                localStorage.setItem('slotMachineUsers', JSON.stringify(users));
                localStorage.setItem('slotMachineCurrentUser', JSON.stringify(currentUser));
            }
        }

        function goHome() {
            saveUserData();
            window.close();
            if (window.opener) {
                window.opener.focus();
            }
        }

        // Initialize when page loads
        window.onload = initGame;
    </script>
</body>
</html>
"""

def create_complete_game():
    """Create the complete slot machine game file"""
    with open('slotmachine_complete.html', 'w', encoding='utf-8') as f:
        f.write(COMPLETE_GAME_HTML)
    
    print("🎰 Complete slot machine created!")
    print("✅ slotmachine_complete.html is now available")
    print("🔐 Admin code: 12345##")
    print("🏠 Update home page to use slotmachine_complete.html")

if __name__ == "__main__":
    create_complete_game() 