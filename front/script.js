document.addEventListener('DOMContentLoaded', function () {
  const apiUrl = 'http://localhost:8000';  // Substitua pela URL da sua API
  let userId = null;  // Variável para armazenar o ID do usuário logado

  // Função para fazer login
  function loginUser(cpf, password) {
    axios.post(`${apiUrl}/login`, { cpf, password })
      .then(response => {
        console.log('Login bem-sucedido:', response.data);
        userId = response.data.user_id;  // Armazenar o ID do usuário
        // Exibir elementos relevantes para usuário logado
        document.getElementById('loggedInSection').style.display = 'block';
        document.getElementById('loginForm').style.display = 'none';
        // Atualizar a lista de serviços do usuário
        getUserServices();
      })
      .catch(error => {
        console.error('Erro ao fazer login:', error.response.data);
      });
  }

  // Evento de envio para o formulário de login
  document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const cpf = document.getElementById('loginCpf').value;
    const password = document.getElementById('loginPassword').value;
    loginUser(cpf, password);
  });

  // Função para criar um serviço
  function createService(serviceName, value, description) {
    axios.post(`${apiUrl}/services`, { serviceName, value, description, user_id: userId })
      .then(response => {
        console.log('Serviço criado com sucesso:', response.data);
        // Atualizar a lista de serviços do usuário após criar um novo serviço
        getUserServices();
      })
      .catch(error => {
        console.error('Erro ao criar serviço:', error.response.data);
      });
  }

  // Função para obter serviços do usuário
  function getUserServices() {
    axios.get(`${apiUrl}/services?user_id=${userId}`)
      .then(response => {
        console.log('Serviços do usuário:', response.data);
        // Atualizar a interface com os serviços do usuário
        updateServiceList(response.data);
      })
      .catch(error => {
        console.error('Erro ao obter serviços do usuário:', error.response.data);
      });
  }

  // Atualizar a lista de serviços na interface
  function updateServiceList(services) {
    const serviceList = document.getElementById('serviceList');
    serviceList.innerHTML = '';  // Limpar a lista antes de adicionar os novos serviços

    services.forEach(service => {
      const serviceItem = document.createElement('div');
      serviceItem.classList.add('service-item');
      serviceItem.innerHTML = `
        <strong>${service.service_name}</strong> - Valor: ${service.value} - ${service.description}
      `;
      serviceList.appendChild(serviceItem);
    });
  }

  // Exemplo de uso da função para criar um serviço
  document.getElementById('addServiceBtn').addEventListener('click', function () {
    const serviceName = document.getElementById('serviceName').value;
    const value = document.getElementById('serviceValue').value;
    const description = document.getElementById('serviceDescription').value;
    createService(serviceName, value, description);
  });
});
