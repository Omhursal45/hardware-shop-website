document.getElementById('enquiryForm').addEventListener('submit', function(e) {
    const btn = document.getElementById('submitBtn');
    const text = btn.querySelector('.btn-text');
    const spinner = btn.querySelector('.spinner');
    
    btn.style.pointerEvents = 'none';
    btn.style.opacity = '0.8';
    text.innerText = 'Sending...';
    spinner.style.display = 'block';
});