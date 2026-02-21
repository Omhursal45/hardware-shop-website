document.addEventListener('DOMContentLoaded', function() {

    if(window.location.hash === '#reviews'){
        const el = document.querySelector('.reviews-section');
        if(el) el.scrollIntoView({behavior: 'smooth'});
    }

    const ratingSelect = document.getElementById('id_rating');
    if(ratingSelect){
        ratingSelect.addEventListener('change', function(){
            
        });
    }
});