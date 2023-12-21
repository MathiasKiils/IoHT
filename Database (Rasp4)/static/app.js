document.addEventListener('DOMContentLoaded', function () {

    // Function to fetch and update data
    function fetchDataAndUpdate(deviceId) {
        fetch(`/api/device/${deviceId}/latest_data`)
        .then(response => response.json())
        .then(data => {
            console.log(`Latest data for Device ${deviceId}:`, data.latest_temp[0],data.latest_co2[0], data.latest_fugt[0]);
            updateTemp(deviceId, data.latest_temp[0]);
            updateCO2(deviceId, data.latest_co2[0]);
            updateFugt(deviceId, data.latest_fugt[0]);
        })
        .catch(error => console.error(`Error fetching data for Device ${deviceId}:`, error));
    }

    // Set up automatic updates every 5 seconds
    setInterval(() => {
        if (currentPage === 'device1') {
            fetchDataAndUpdate(1);
        } else if (currentPage === 'device2') {
            fetchDataAndUpdate(2);
        } else if (currentPage === 'device3') {
            fetchDataAndUpdate(3);
        }
    }, 5000);
});

function updateTemp(deviceId, tempValue) {
    const tempDiv = document.getElementById(`temp${deviceId}`);

    tempDiv.textContent = tempValue;
}

function updateCO2(deviceId, co2Value) {
    const co2Div = document.getElementById(`co2${deviceId}`);

    co2Div.textContent = co2Value;
}

function updateFugt(deviceId, fugtValue) {
    const fugtDiv = document.getElementById(`fugt${deviceId}`);

    fugtDiv.textContent = fugtValue;
}
