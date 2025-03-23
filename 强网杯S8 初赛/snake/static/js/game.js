const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let snake = [];
let food = {};
let score = 0;

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 绘制蛇
    ctx.fillStyle = '#00ff00';
    snake.forEach(segment => {
        ctx.fillRect(segment[0] * 20, segment[1] * 20, 20, 20);
    });
    
    // 绘制食物
    ctx.fillStyle = '#ff0000';
    ctx.fillRect(food.x * 20, food.y * 20, 20, 20);
    
    // 显示分数
    document.getElementById('score').innerText = `Score: ${score}`;
}

function update() {
    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ direction: currentDirection })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'game_over') {
            alert(`Game Over! Your score: ${data.score}`);
            reset_game();
        }else if (data.status === 'win') {
            window.location.href = `${data.url}`;
        }else {
            snake = data.snake;
            food = { x: data.food[0], y: data.food[1] };
            score = data.score;
            draw();
        }
    });
}

let currentDirection = 'RIGHT';

document.addEventListener('keydown', event => {
    switch (event.key) {
        case 'ArrowUp':
            currentDirection = 'UP';
            break;
        case 'ArrowDown':
            currentDirection = 'DOWN';
            break;
        case 'ArrowLeft':
            currentDirection = 'LEFT';
            break;
        case 'ArrowRight':
            currentDirection = 'RIGHT';
            break;
    }
});

function reset_game() {
    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ direction: 'RIGHT' })
    })
    .then(response => response.json())
    .then(data => {
        snake = data.snake;
        food = { x: data.food[0], y: data.food[1] };
        score = data.score;
        draw();
        setInterval(update, 100);
    });
}

// 初始化游戏
reset_game();document.getElementById('usernameForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    
    fetch('/set_username', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `username=${encodeURIComponent(username)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            window.location.href = '/';
        }
    });
});