document.addEventListener('DOMContentLoaded', function() {
    const getStartedBtns = document.querySelectorAll('.btn-primary');
    const loginModal = document.getElementById('loginModal');
    const closeModalBtn = document.getElementById('closeModal');
    const passwordToggle = document.querySelector('.password-toggle');
    const passwordInput = document.getElementById('password');
    const loginForm = document.querySelector('.login-form');
    const registerForm = document.getElementById('registerForm');

    // API Base URL
    const API_BASE = '/auth';

    // Utility functions
    function showMessage(message, type = 'info') {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <span class="toast-message">${message}</span>
                <button class="toast-close">&times;</button>
            </div>
        `;
        
        // Add styles if not exist
        if (!document.querySelector('#toast-styles')) {
            const styles = document.createElement('style');
            styles.id = 'toast-styles';
            styles.textContent = `
                .toast {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    padding: 15px 20px;
                    border-radius: 8px;
                    color: white;
                    font-weight: 500;
                    z-index: 10000;
                    transform: translateX(400px);
                    transition: transform 0.3s ease;
                    max-width: 400px;
                }
                .toast.show { transform: translateX(0); }
                .toast-success { background: #10b981; }
                .toast-error { background: #ef4444; }
                .toast-info { background: #3b82f6; }
                .toast-content { display: flex; justify-content: space-between; align-items: center; }
                .toast-close { background: none; border: none; color: white; font-size: 18px; cursor: pointer; margin-left: 10px; }
            `;
            document.head.appendChild(styles);
        }
        
        document.body.appendChild(toast);
        
        // Show toast
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
        
        // Close button
        toast.querySelector('.toast-close').addEventListener('click', () => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        });
    }

    function setLoading(form, isLoading) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (isLoading) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Loading...';
        } else {
            submitBtn.disabled = false;
            submitBtn.textContent = submitBtn.dataset.originalText || (form.id === 'registerForm' ? 'Create Account' : 'Login');
        }
    }

    // Fungsi untuk membuka modal
    function openLoginModal(e) {
        e.preventDefault();
        if (loginModal) {
            loginModal.classList.remove('hidden');
            setTimeout(() => {
                loginModal.classList.add('show');
            }, 10);
        }
    }

    // Fungsi untuk menutup modal
    function closeLoginModal() {
        if (loginModal) {
            loginModal.classList.remove('show');
            setTimeout(() => {
                loginModal.classList.add('hidden');
            }, 300);
        }
    }

    // Handle Login Form Submission
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(loginForm);
            const loginData = {
                email: formData.get('email'),
                password: formData.get('password')
            };

            setLoading(loginForm, true);

            try {
                const response = await fetch(`${API_BASE}/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(loginData)
                });

                const result = await response.json();

                if (response.ok) {
                    // Store token
                    localStorage.setItem('access_token', result.token.access_token);
                    localStorage.setItem('user_data', JSON.stringify(result.user));
                    
                    showMessage('Login successful! Redirecting...', 'success');
                    
                    // Redirect to welcome page or dashboard
                    setTimeout(() => {
                        window.location.href = '/welcome';
                    }, 1500);
                } else {
                    showMessage(result.detail || 'Login failed. Please try again.', 'error');
                }
            } catch (error) {
                console.error('Login error:', error);
                showMessage('Network error. Please try again.', 'error');
            } finally {
                setLoading(loginForm, false);
            }
        });
    }

    // Handle Register Form Submission
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(registerForm);
            const password = formData.get('password');
            const confirmPassword = formData.get('confirm_password');
            
            // Client-side validation
            if (password !== confirmPassword) {
                showMessage('Passwords do not match', 'error');
                return;
            }
            
            const registerData = {
                email: formData.get('email'),
                password: password,
                first_name: formData.get('first_name'),
                last_name: formData.get('last_name'),
                date_of_birth: formData.get('date_of_birth'),
                gender: formData.get('gender')
            };

            setLoading(registerForm, true);

            try {
                const response = await fetch(`${API_BASE}/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(registerData)
                });

                const result = await response.json();

                if (response.ok) {
                    // Store token
                    localStorage.setItem('access_token', result.token.access_token);
                    localStorage.setItem('user_data', JSON.stringify(result.user));
                    
                    showMessage('Registration successful! Redirecting...', 'success');
                    
                    // Redirect to welcome page or dashboard
                    setTimeout(() => {
                        window.location.href = '/welcome';
                    }, 1500);
                } else {
                    showMessage(result.detail || 'Registration failed. Please try again.', 'error');
                }
            } catch (error) {
                console.error('Registration error:', error);
                showMessage('Network error. Please try again.', 'error');
            } finally {
                setLoading(registerForm, false);
            }
        });
    }

    // Event listeners untuk tombol "Get Started"
    getStartedBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Pastikan hanya tombol yang tidak ada di form register yang membuka modal
            if (!btn.closest('#registerForm')) {
                openLoginModal(e);
            }
        });
    });

    // Tombol close modal
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeLoginModal);
    }

    // Tutup modal saat klik di luar modal
    if (loginModal) {
        loginModal.addEventListener('click', (e) => {
            if (e.target === loginModal) {
                closeLoginModal();
            }
        });
    }

    // Toggle password visibility dalam modal login
    if (passwordToggle && passwordInput) {
        passwordToggle.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
        });
    }

    // Password toggle for register form
    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', (e) => {
            const input = e.target.previousElementSibling;
            if (input) {
                input.type = input.type === 'password' ? 'text' : 'password';
            }
        });
    });

    // Login modal trigger from register page
    const showLoginModalLink = document.getElementById('showLoginModal');
    if (showLoginModalLink) {
        showLoginModalLink.addEventListener('click', (e) => {
            e.preventDefault();
            openLoginModal(e);
        });
    }
});