document.addEventListener('DOMContentLoaded', function() {
    const earnCoinBtn = document.getElementById('earn-coin-btn');
    const messageDiv = document.getElementById('message');

    if (earnCoinBtn) {
        earnCoinBtn.addEventListener('click', function() {
            fetch('/', { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        // Update the coins displayed
                        return response.json();
                    } else {
                        throw new Error('Network response was not ok');
                    }
                })
                .then(data => {
                    document.getElementById('coins').textContent = data.coins;
                    messageDiv.textContent = 'You earned a coin!';
                })
                .catch(error => {
                    messageDiv.textContent = 'Error earning coin: ' + error.message;
                });
        });
    }

    const boostForm = document.getElementById('boost-form');
    if (boostForm) {
        boostForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const boostType = document.getElementById('boost-type').value;

            fetch('/boost', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ boost_type: boostType }),
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Network response was not ok');
                }
            })
            .then(data => {
                document.getElementById('coins').textContent = data.coins;
                messageDiv.textContent = 'Boost purchased successfully!';
            })
            .catch(error => {
                messageDiv.textContent = 'Error purchasing boost: ' + error.message;
            });
        });
    }
});
