function Login(){
    const loginButton = document.getElementById('loginButton');
    const profileContainer = document.getElementById('profileContainer');
  
    loginButton.addEventListener('click', () => {
      loginButton.classList.add('hidden');
      profileContainer.classList.remove('hidden');
    });
}