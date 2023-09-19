/* eslint-env browser */
/* eslint-env jquery */

window.addEventListener('online', function () {
  const savedFormData = localStorage.getItem('offlineFormData')
  if (savedFormData) {
    const formData = new FormData()
    const data = JSON.parse(savedFormData)

    for (const key in data) {
      formData.append(key, data[key])
    }

    sendFormData(formData)
    // remove saved data from localStorage
    localStorage.removeItem('offlineFormData')
  }
})

$(document).ready(function () {
  $('#dateField').datepicker({
    format: 'dd/mm/yyyy',
    language: 'es'
  })
})

function createCard (data) {
  // create card elements
  const card = document.createElement('div')
  card.className = 'card mb-3'

  const cardBody = document.createElement('div')
  cardBody.className = 'card-body'

  const cardTitle = document.createElement('h5')
  cardTitle.className = 'card-title'
  cardTitle.innerText = data.note

  const cardTextTotal = document.createElement('p')
  cardTextTotal.className = 'card-text'
  cardTextTotal.innerText = 'Total: $' + data.total

  const cardTextDate = document.createElement('p')
  cardTextDate.className = 'card-text'

  const smallText = document.createElement('small')
  smallText.className = 'text-muted'
  smallText.innerText = 'Fecha: ' + data.date

  // add elements to the card
  cardTextDate.appendChild(smallText)
  cardBody.appendChild(cardTitle)
  cardBody.appendChild(cardTextTotal)
  cardBody.appendChild(cardTextDate)
  card.appendChild(cardBody)

  return card
}

function sendFormData (formData) {
  fetch('/submit-form', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      const cardContainer = document.querySelector('.card-container')
      const newCard = createCard(data)
      if (cardContainer.firstChild) {
        cardContainer.insertBefore(newCard, cardContainer.firstChild)
      } else {
        cardContainer.appendChild(newCard)
      }
    })
    .catch(error => {
      console.error('Error:', error)
    })
}

// eslint-disable-next-line no-unused-vars
function submitForm (type) {
  // Set the operation type in the form
  document.getElementById('operationType').value = type

  const formData = new FormData(document.getElementById('myForm'))

  if (navigator.onLine) {
    // if have connection, send directly
    sendFormData(formData)
  } else {
    // if no connection, store in localStorage
    localStorage.setItem(
      'offlineFormData',
      JSON.stringify(Object.fromEntries(formData.entries()))
    )
    alert(
      'Estás sin conexión. Tus datos se han guardado y se enviarán cuando vuelvas a estar en línea.'
    )
  }
}
