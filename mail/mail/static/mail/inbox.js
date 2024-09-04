document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#compose-recipients').disabled = false;

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  document.querySelector('#create').addEventListener('click', () => {
    recipient = document.querySelector('#compose-recipients').value;
    subjects = document.querySelector('#compose-subject').value;
    bodys = document.querySelector('#compose-body').value;
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipient,
          subject: subjects,
          body: bodys,
      })
    })
    .then(response => response.json())
    .then(response => {
      console.log(`${response} succesfull`);
      load_mailbox('inbox');
    });
  });
}
function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    emails.forEach(email => {
      const element = document.createElement('div');
      element.classList.add('email');
      element.innerHTML = `
          <h5>${email['sender']}</h5>
          <p>${email['subject']} </p>
        <p id="time">${email['timestamp']}</p>`;
        document.querySelector('#emails-view').append(element);
        element.addEventListener('click', () => {
          fetch(`/emails/${email['id']}`,{cache: "reload"})
          .then(response => response.json())
          .then(email => {
              // Print email
              var archive_button = '';
              if(mailbox != 'sent'){
                var archive;
                if(email['archived'] == false){
                  archive = 'Archive';
                }else if(email['archived'] == true){
                  archive = 'Unarchive';
                }
                archive_button = `<button type="submit" id="archive" class="btn btn-sm btn-outline-primary">${archive}</button>`;
              }
              document.querySelector('#email-view').innerHTML = '';
              document.querySelector('#emails-view').style.display = 'none';
              document.querySelector('#email-view').style.display = 'block';
              const info = document.createElement('div');
              info.classList.add('info');
              info.innerHTML = `<hr>
              <div><b>From: </b>${email['sender']}</div>
              <div><b>To: </b>${email['recipients']}</div>
              <div><b>Subject: </b>${email['subject']}</div>
              <div><b>Timestamp:</b>${email['timestamp']}</div>
              <button type="submit" value="reply" class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
              ${archive_button}
              <hr>
              <p id="body">${email['body']}</p>
              `;
              document.querySelector('#email-view').append(info);
              fetch(`/emails/${email['id']}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read:true
                })
              }).then(() => {
                console.log(`email ${email['id']} read`);
              });
              if(archive_button !== ''){
                document.querySelector('#archive').addEventListener('click', () =>{
                  var arch = document.querySelector('#archive').innerHTML;
                  if(arch === 'Archive'){
                    fetch(`/emails/${email['id']}`,{
                      method: 'PUT',
                      body: JSON.stringify({
                        archived: true
                      })
                    }).then(() => {
                      console.log(`Archived email ${email['id']}`);
                    }).then(() => load_mailbox('inbox'));
                  }else if(arch === 'Unarchive'){
                    fetch(`/emails/${email['id']}`,{
                      method: 'PUT',
                      body: JSON.stringify({
                        archived: false
                      })
                    }).then(() => {
                      console.log(`Unarchived email ${email['id']}`);
                    }).then(() => load_mailbox('inbox'));
                  }
                });
              }
              document.querySelector("#reply").addEventListener('click', () => {
                document.querySelector('#emails-view').style.display = 'none';
                document.querySelector('#email-view').style.display = 'none';
                document.querySelector('#compose-view').style.display = 'block';

                recipient = document.querySelector('#compose-recipients').value = email['sender'];
                document.querySelector('#compose-recipients').disabled = true;
                if(email['subject'].includes('Re:')){
                  subjects = document.querySelector('#compose-subject').value = email['subject'];
                }
                else{
                  subjects = document.querySelector('#compose-subject').value = `Re: ${email['subject']}`;
                }
                bodys = document.querySelector('#compose-body').value = `On ${email['timestamp']} ${email['sender']} wrote: ${email['body']}`;
                document.querySelector('#create').addEventListener('click', () => {
                  recipient = document.querySelector('#compose-recipients').value;
                  subjects = document.querySelector('#compose-subject').value;
                  bodys = document.querySelector('#compose-body').value;
                  fetch('/emails', {
                    method: 'POST',
                    body: JSON.stringify({
                        recipients: recipient,
                        subject: subjects,
                        body: bodys,
                    })
                  })
                  .then(response => response.json())
                  .then(response => {
                    console.log(`${response} succesfull`);
                    load_mailbox('inbox');
                  });
                });
              });
          });
        });
    });
  });
}