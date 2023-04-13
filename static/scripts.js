const form = document.querySelector('#search-form');
const input = document.querySelector('#search-input');
const spinner = document.querySelector('#loading-spinner');
const results = document.querySelector('#search-results');

form.addEventListener('submit', event => {
  event.preventDefault();

  const query = input.value.trim();

  if (query === '') {
    return;
  }

  showSpinner();

  fetch('/tools', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query })
  })
    .then(response => response.json())
    .then(data => {
      hideSpinner();
      addResult(query, data.summary);
    })
    .catch(error => {
      console.error(error);
      hideSpinner();
      showError();
    });

  input.value = '';
});

function showSpinner() {
  spinner.style.display = 'block';
}

function hideSpinner() {
  spinner.style.display = 'none';
}

function addResult(query, summary) {
  const question = document.createElement('b');
  question.textContent = query;

  const answer = document.createElement('p');
  answer.textContent = summary.trim();

  const result = document.createElement('div');
  result.appendChild(question);
  result.appendChild(answer);

  results.appendChild(result);
  results.style.display = 'block';
}

function showError() {
  alert('An error occurred while retrieving the data.');
}
