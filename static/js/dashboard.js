
    lucide.createIcons();

    const hour = new Date().getHours();
    const name = "{{ user.first_name|default:user.username }}";
    const greet = document.getElementById('greet');
    if (hour < 12) greet.innerText = `Good Morning, ${name} 🌅`;
    else if (hour < 18) greet.innerText = `Good Afternoon, ${name} ☀️`;
    else greet.innerText = `Good Evening, ${name} 🌙`;

    document.getElementById('leadSearch').addEventListener('keyup', function() {
        let value = this.value.toLowerCase();
        let rows = document.querySelectorAll('#leadTableBody .lead-row');
        rows.forEach(row => {
            row.style.display = (row.innerText.toLowerCase().includes(value)) ? "" : "none";
        });
    });
