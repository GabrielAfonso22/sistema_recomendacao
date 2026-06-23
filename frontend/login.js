// ─────────────────────────────────────────────────────────────────────────────
//  login.js  |  Sonho dos Pés CRM  |  Autenticação Frontend (mock)
// ─────────────────────────────────────────────────────────────────────────────

// Credenciais hardcoded para demonstração do TCC
const VALID_EMAIL    = 'gestor@sonhodospes.com.br';
const VALID_PASSWORD = 'sonho123';

// ── Referências DOM ──────────────────────────────────────────────────────────
const loginForm     = document.getElementById('loginForm');
const emailInput    = document.getElementById('emailInput');
const passwordInput = document.getElementById('passwordInput');
const loginBtn      = document.getElementById('loginBtn');
const errorMessage  = document.getElementById('errorMessage');
const errorText     = document.getElementById('errorText');

// ── Utilitários ──────────────────────────────────────────────────────────────
function showError(message) {
    errorText.textContent = message || 'Credenciais inválidas. Tente novamente.';
    errorMessage.classList.add('visible');

    // Shake animation no card
    const card = document.querySelector('.login-card');
    card.classList.remove('shake');
    // Force reflow para reiniciar a animação
    void card.offsetWidth;
    card.classList.add('shake');

    // Borda vermelha nos inputs
    emailInput.classList.add('input-error');
    passwordInput.classList.add('input-error');
}

function hideError() {
    errorMessage.classList.remove('visible');
    emailInput.classList.remove('input-error');
    passwordInput.classList.remove('input-error');
}

function setLoading(isLoading) {
    if (isLoading) {
        loginBtn.classList.add('loading');
        loginBtn.disabled = true;
    } else {
        loginBtn.classList.remove('loading');
        loginBtn.disabled = false;
    }
}

// ── Handler principal de Login ───────────────────────────────────────────────
async function handleLogin(event) {
    event.preventDefault();

    const email    = emailInput.value.trim();
    const password = passwordInput.value;

    // Limpa erros anteriores
    hideError();

    // Validação básica de campos vazios
    if (!email || !password) {
        showError('Por favor, preencha todos os campos.');
        return;
    }

    // Simula um pequeno delay de rede para parecer real
    setLoading(true);
    await new Promise(resolve => setTimeout(resolve, 700));
    setLoading(false);

    // Validação das credenciais
    if (email === VALID_EMAIL && password === VALID_PASSWORD) {
        // ✅ Autenticação bem-sucedida
        sessionStorage.setItem('auth_token', 'logado');
        sessionStorage.setItem('user_email', email);

        // Feedback visual antes de redirecionar
        loginBtn.classList.remove('loading');
        loginBtn.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
                 style="width:18px;height:18px;" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"/>
            </svg>
            <span class="btn-text">Acesso Permitido!</span>
        `;
        loginBtn.style.background = 'linear-gradient(135deg, #16a34a, #22c55e)';
        loginBtn.style.boxShadow  = '0 4px 15px rgba(22, 163, 74, 0.4)';

        setTimeout(() => {
            window.location.href = '/';
        }, 600);

    } else {
        // ❌ Credenciais incorretas
        showError('Credenciais inválidas. Tente novamente.');
    }
}

// ── Event Listeners ──────────────────────────────────────────────────────────
loginForm.addEventListener('submit', handleLogin);

// Limpa erro ao começar a digitar novamente
emailInput.addEventListener('input', hideError);
passwordInput.addEventListener('input', hideError);

// ── Verificação: se já estiver logado, redireciona direto ────────────────────
(function checkAlreadyLogged() {
    if (sessionStorage.getItem('auth_token') === 'logado') {
        window.location.href = '/';
    }
})();
