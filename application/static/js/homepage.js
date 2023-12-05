console.log('sup');

document
  .getElementById('searchButton')
  .addEventListener('click', redirectToSearch);

function redirectToSearch() {
  window.location.href = '/search';
}
