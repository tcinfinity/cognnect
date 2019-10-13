$(function () {

  const socket = io();

  socket.on('connect', () => {
    socket.emit('client_connect', 'client: client connected')
  })

  $('form').submit(e => {
    e.preventDefault();
    socket.emit('message', $('#m').val()); // to server
    $('#m').val(''); // clear
    return false;
  });

  socket.on('message', msg => {
    $('#messages').append($('<li>').text(msg));
  })

});