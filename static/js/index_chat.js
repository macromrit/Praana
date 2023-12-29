jQuery(document).ready(function() {
    // Function to scroll the chatbox to the bottom
    function scrollToBottom() {
        var chatbox = $(".chatbox");
        var chatlist = $(".chatlist");
        var chatlistHeight = chatlist.height();
        var chatboxHeight = chatbox.height();
        
        if (chatlistHeight > chatboxHeight) {
            chatlist.scrollTop(chatlistHeight - chatboxHeight);
        }
    }

    $(".chat-list a").click(function() {
        alert("test");
        $(".chatbox").addClass('showbox');
        
        // Call scrollToBottom to ensure the scroll bar is at the bottom
        scrollToBottom();
        
        return false;
    });

    $(".chat-icon").click(function() {
        $(".chatbox").removeClass('showbox');
    });
});

