(function() {
  let config = {
    apiUrl: null
  };

  window.serverless_mailer = {
    setup: function(args) {
      config = Object.assign(config, args);
    },

    handleForm: function(formEl, subject = 'Form Message', onSuccess = null, onError = null) {
      formEl.addEventListener('submit', (e) => {
        const data = { subject };

        e.preventDefault();
        let content = '';
        const fields = Array.from(formEl.querySelectorAll('input, textarea'));
        fields.forEach(field => {
          data[field.name] = field.value;
          content += field.name + ': ' + field.value + "\r\n";
        });

        data['content'] = content;

        serverless_mailer.send(data, onSuccess, onError);
      });
    },

    send: async function(data, onSuccess = null, onError = null) {
      if(config.apiUrl === null) throw 'No API URL configured';
      try {
        const response = await fetch(config.apiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });
        if(response.status !== 200) {
          if(onError !== null) onError(await response.json())
        } else {
          if(onSuccess !== null) onSuccess();
        }
      } catch(e) {
        if(onError !== null) onError(e.message);
      }
    }
  };

  const apiMeta = document.querySelector('meta[name=serverless-api-url]');
  if(apiMeta !== null) {
    serverless_mailer.setup({apiUrl: apiMeta.content});
  }
  const forms = Array.from(document.querySelectorAll('form.serverless_mailer'));
  forms.forEach(form => {
    let onSuccess = null;
    let onFail = null;
    if('successMsg' in form.dataset) onSuccess = () => alert(form.dataset.successMsg);
    if('failMsg' in form.dataset) onFail = () => alert(form.dataset.failMsg);
    serverless_mailer.handleForm(form, null, onSuccess, onFail);
  });
})();
