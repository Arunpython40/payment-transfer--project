function processPayment() {
        
    document.getElementById('spinner').style.display = 'block';
    setTimeout(function() {

        window.location.href = 'success.html';
    }, 30000); 
}