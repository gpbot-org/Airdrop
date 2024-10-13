document.addEventListener('DOMContentLoaded', function() {
    const earnCoinBtn = document.getElementById('earn-coin-btn');
    const messageDiv = document.getElementById('message');
    
    if (earnCoinBtn) {
        earnCoinBtn.addEventListener('click', function() {
            fetch('/save_coins', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        document.getElementById('coins').textContent = data.coins;
                        messageDiv.textContent = 'You earned a coin!';
                    } else {
                        messageDiv.textContent = 'Error earning coin.';
                    }
                })
                .catch(error => {
                    messageDiv.textContent = 'Error: ' + error.message;
                });
        });
    }

    const boostForm = document.getElementById('boost-form');
    if (boostForm) {
        boostForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const boostType = document.getElementById('boost-type').value;

            fetch('/buy_boost', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ boost_type: boostType }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    document.getElementById('coins').textContent = data.coins;
                    messageDiv.textContent = 'Boost purchased successfully!';
                } else {
                    messageDiv.textContent = data.message || 'Error purchasing boost.';
                }
            })
            .catch(error => {
                messageDiv.textContent = 'Error: ' + error.message;
            });
        });
    }
});
