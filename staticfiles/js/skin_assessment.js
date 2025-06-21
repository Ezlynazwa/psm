document.addEventListener('DOMContentLoaded', function() {
    // Get all form sections
    const formSections = document.querySelectorAll('.form-section');
    const progressBar = document.querySelector('.progress-bar');
    const totalSections = formSections.length;
    let currentSection = 0;
    
    // Initialize form - show first section
    showSection(currentSection);
    updateProgressBar();

    // Next button functionality
    document.querySelectorAll('.btn-next').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const nextSectionId = this.getAttribute('data-next');
            
            // Validate current section before proceeding
            if (validateCurrentSection(currentSection)) {
                // Hide current section
                formSections[currentSection].classList.remove('active');
                
                // Show next section
                const nextSection = document.getElementById(nextSectionId);
                nextSection.classList.add('active');
                
                // Update current section index
                currentSection = Array.from(formSections).findIndex(section => section.id === nextSectionId);
                updateProgressBar();
                
                // Scroll to top of form
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    });

    // Previous button functionality
    document.querySelectorAll('.btn-prev').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const prevSectionId = this.getAttribute('data-prev');
            
            // Hide current section
            formSections[currentSection].classList.remove('active');
            
            // Show previous section
            const prevSection = document.getElementById(prevSectionId);
            prevSection.classList.add('active');
            
            // Update current section index
            currentSection = Array.from(formSections).findIndex(section => section.id === prevSectionId);
            updateProgressBar();
            
            // Scroll to top of form
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });

    // Function to show specific section
    function showSection(index) {
        formSections.forEach((section, i) => {
            if (i === index) {
                section.classList.add('active');
            } else {
                section.classList.remove('active');
            }
        });
    }

    // Function to update progress bar
    function updateProgressBar() {
        const progress = ((currentSection + 1) / totalSections) * 100;
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);
        document.querySelector('.progress-container small').textContent = `Step ${currentSection + 1} of ${totalSections}`;
    }

    // Function to validate current section
    function validateCurrentSection(sectionIndex) {
        const currentSection = formSections[sectionIndex];
        let isValid = true;
        
        // Check if required radio buttons are selected
        const requiredRadios = currentSection.querySelectorAll('input[type="radio"][required]');
        if (requiredRadios.length > 0) {
            const radioGroupNames = new Set();
            requiredRadios.forEach(radio => radioGroupNames.add(radio.name));
            
            radioGroupNames.forEach(name => {
                if (!currentSection.querySelector(`input[name="${name}"]:checked`)) {
                    isValid = false;
                    // Highlight error
                    const radioGroup = currentSection.querySelectorAll(`input[name="${name}"]`);
                    radioGroup.forEach(radio => {
                        radio.parentElement.classList.add('error');
                    });
                }
            });
        }
        
        // Check if at least one concern is selected (if in concerns section)
        if (currentSection.id === 'concerns-section') {
            const checkedConcerns = currentSection.querySelectorAll('input[type="checkbox"]:checked');
            if (checkedConcerns.length === 0) {
                isValid = false;
                currentSection.querySelector('.concerns-grid').classList.add('error');
            }
        }
        
        return isValid;
    }

    // Remove error class when user interacts
    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('change', function() {
            if (this.type === 'radio') {
                document.querySelectorAll(`input[name="${this.name}"]`).forEach(radio => {
                    radio.parentElement.classList.remove('error');
                });
            } else if (this.type === 'checkbox' && this.closest('#concerns-section')) {
                this.closest('.concerns-grid').classList.remove('error');
            }
        });
    });
});