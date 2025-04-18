// Interactive features for ADCortex documentation

document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add copy button functionality
    document.querySelectorAll('.highlight').forEach(block => {
        const button = document.createElement('button');
        button.className = 'copybtn';
        button.textContent = 'Copy';
        button.addEventListener('click', () => {
            const code = block.querySelector('code').textContent;
            navigator.clipboard.writeText(code).then(() => {
                button.textContent = 'Copied!';
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 2000);
            });
        });
        block.appendChild(button);
    });

    // Add collapsible sections for long code examples
    document.querySelectorAll('.highlight').forEach(block => {
        if (block.scrollHeight > 300) {
            const button = document.createElement('button');
            button.className = 'collapsebtn';
            button.textContent = 'Show more';
            button.addEventListener('click', () => {
                block.classList.toggle('expanded');
                button.textContent = block.classList.contains('expanded') ? 'Show less' : 'Show more';
            });
            block.parentNode.insertBefore(button, block.nextSibling);
        }
    });

    // Add search functionality
    const searchInput = document.querySelector('.search input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            document.querySelectorAll('.section').forEach(section => {
                const text = section.textContent.toLowerCase();
                section.style.display = text.includes(searchTerm) ? 'block' : 'none';
            });
        });
    }
}); 