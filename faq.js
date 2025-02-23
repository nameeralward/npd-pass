document.addEventListener('DOMContentLoaded', function() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    // Set first item as active by default
    faqItems[0].classList.add('active');
    
    faqItems.forEach(item => {
        const header = item.querySelector('h3');
        header.addEventListener('click', () => {
            // Toggle active state
            item.classList.toggle('active');
        });
    });
}); 