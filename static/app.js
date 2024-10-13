let points = 0;

function earnPoints() {
    fetch('/earn', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            points += data.points;
            document.getElementById('points').innerText = points;
        })
        .catch(error => console.error('Error:', error));
}
document.addEventListener('DOMContentLoaded', (event) => {
    // Fetch coins from server when user logs in
    fetch('/login')
        .then(response => response.json())
        .then(data => {
            document.getElementById("coin-count").innerText = data.coins;
        });
});
