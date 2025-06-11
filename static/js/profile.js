// Profile Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Profile picture upload functionality
    const profilePictureInput = document.getElementById('profilePictureInput');
    const profileImage = document.getElementById('profileImage');
    const uploadBtn = document.getElementById('uploadBtn');
    const profilePicturePreview = document.getElementById('profilePicturePreview');
    
    // Handle profile picture upload button click
    uploadBtn.addEventListener('click', function() {
        profilePictureInput.click();
    });
    
    // Handle profile picture preview click
    profilePicturePreview.addEventListener('click', function() {
        profilePictureInput.click();
    });
    
    // Handle file selection
    profilePictureInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                profileImage.src = e.target.result;
            };
            
            reader.readAsDataURL(this.files[0]);
        }
    });
    
    // Form submission
    const profileForm = document.getElementById('profileForm');
    
    profileForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        const saveBtn = document.getElementById('saveProfileBtn');
        const originalBtnText = saveBtn.textContent;
        saveBtn.textContent = 'Menyimpan...';
        saveBtn.disabled = true;
        
        try {
            // Get form data
            const formData = new FormData(profileForm);
            
            // Create profile data object
            const profileData = {
                first_name: formData.get('first_name'),
                last_name: formData.get('last_name'),
                bio: formData.get('bio'),
                phone: formData.get('phone'),
                location: formData.get('location'),
                date_of_birth: formData.get('date_of_birth') || null
            };
            
            // Send profile data to API
            const userId = await getCurrentUserId();
            const response = await fetch(`/users/${userId}/profile`, {
                method: 'PUT',
                headers: getAuthHeaders(),
                body: JSON.stringify(profileData)
            });
            
            if (!response.ok) {
                throw new Error('Failed to update profile');
            }
            
            // Handle profile picture upload separately if a file was selected
            if (profilePictureInput.files && profilePictureInput.files[0]) {
                const imageFormData = new FormData();
                imageFormData.append('file', profilePictureInput.files[0]);
                
                const token = localStorage.getItem('access_token');
                const uploadResponse = await fetch(`/users/${userId}/upload-avatar`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    body: imageFormData
                });
                
                if (!uploadResponse.ok) {
                    console.error('Failed to upload profile picture');
                }
            }
            
            // Redirect to welcome page
            window.location.href = '/welcome';
            
        } catch (error) {
            console.error('Error updating profile:', error);
            alert('Terjadi kesalahan saat menyimpan profil. Silakan coba lagi.');
            
            // Reset button
            saveBtn.textContent = originalBtnText;
            saveBtn.disabled = false;
        }
    });
    
    // Function to get authorization headers
    function getAuthHeaders() {
        const token = localStorage.getItem('access_token');
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
    }
    
    // Function to get current user ID
    async function getCurrentUserId() {
        try {
            const token = localStorage.getItem('access_token');
            if (!token) {
                throw new Error('No access token found');
            }
            
            const response = await fetch('/auth/me', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to get user info');
            }
            
            const userData = await response.json();
            return userData.id;
        } catch (error) {
            console.error('Error getting user ID:', error);
            // Redirect to login if token is invalid
            window.location.href = '/login';
            throw error;
        }
    }
    
    // Load user profile data if available
    loadUserProfile();
    
    async function loadUserProfile() {
        try {
            const userId = await getCurrentUserId();
            const token = localStorage.getItem('access_token');
            
            const response = await fetch(`/users/${userId}/profile`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to load profile');
            }
            
            const profileData = await response.json();
            
            // Also load user data to get basic info from registration
            const userResponse = await fetch(`/users/${userId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (userResponse.ok) {
                const userData = await userResponse.json();
                document.getElementById('username').value = userData.email.split('@')[0] || '';
                
                // Fill first name and last name from registration data
                document.getElementById('firstName').value = userData.first_name || '';
                document.getElementById('lastName').value = userData.last_name || '';
                
                // Fill date of birth from registration data
                if (userData.date_of_birth) {
                    const date = new Date(userData.date_of_birth);
                    const formattedDate = date.toISOString().split('T')[0];
                    document.getElementById('dateOfBirth').value = formattedDate;
                }
            }
            
            // Fill form with additional profile data if available
            if (profileData) {
                document.getElementById('bio').value = profileData.bio || '';
                document.getElementById('phone').value = profileData.phone || '';
                document.getElementById('location').value = profileData.location || '';
                
                // Load profile picture if available
                if (profileData.avatar_url) {
                    profileImage.src = profileData.avatar_url;
                }
            }
            
        } catch (error) {
            console.error('Error loading profile:', error);
        }
    }
});