(function() {
  let config = {
    apiUrl: null
  };

  window.serverless_mailer = {
    setup: function(args) {
      config = Object.assign(config, args);
    },

    handleForm: function(formEl, subject, onSuccess = null, onError = null) {
      formEl.addEventListener('submit', (e) => {
        e.preventDefault();
        let content = '';
        const fields = Array.from(formEl.querySelectorAll('input, textarea'));
        fields.forEach(field => content += field.name + ': ' + field.value + "\r\n");
        serverless_mailer.send({
          subject, content
        }, onSuccess, onError);
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
})();
