document.addEventListener("DOMContentLoaded", function() {
    const messages = document.querySelectorAll('.alert');
    if (messages.length > 0) {
        setTimeout(function() {
            messages.forEach(function(message) {
                message.style.transition = "opacity 0.5s ease-out";
                message.style.opacity = 0;
                setTimeout(function() {
                    message.style.display = "none";
                }, 500); // Убираем сообщение после завершения анимации (через 500 мс)
            });
        }, 7000); // Сообщения исчезнут через 7 секунд
    }
});
