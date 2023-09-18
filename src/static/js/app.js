document.getElementById("myForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const formData = new FormData(event.target);

  if (navigator.onLine) {
    // Si hay conexión, envía directamente
    sendFormData(formData);
  } else {
    // Si no hay conexión, almacena en localStorage
    localStorage.setItem(
      "offlineFormData",
      JSON.stringify(Object.fromEntries(formData.entries()))
    );
    alert(
      "Estás sin conexión. Tus datos se han guardado y se enviarán cuando vuelvas a estar en línea."
    );
  }
});

window.addEventListener("online", function () {
  const savedFormData = localStorage.getItem("offlineFormData");
  if (savedFormData) {
    const formData = new FormData();
    const data = JSON.parse(savedFormData);

    for (const key in data) {
      formData.append(key, data[key]);
    }

    sendFormData(formData);
    localStorage.removeItem("offlineFormData"); // Borra la data guardada una vez enviada
  }
});

function sendFormData(formData) {
  fetch("/submit-form", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("response").innerText =
        data.message + " Recibido: " + data.name + ", " + data.email;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
