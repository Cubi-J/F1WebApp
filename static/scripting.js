document.getElementById('loadDataBtn').addEventListener('click', function() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            // Display data in console or update DOM as needed
            console.log(data);
            document.getElementById('dataContainer').textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});