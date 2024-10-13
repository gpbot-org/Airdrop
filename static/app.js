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

    document.getElementById('boost-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent page reload
        const boostType = document.getElementById('boost-type').value;
    
        fetch('/buy-boost', {
            method: 'POST',
            body: JSON.stringify({ boost_type: boostType }),
            headers: { 'Content-Type': 'application/json' }
        }).then(response => response.json())
        .then(data => {
            // Display the response message and update coin count
            document.getElementById('message').textContent = data.message;
            document.getElementById('coins').textContent = data.coins;
        }).catch(error => {
            // Display error if purchase fails
            document.getElementById('message').textContent = "Error: " + error.message;
        });
    });
    
});
