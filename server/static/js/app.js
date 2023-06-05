$(document).ready(function () {
  const ctx = document.getElementById("myChart").getContext("2d");

  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      datasets: [{ label: "Humidity" }],
    },
    options: {
      borderWidth: 3,
      borderColor: ["rgba(255, 99, 132, 1)"],
    },
  });

  const temperatureChart = new Chart(
    document.getElementById("temperatureChart").getContext("2d"),
    {
      type: "line",
      data: {
        datasets: [{ label: "Temperature" }],
      },
      options: {
        borderWidth: 3,
        borderColor: ["rgba(255, 99, 132, 1)"],
      },
    }
  );

  function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
    });
    chart.update();
  }

  function removeFirstData(chart) {
    chart.data.labels.splice(0, 1);
    chart.data.datasets.forEach((dataset) => {
      dataset.data.shift();
    });
  }

  const MAX_DATA_COUNT = 10;
  //connect to the socket server.
  //   var socket = io.connect("http://" + document.domain + ":" + location.port);
  var socket = io.connect();

  //receive details from server
  socket.on("updateHumidity", function (msg) {
    console.log("Received sensorData :: " + msg.date + " :: " + msg.value);

    if (myChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData(myChart);
    }
    addData(myChart, msg.date, msg.value);
  });

  socket.on("updateTemperature", function (msg) {
    console.log("Received data: " + msg.date + " :: " + msg.value);

    if (temperatureChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData(temperatureChart);
    }
    addData(temperatureChart, msg.date, msg.value);
  });
});
