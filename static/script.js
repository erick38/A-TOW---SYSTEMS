// Get the conversation links
var conversationLinks = document.querySelectorAll('ul li a');

// Add a click event listener to each conversation link
for (var i = 0; i < conversationLinks.length; i++) {
  conversationLinks[i].addEventListener('click', function(event) {
    event.preventDefault();
    // Get the conversation ID from the link's href attribute
    var conversationId = this.getAttribute('href').split('=')[1];
    // Make an AJAX request to get the conversation messages
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        // Replace the messages with the new messages
        var messagesContainer = document.querySelector('ul.messages');
        messagesContainer.innerHTML = xhr.responseText;
      }
    };
    xhr.open('GET', '/messages/?conversation_id=' + conversationId);
    xhr.send();
  });
}
