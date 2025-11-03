// script simples que mantém estado 'curtido' em localStorage para produtos e lojas
(function () {
    function getStore(key) {
        try { return JSON.parse(localStorage.getItem(key) || '{}'); } catch(e){ return {}; }
    }
    function setStore(key, obj) { localStorage.setItem(key, JSON.stringify(obj)); }

    const PROD_KEY = 'likes_produto_v1';
    const LOJA_KEY = 'likes_loja_v1';

    function isLiked(type, id) {
        const store = getStore(type === 'produto' ? PROD_KEY : LOJA_KEY);
        return !!store[id];
    }
    function toggleLike(btn, type, id) {
        const key = (type === 'produto') ? PROD_KEY : LOJA_KEY;
        const store = getStore(key);
        if (store[id]) { delete store[id]; btn.classList.remove('liked'); }
        else { store[id] = (new Date()).toISOString(); btn.classList.add('liked'); }
        setStore(key, store);
    }

    function initButtons() {
        document.querySelectorAll('.btn-curtir[data-type]').forEach(btn => {
            const type = btn.getAttribute('data-type');
            const id = btn.getAttribute('data-id');
            if (!type || !id) return;
            if (isLiked(type, id)) btn.classList.add('liked');

            btn.addEventListener('click', function (e) {
                e.preventDefault();
                toggleLike(btn, type, id);
                // aqui você pode adicionar chamada AJAX para persistir no servidor
            });
        });
    }

    // on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initButtons);
    } else initButtons();
})();