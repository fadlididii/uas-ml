/**
 * Authentication and Profile Management Utility
 * Handles login state, profile completeness checks, and redirects
 */

class AuthManager {
    constructor() {
        this.API_BASE_URL = 'http://localhost:8000';
        this.TOKEN_KEY = 'access_token';
        this.USER_DATA_KEY = 'user_data';
    }

    /**
     * Get authentication headers with Bearer token
     * @returns {Object} Headers object with Authorization
     */
    getAuthHeaders() {
        const token = this.getToken();
        if (!token) {
            return {};
        }
        return {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };
    }

    /**
     * Get stored access token
     * @returns {string|null} Access token or null if not found
     */
    getToken() {
        return localStorage.getItem(this.TOKEN_KEY);
    }

    /**
     * Store access token
     * @param {string} token - Access token to store
     */
    setToken(token) {
        localStorage.setItem(this.TOKEN_KEY, token);
    }

    /**
     * Get stored user data
     * @returns {Object|null} User data object or null if not found
     */
    getUserData() {
        const userData = localStorage.getItem(this.USER_DATA_KEY);
        return userData ? JSON.parse(userData) : null;
    }

    /**
     * Store user data
     * @param {Object} userData - User data object to store
     */
    setUserData(userData) {
        localStorage.setItem(this.USER_DATA_KEY, JSON.stringify(userData));
    }

    /**
     * Check if user is authenticated
     * @returns {boolean} True if user has valid token
     */
    isAuthenticated() {
        return !!this.getToken();
    }

    /**
     * Clear all authentication data
     */
    logout() {
        localStorage.removeItem(this.TOKEN_KEY);
        localStorage.removeItem(this.USER_DATA_KEY);
    }

    /**
     * Redirect to login page if not authenticated
     */
    requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = '/login';
            return false;
        }
        return true;
    }

    /**
     * Get current user information with profile status
     * @returns {Promise<Object>} User data with profile status
     */
    async getCurrentUser() {
        try {
            const response = await fetch(`${this.API_BASE_URL}/auth/me`, {
                headers: this.getAuthHeaders()
            });

            if (!response.ok) {
                if (response.status === 401) {
                    this.logout();
                    window.location.href = '/login';
                }
                throw new Error('Failed to get user information');
            }

            return await response.json();
        } catch (error) {
            console.error('Error getting current user:', error);
            throw error;
        }
    }

    /**
     * Check profile completeness and redirect if necessary
     * @param {Object} options - Configuration options
     * @param {boolean} options.autoRedirect - Whether to automatically redirect
     * @param {Function} options.onComplete - Callback when profile is complete
     * @param {Function} options.onIncomplete - Callback when profile is incomplete
     * @returns {Promise<Object>} Profile status information
     */
    async checkProfileCompleteness(options = {}) {
        const {
            autoRedirect = true,
            onComplete = null,
            onIncomplete = null
        } = options;

        try {
            const userData = await this.getCurrentUser();
            const profileStatus = userData.profile_status;

            if (profileStatus.is_complete) {
                if (onComplete) {
                    onComplete(profileStatus);
                }
                if (autoRedirect && window.location.pathname === '/edit-profile') {
                    window.location.href = '/welcome';
                }
            } else {
                if (onIncomplete) {
                    onIncomplete(profileStatus);
                }
                if (autoRedirect && window.location.pathname !== '/edit-profile') {
                    window.location.href = '/edit-profile';
                }
            }

            return profileStatus;
        } catch (error) {
            console.error('Error checking profile completeness:', error);
            throw error;
        }
    }

    /**
     * Handle post-login flow with profile completeness check
     * @param {Object} loginResponse - Response from login API
     * @param {Function} onSuccess - Success callback
     * @param {Function} onError - Error callback
     */
    async handlePostLogin(loginResponse, onSuccess = null, onError = null) {
        try {
            // Store authentication data
            this.setToken(loginResponse.token.access_token);
            this.setUserData(loginResponse.user);

            // Check profile completeness
            const userData = await this.getCurrentUser();
            const profileStatus = userData.profile_status;

            const redirectInfo = {
                redirectTo: profileStatus.redirect_to,
                isComplete: profileStatus.is_complete,
                missingFields: profileStatus.missing_fields
            };

            if (onSuccess) {
                onSuccess(redirectInfo);
            }

            // Auto redirect after callback
            setTimeout(() => {
                window.location.href = profileStatus.redirect_to;
            }, 1500);

        } catch (error) {
            console.error('Error in post-login flow:', error);
            if (onError) {
                onError(error);
            }
            // Fallback redirect
            setTimeout(() => {
                window.location.href = '/profile';
            }, 1500);
        }
    }

    /**
     * Initialize auth manager for protected pages
     * Checks authentication and profile completeness
     * @param {Object} options - Configuration options
     */
    async initializeProtectedPage(options = {}) {
        const {
            requireCompleteProfile = false,
            allowedPaths = ['/edit-profile', '/profile']
        } = options;

        // Check authentication
        if (!this.requireAuth()) {
            return;
        }

        try {
            // Check profile completeness
            const profileStatus = await this.checkProfileCompleteness({
                autoRedirect: false
            });

            // If profile is incomplete and current page requires complete profile
            if (!profileStatus.is_complete && requireCompleteProfile) {
                if (!allowedPaths.includes(window.location.pathname)) {
                    window.location.href = '/edit-profile';
                }
            }

            // If profile is complete and user is on edit-profile page
            if (profileStatus.is_complete && window.location.pathname === '/edit-profile') {
                window.location.href = '/welcome';
            }

        } catch (error) {
            console.error('Error initializing protected page:', error);
        }
    }

    /**
     * Get profile completion percentage
     * @returns {Promise<number>} Completion percentage (0-100)
     */
    async getProfileCompletionPercentage() {
        try {
            const userData = await this.getCurrentUser();
            const profileStatus = userData.profile_status;
            
            const totalFields = 3; // first_name, bio, avatar_url
            const missingFields = profileStatus.missing_fields.length;
            const completedFields = totalFields - missingFields;
            
            return Math.round((completedFields / totalFields) * 100);
        } catch (error) {
            console.error('Error calculating profile completion:', error);
            return 0;
        }
    }

    /**
     * Show profile completion status in UI
     * @param {string} containerId - ID of container element
     */
    async displayProfileStatus(containerId) {
        try {
            const container = document.getElementById(containerId);
            if (!container) return;

            const userData = await this.getCurrentUser();
            const profileStatus = userData.profile_status;
            const percentage = await this.getProfileCompletionPercentage();

            const statusHtml = `
                <div class="profile-status">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span>Profile Completion</span>
                        <span class="fw-bold">${percentage}%</span>
                    </div>
                    <div class="progress mb-2">
                        <div class="progress-bar ${percentage === 100 ? 'bg-success' : 'bg-warning'}" 
                             style="width: ${percentage}%"></div>
                    </div>
                    ${!profileStatus.is_complete ? `
                        <small class="text-muted">
                            Missing: ${profileStatus.missing_fields.join(', ')}
                        </small>
                    ` : `
                        <small class="text-success">
                            <i class="fas fa-check-circle"></i> Profile Complete!
                        </small>
                    `}
                </div>
            `;

            container.innerHTML = statusHtml;
        } catch (error) {
            console.error('Error displaying profile status:', error);
        }
    }
}

// Create global instance
const authManager = new AuthManager();

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AuthManager;
}