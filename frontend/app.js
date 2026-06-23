// ─── Guarda de Autenticação ─────────────────────────────────────────────────
// Redireciona imediatamente para o login se não houver sessão válida.
(function authGuard() {
    if (sessionStorage.getItem('auth_token') !== 'logado') {
        window.location.replace('/login.html');
    }
})();

const skuInput = document.getElementById('skuInput');
const searchBtn = document.getElementById('searchBtn');
const container = document.getElementById('recommendationsContainer');
const targetSection = document.getElementById('targetProductSection');
const recommendationsHeader = document.getElementById('recommendationsHeader');
const recommendationsTitle = document.getElementById('recommendationsTitle');
const campaignBtn = document.getElementById('campaignBtn');
const toast = document.getElementById('toast');

let currentProductKey = null;

const FALLBACK_IMAGE = 'https://storage.googleapis.com/ss-reports-bi/default/sem_foto.png';

async function fetchRecommendations() {
    const sku = skuInput.value.trim();
    if (!sku) return;

    // Loading state
    container.innerHTML = '<div class="empty-state"><div class="loader"></div><p>Buscando conexões...</p></div>';
    targetSection.style.display = 'none';
    if(recommendationsHeader) recommendationsHeader.style.display = 'none';
    recommendationsTitle.style.display = 'none';
    if(campaignBtn) campaignBtn.style.display = 'none';

    try {
        const response = await fetch(`/api/recommend/${sku}`);
        const data = await response.json();

        renderResults(data);
    } catch (error) {
        console.error('Erro ao buscar recomendações:', error);
        container.innerHTML = '<div class="empty-state"><p>Ocorreu um erro na conexão com o servidor.</p></div>';
    }
}

function renderResults(data) {
    const { target_product, recommendations, vendas_totais_tickets } = data;

    currentProductKey = data.product_key || (target_product ? target_product.PRODUTO_SKU : null);

    // Renderizar produto pesquisado
    if (target_product) {
        const productName = target_product.PRODUTO_NOME || 'Produto sem Nome';
        targetSection.innerHTML = `
            <div class="target-card">
                <div class="target-badge">Produto Pesquisado</div>
                <div class="target-content">
                    <img src="${target_product.LINK_FOTO || FALLBACK_IMAGE}" 
                         alt="${target_product.PRODUTO_SKU}"
                         onerror="this.onerror=null;this.src='${FALLBACK_IMAGE}'">
                    <div class="target-info">
                        <h2>${productName}</h2>
                        <span class="sku-badge">${data.product_key || target_product.PRODUTO_SKU}</span>
                        
                        <div class="target-meta">
                            <div class="target-meta-item">
                                <span class="target-meta-label">Cor</span>
                                <span class="target-meta-value">${target_product.PRODUTO_COR || 'N/A'}</span>
                            </div>
                        </div>

                        <div class="target-meta-item" style="margin-bottom: 1rem;">
                            <span class="target-meta-label">Preço</span>
                            <div class="target-price">${target_product.PRODUTO_PRECO || ''}</div>
                        </div>
                        
                        <div class="xai-badge magenta">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"></path><path d="M3 6h18"></path><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
                            ${vendas_totais_tickets.toLocaleString('pt-BR')} unidades vendidas
                        </div>

                        <p style="margin-top: 1rem;">Exibindo associações inteligentes para este item.</p>
                    </div>
                </div>
            </div>
        `;
        targetSection.style.display = 'block';
    }

    if (!recommendations || recommendations.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>Nenhuma recomendação encontrada para este produto.</p></div>';
        if(recommendationsHeader) recommendationsHeader.style.display = 'flex';
        recommendationsTitle.style.display = 'block';
        if(campaignBtn) campaignBtn.style.display = 'inline-flex';
        return;
    }

    if(recommendationsHeader) recommendationsHeader.style.display = 'flex';
    recommendationsTitle.style.display = 'block';
    if(campaignBtn) campaignBtn.style.display = 'inline-flex';
    container.innerHTML = recommendations.map(product => {
        const productName = product.PRODUTO_NOME || 'Produto sem Nome';
        return `
            <div class="card">
                <div class="img-container">
                    <img src="${product.LINK_FOTO || FALLBACK_IMAGE}" 
                         alt="${product.PRODUTO_SKU}"
                         onerror="this.onerror=null;this.src='${FALLBACK_IMAGE}'">
                </div>
                <div class="card-content">
                    <h3>${productName}</h3>
                    <span class="sku-small">${product.PRODUTO_CHAVE || product.PRODUTO_SKU}</span>
                    
                    <div class="metrics-container">
                        <span title="Porcentagem total de vendas contendo este item.">Suporte: ${product.suporte}%</span> | 
                        <span title="Probabilidade de compra deste item.">Confiança: ${product.confianca}%</span> | 
                        <span title="Lift > 1 indica forte associação entre os itens.">Lift: ${product.lift}</span> | 
                        <span title="Grau de dependência da regra.">Convicção: ${product.conviccao}</span>
                    </div>
                    
                    <div class="product-meta">
                        <span>${product.PRODUTO_COR || 'N/A'}</span>
                    </div>

                    <div class="price-tag">${product.PRODUTO_PRECO || ''}</div>
                    
                    ${product.is_fallback ? '' : `
                    <div class="xai-badge" title="Taxa de conversão: ${product.confianca}% dos clientes que compram este item, também levam a recomendação.">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
                        Comprados juntos: ${product.comprados_juntos} vezes
                    </div>
                    `}
                </div>
            </div>
        `;
    }).join('');
}

searchBtn.addEventListener('click', fetchRecommendations);

skuInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') fetchRecommendations();
});

// ─── Referências do Modal ────────────────────────────────────────────
const campaignModal       = document.getElementById('campaignModal');
const modalTitle          = document.getElementById('modalTitle');
const modalSubtitle       = document.getElementById('modalSubtitle');
const modalClientList     = document.getElementById('modalClientList');
const modalRecsList       = document.getElementById('modalRecsList');
const modalRecsSection    = document.getElementById('modalRecsSection');
const modalCloseBtn       = document.getElementById('modalCloseBtn');
const modalCloseBtnBottom = document.getElementById('modalCloseBtnBottom');

function openCampaignModal(result) {
    // Título
    modalTitle.textContent   = `✅ Campanha Disparada!`;
    modalSubtitle.textContent = result.message || `${result.impacted} cliente(s) impactado(s)`;

    // Lista de clientes
    if (result.clients && result.clients.length > 0) {
        modalClientList.innerHTML = result.clients.map(c => `
            <div class="modal-client-row">
                <div>
                    <div class="client-name">${c.nome}</div>
                    <div class="client-email">${c.email}</div>
                </div>
                <span class="badge-simulado">${c.status}</span>
            </div>
        `).join('');
    } else {
        modalClientList.innerHTML = '<p style="color:var(--text-muted);font-size:0.9rem;">Nenhum cliente elegível encontrado.</p>';
    }

    // Lista de recomendações
    if (result.recommendations && result.recommendations.length > 0) {
        modalRecsSection.style.display = 'block';
        modalRecsList.innerHTML = result.recommendations.map(r => `
            <div class="modal-rec-item">
                <img src="${r.foto || FALLBACK_IMAGE}" onerror="this.onerror=null;this.src='${FALLBACK_IMAGE}'" alt="${r.nome}">
                <span>${r.nome}</span>
            </div>
        `).join('');
    } else {
        modalRecsSection.style.display = 'none';
    }

    campaignModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeCampaignModal() {
    campaignModal.style.display = 'none';
    document.body.style.overflow = '';
}

if (modalCloseBtn)       modalCloseBtn.addEventListener('click', closeCampaignModal);
if (modalCloseBtnBottom) modalCloseBtnBottom.addEventListener('click', closeCampaignModal);
if (campaignModal)       campaignModal.addEventListener('click', (e) => {
    if (e.target === campaignModal) closeCampaignModal();
});

// ─── Botão Disparar Campanha ─────────────────────────────────────────
// Guarda os dados do último resultado renderizado para o disparo de e-mail
let _lastTargetProduct  = null;
let _lastRecommendations = [];

// Sobrescreve renderResults para guardar os dados localmente
const _originalRenderResults = renderResults;
// Interceptamos via wrapper abaixo (após a definição de renderResults)

if (campaignBtn) {
    campaignBtn.addEventListener('click', async () => {
        if (!currentProductKey) return;

        // ── 1. Coletar dados do produto-alvo exibido na tela ──────────────
        const targetImgEl    = targetSection.querySelector('img');
        const targetNameEl   = targetSection.querySelector('h2');
        const targetPriceEl  = targetSection.querySelector('.target-price');

        const produtoNome  = targetNameEl  ? targetNameEl.textContent.trim()  : (currentProductKey || '');
        const produtoPreco = targetPriceEl ? targetPriceEl.textContent.trim() : '';
        const produtoFoto  = targetImgEl   ? targetImgEl.src                  : '';

        // ── 2. Coletar cards de recomendação visíveis na tela ─────────────
        const cards = container.querySelectorAll('.card');
        const recomendacoes = [];
        cards.forEach(card => {
            const img   = card.querySelector('img');
            const nome  = card.querySelector('h3');
            const preco = card.querySelector('.price-tag');
            recomendacoes.push({
                nome:  nome  ? nome.textContent.trim()  : '',
                preco: preco ? preco.textContent.trim() : '',
                foto:  img   ? img.src                  : ''
            });
        });

        // ── 3. Estado visual: loading ──────────────────────────────────────
        campaignBtn.disabled = true;
        const originalContent = campaignBtn.innerHTML;
        campaignBtn.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                 style="width:16px;height:16px;margin-right:8px;vertical-align:middle;
                        animation:spin 1s linear infinite;">
                <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
            </svg>
            Enviando...`;

        // Garante que o spinner CSS existe
        if (!document.getElementById('spin-style')) {
            const s = document.createElement('style');
            s.id = 'spin-style';
            s.textContent = '@keyframes spin{to{transform:rotate(360deg)}}';
            document.head.appendChild(s);
        }

        // ── 4. Chamar o endpoint ───────────────────────────────────────────
        try {
            const response = await fetch('/api/disparar-campanha', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    produto_nome:    produtoNome,
                    produto_preco:   produtoPreco,
                    produto_foto:    produtoFoto,
                    recomendacoes:   recomendacoes
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // ── 5a. Sucesso: modal premium ─────────────────────────────
                _showEmailSuccessModal(data, produtoNome, recomendacoes);
            } else {
                // ── 5b. Erro de configuração (400) ─────────────────────────
                const detail = data.detail || data.message || 'Erro desconhecido.';
                showToast(`⚠️ ${detail}`, 'error');
            }

        } catch (error) {
            console.error('Erro ao disparar campanha:', error);
            showToast('Erro de conexão. Verifique se o servidor está rodando.', 'error');
        } finally {
            campaignBtn.disabled = false;
            campaignBtn.innerHTML = originalContent;
        }
    });
}

// ─── Modal de Sucesso de E-mail ───────────────────────────────────────────────
function _showEmailSuccessModal(data, produtoNome, recomendacoes) {
    // Reutiliza o modal existente com dados do envio real
    if (!campaignModal) return;

    modalTitle.textContent    = '🚀 Campanha Disparada com Sucesso!';
    modalSubtitle.textContent = data.message || 'E-mail enviado com sucesso!';

    // Lista "clientes" — no modo teste é só o destinatário
    modalClientList.innerHTML = `
        <div class="modal-client-row">
            <div>
                <div class="client-name">Cliente de Homologação</div>
                <div class="client-email">${data.destinatario || ''}</div>
            </div>
            <span class="badge-simulado" style="background:#e6f9f0;color:#1a8a4a;">✅ Enviado</span>
        </div>`;

    // Lista de recomendações incluídas no e-mail
    if (recomendacoes && recomendacoes.length > 0) {
        modalRecsSection.style.display = 'block';
        modalRecsList.innerHTML = recomendacoes.slice(0, 5).map(r => `
            <div class="modal-rec-item">
                <img src="${r.foto || FALLBACK_IMAGE}"
                     onerror="this.onerror=null;this.src='${FALLBACK_IMAGE}'"
                     alt="${r.nome}">
                <span>${r.nome}</span>
            </div>`).join('');
    } else {
        modalRecsSection.style.display = 'none';
    }

    // Atualiza o botão de preview
    const previewBtn = document.getElementById('modalPreviewBtn');
    if (previewBtn) {
        previewBtn.href = data.preview_url || '/preview_campanha.html';
        previewBtn.style.display = 'inline-flex';
    }

    campaignModal.style.display  = 'flex';
    document.body.style.overflow = 'hidden';
}

// ─── Toast ───────────────────────────────────────────────────────────
function showToast(message, type = 'success') {
    if (!toast) return;
    toast.textContent = message;
    toast.className = `toast show ${type === 'error' ? 'error' : ''}`;
    setTimeout(() => { toast.className = 'toast hidden'; }, 4000);
}

// ─── Sidebar (Top 20) ────────────────────────────────────────────────
async function fetchTopSellers() {
    const listContainer = document.getElementById('topSellersList');
    if (!listContainer) return;

    try {
        const response = await fetch('/api/products/top-sellers');
        const data = await response.json();
        
        if (data.top_sellers && data.top_sellers.length > 0) {
            listContainer.innerHTML = data.top_sellers.map((item, index) => {
                // Usa produto_chave para buscar recomendações corretas; fallback para referencia
                const searchKey = item.produto_chave || item.referencia;
                return `
                <div class="sidebar-item" onclick="triggerSearch('${searchKey}')">
                    <div class="sidebar-item-rank">${index + 1}</div>
                    <img src="${item.foto || FALLBACK_IMAGE}" onerror="this.onerror=null;this.src='${FALLBACK_IMAGE}'" alt="${item.nome}">
                    <div class="sidebar-item-info">
                        <div class="sidebar-item-name" title="${item.nome || item.referencia}">${item.nome || item.referencia}</div>
                        <div class="sidebar-item-meta">${item.qtde_vendida} vendidos${item.cor ? ' · ' + item.cor : ''}</div>
                    </div>
                </div>
                `;
            }).join('');
        } else {
            listContainer.innerHTML = '<p style="text-align:center;color:var(--text-muted);font-size:0.9rem;padding:1rem;">Nenhum produto encontrado.</p>';
        }
    } catch (error) {
        console.error('Erro ao buscar top sellers:', error);
        listContainer.innerHTML = '<p style="text-align:center;color:var(--text-muted);font-size:0.9rem;padding:1rem;">Erro ao carregar ranking.</p>';
    }
}

function triggerSearch(sku) {
    if (skuInput) {
        skuInput.value = sku;
        fetchRecommendations();
        // Opcional: Rolar para o topo caso no mobile
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// ─── Logout ──────────────────────────────────────────────────────────────────
function logout() {
    sessionStorage.removeItem('auth_token');
    sessionStorage.removeItem('user_email');
    window.location.href = '/login.html';
}

const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) logoutBtn.addEventListener('click', logout);

// Inicializar
document.addEventListener('DOMContentLoaded', fetchTopSellers);
