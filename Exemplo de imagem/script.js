document.getElementById('calcForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const response = await fetch('http://localhost:5000/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            width: 30,
            height: 45,
            agressClass: 2,
            quantBar: 10,
            dBar: 1.25,
            dAgreg: 2.5,
            dEstribo: 0.5,
            av: 2
        })
    });

    const result = await response.json();

    if (response.ok) {
        document.getElementById('areaValue').textContent = result.calc_area;  // Update to access calc_area from JSON
        document.getElementById('resultImage').src = result.image_path;  // Update to access image_path from JSON
        document.getElementById('result').style.display = 'block';
    } else {
        alert('Error: ' + result[0]);
    }
});
