import http.server
import socketserver
import webbrowser
import os
import threading
import time

# HTML content for the slot machine
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎰 Lucky Slot Machine 🎰</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #2C3E50, #34495E);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }

        .main-container {
            display: flex;
            gap: 30px;
            max-width: 1200px;
            width: 100%;
            margin: 0 auto;
        }

        .game-panel {
            background: rgba(52, 73, 94, 0.9);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            text-align: center;
            flex: 1;
            min-width: 500px;
        }

        .history-panel {
            background: rgba(52, 73, 94, 0.9);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            flex: 1;
            min-width: 400px;
            max-height: 600px;
            overflow-y: auto;
        }

        .title {
            font-size: 2.5em;
            margin-bottom: 30px;
            color: #F39C12;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }

        .info-panel {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
            gap: 20px;
        }

        .balance, .bet {
            flex: 1;
            padding: 15px;
            border-radius: 10px;
            font-size: 1.2em;
            font-weight: bold;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }

        .balance {
            background: linear-gradient(45deg, #27AE60, #2ECC71);
        }

        .bet {
            background: linear-gradient(45deg, #E74C3C, #C0392B);
        }

        .slot-machine {
            background: #34495E;
            border: 5px solid #F39C12;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
        }

        .reels {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }

        .reel-container {
            background: #2C3E50;
            border: 3px solid #F39C12;
            border-radius: 10px;
            padding: 5px;
            min-height: 120px;
            position: relative;
            overflow: hidden;
            box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3);
        }

        .reel {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-size: 2.5em;
            min-height: 120px;
            transition: all 0.3s ease;
        }

        .reel.spinning {
            animation: slotSpin 0.02s linear infinite;
        }

        @keyframes slotSpin {
            0% { transform: translateY(0px); }
            100% { transform: translateY(-40px); }
        }

        .reel-symbols {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
            transition: transform 0.02s linear;
        }

        .reel-window {
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 40px;
            transform: translateY(-50%);
            background: linear-gradient(
                to bottom,
                transparent 0%,
                rgba(52, 73, 94, 0.8) 20%,
                rgba(52, 73, 94, 0.8) 80%,
                transparent 100%
            );
            pointer-events: none;
            z-index: 2;
        }

        .reel-symbols {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
        }

        .controls {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
        }

        .spin-btn {
            background: linear-gradient(45deg, #E74C3C, #C0392B);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 1.3em;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }

        .spin-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        }

        .spin-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .bet-controls {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .bet-btn {
            background: #95A5A6;
            color: white;
            border: none;
            width: 40px;
            height: 40px;
            font-size: 1.2em;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .bet-btn:hover {
            background: #7F8C8D;
            transform: scale(1.1);
        }

        .bet-amount {
            font-size: 1.2em;
            font-weight: bold;
            color: #F39C12;
            min-width: 60px;
        }

        .win-message {
            font-size: 1.5em;
            font-weight: bold;
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            opacity: 0;
            transition: opacity 0.5s ease;
        }

        .win-message.show {
            opacity: 1;
        }

        .win {
            background: linear-gradient(45deg, #27AE60, #2ECC71);
            color: white;
        }

        .lose {
            background: linear-gradient(45deg, #E74C3C, #C0392B);
            color: white;
        }

        .paytable {
            background: rgba(52, 73, 94, 0.8);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            font-size: 0.9em;
        }

        .paytable h3 {
            color: #F39C12;
            margin-bottom: 10px;
        }

        .paytable-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 5px;
        }

        .paytable-item {
            display: flex;
            justify-content: space-between;
            padding: 2px 0;
        }

        .history-title {
            color: #F39C12;
            font-size: 1.5em;
            margin-bottom: 20px;
            text-align: center;
        }

        .history-item {
            background: rgba(44, 62, 80, 0.8);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #F39C12;
            transition: all 0.3s ease;
        }

        .history-item:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }

        .history-item.win {
            border-left-color: #27AE60;
        }

        .history-item.lose {
            border-left-color: #E74C3C;
        }

        .history-time {
            font-size: 0.8em;
            color: #BDC3C7;
            margin-bottom: 5px;
        }

        .history-result {
            font-weight: bold;
            margin-bottom: 5px;
        }

        .history-details {
            font-size: 0.9em;
            color: #ECF0F1;
        }

        .stats {
            background: rgba(44, 62, 80, 0.8);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }

        .stats h3 {
            color: #F39C12;
            margin-bottom: 10px;
            text-align: center;
        }

        .stat-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }

        .clear-history-btn {
            background: linear-gradient(45deg, #E74C3C, #C0392B);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 10px;
            transition: all 0.3s ease;
        }

        .clear-history-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }

        .odds-panel {
            background: rgba(44, 62, 80, 0.8);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }

        .odds-panel h3 {
            color: #F39C12;
            margin-bottom: 10px;
            text-align: center;
        }

        .odds-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            padding: 5px 0;
            border-bottom: 1px solid rgba(189, 195, 199, 0.2);
        }

        .odds-symbol {
            font-size: 1.2em;
        }

        .odds-probability {
            color: #F39C12;
            font-weight: bold;
        }

        .odds-payout {
            color: #27AE60;
            font-weight: bold;
        }

        @media (max-width: 1000px) {
            .main-container {
                flex-direction: column;
                gap: 20px;
            }
            
            .game-panel, .history-panel {
                min-width: auto;
            }
        }

        @media (max-width: 600px) {
            .main-container {
                margin: 20px;
            }
            
            .title {
                font-size: 2em;
            }
            
            .info-panel {
                flex-direction: column;
            }
            
            .reel {
                font-size: 2em;
                min-height: 80px;
            }
        }
    </style>
</head>
<body>
    <div class="main-container">
        <!-- Game Panel (Left Side) -->
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
                                <div>🎰</div>
                                <div>🎰</div>
                                <div>🎰</div>
                                <div>🎰</div>
                                <div>🎰</div>
                            </div>
                        </div>
                        <div class="reel-window"></div>
                    </div>
                    <div class="reel-container">
                        <div class="reel" id="reel2">
                            <div class="reel-symbols">
                                <div>🎰</div>
                                <div>🎰</div>
                                <div>🎰</div>
                                <div>🎰</div>
                                <div>🎰</div>
                            </div>
                        </div>
                        <div class="reel-window"></div>
                    </div>
                    <div class="reel-container">
                        <div class="reel" id="reel3">
                            <div class="reel-symbols">
                                <div>🎰</div>
                                <div>🎰</div>
                                <div>🎰</div>
                                <div>🎰</div>
                                <div>🎰</div>
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
                <p style="margin-top: 10px; font-size: 0.8em; color: #BDC3C7;">
                    Diagonals pay double! 🎯
                </p>
            </div>
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
        const symbols = ['🍒', '🍊', '🍋', '💎', '7️⃣', '🎰', '🍀', '⭐'];
        const payouts = {
            '🍒': 50, '🍊': 100, '🍋': 150, '💎': 200,
            '7️⃣': 500, '🎰': 1000, '🍀': 750, '⭐': 300
        };

        // History tracking
        let gameHistory = [];
        let totalSpins = 0;
        let totalWins = 0;
        let totalLosses = 0;
        let totalWon = 0;
        let totalLost = 0;

        // DOM elements
        const balanceEl = document.getElementById('balance');
        const betEl = document.getElementById('bet');
        const betAmountEl = document.getElementById('betAmount');
        const spinBtn = document.getElementById('spinBtn');
        const winMessageEl = document.getElementById('winMessage');
        const historyListEl = document.getElementById('historyList');
        const reels = [
            document.getElementById('reel1'),
            document.getElementById('reel2'),
            document.getElementById('reel3')
        ];

        function updateDisplay() {
            balanceEl.textContent = `💰 Balance: $${balance}`;
            betEl.textContent = `🎯 Bet: $${bet}`;
            betAmountEl.textContent = `$${bet}`;
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
            
            gameHistory.unshift(historyItem); // Add to beginning
            if (gameHistory.length > 50) { // Keep only last 50 entries
                gameHistory.pop();
            }
            
            updateHistoryDisplay();
        }

        function updateHistoryDisplay() {
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
                totalSpins = 0;
                totalWins = 0;
                totalLosses = 0;
                totalWon = 0;
                totalLost = 0;
                updateStats();
                updateHistoryDisplay();
            }
        }

        function changeBet(amount) {
            if (isSpinning) return;
            
            const newBet = bet + amount;
            if (newBet >= 10 && newBet <= 100 && newBet <= balance) {
                bet = newBet;
                updateDisplay();
                
                // Animate button
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
            if (wins.length > 0) {
                winMessageEl.textContent = `🎉 WINNER! 🎉 You won $${payout}!`;
                winMessageEl.className = 'win-message win show';
                
                // Show detailed win info
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
            
            // Disable spin button
            spinBtn.disabled = true;
            spinBtn.textContent = '🎰 SPINNING... 🎰';
            
            // Clear win message
            winMessageEl.className = 'win-message';
            
            // Start spinning animation
            const spinDuration = 2000; // 2 seconds
            const frameDuration = 50; // 50ms per frame for smoother animation
            const totalFrames = spinDuration / frameDuration;
            
            // Add spinning class to reels
            reels.forEach(reel => reel.classList.add('spinning'));
            
            for (let frame = 0; frame < totalFrames; frame++) {
                // Update reels with random symbols in a scrolling pattern
                reels.forEach((reel, reelIndex) => {
                    const symbolsContainer = reel.querySelector('.reel-symbols');
                    if (symbolsContainer) {
                        // Create a scrolling effect by updating symbols
                        const symbols = symbolsContainer.children;
                        for (let i = 0; i < symbols.length; i++) {
                            symbols[i].textContent = getRandomSymbol();
                        }
                    }
                });
                
                // Slow down animation towards the end
                const delay = frameDuration + (frame * 15);
                await new Promise(resolve => setTimeout(resolve, delay));
            }
            
            // Stop spinning animation
            reels.forEach(reel => reel.classList.remove('spinning'));
            
            // Generate final result
            const finalResults = [
                [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()],
                [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()],
                [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()]
            ];
            
            // Display final result
            for (let i = 0; i < 3; i++) {
                const symbolsContainer = reels[i].querySelector('.reel-symbols');
                if (symbolsContainer) {
                    const symbols = symbolsContainer.children;
                    for (let j = 0; j < 3; j++) {
                        symbols[j].textContent = finalResults[i][j];
                    }
                }
            }
            
            // Check for wins
            const wins = checkWin(finalResults);
            const payout = calculatePayout(wins);
            balance += payout;
            
            // Update statistics
            totalSpins++;
            if (wins.length > 0) {
                totalWins++;
                totalWon += payout;
            } else {
                totalLosses++;
                totalLost += bet;
            }
            
            // Add to history
            addToHistory(wins, payout, bet);
            
            // Show results
            showWinMessage(wins, payout);
            
            // Re-enable spin button
            spinBtn.disabled = false;
            spinBtn.textContent = '🎰 SPIN! 🎰';
            
            isSpinning = false;
            updateDisplay();
        }

        // Initialize display
        updateDisplay();
    </script>
</body>
</html>
"""

def create_html_file():
    """Create the HTML file for the slot machine"""
    with open('slotmachine.html', 'w', encoding='utf-8') as f:
        f.write(HTML_CONTENT)
    print("🎰 Slot machine HTML file created!")

def start_server():
    """Start a local web server to serve the slot machine"""
    PORT = 8000
    
    # Create HTML file
    create_html_file()
    
    # Change to the directory containing the HTML file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Start server
    try:
        with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"🎰 Slot machine server starting on http://localhost:{PORT}")
            print("🌐 Opening slot machine in your browser...")
            
            # Open browser after a short delay
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{PORT}/slotmachine.html')
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n🎰 Server stopped. Thanks for playing!")
                # Clean up HTML file
                try:
                    os.remove('slotmachine.html')
                    print("🧹 Cleaned up temporary files.")
                except:
                    pass
    except OSError:
        # Try alternative port
        PORT = 8080
        print(f"Port 8000 busy, trying port {PORT}...")
        with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"🎰 Slot machine server starting on http://localhost:{PORT}")
            print("🌐 Opening slot machine in your browser...")
            
            # Open browser after a short delay
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{PORT}/slotmachine.html')
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n🎰 Server stopped. Thanks for playing!")
                # Clean up HTML file
                try:
                    os.remove('slotmachine.html')
                    print("🧹 Cleaned up temporary files.")
                except:
                    pass

if __name__ == "__main__":
    start_server()
