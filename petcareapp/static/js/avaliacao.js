// Removemos o listener de 'DOMContentLoaded' duplicado e unificamos tudo em um só.
document.addEventListener('DOMContentLoaded', () => {
    
    // ===================================================================
    // Parte 1: Script para avaliação com estrelas (Formulário NOVO)
    // (Seu código original, seleciona .rating)
    // ===================================================================
    document.querySelectorAll('.rating').forEach(ratingContainer => {
        const estrelas = ratingContainer.querySelectorAll('label');
        const inputs = ratingContainer.querySelectorAll('input');

        estrelas.forEach((label, idx) => {
            label.addEventListener('click', () => {
                // Ao clicar, garante que o input correspondente seja marcado
                const input = document.getElementById(label.htmlFor);
                if (input) input.checked = true;
                // O CSS cuidará da atualização visual
            });
        });
    });

    // ===================================================================
    // Parte 2: Envio AJAX de avaliação de PRODUTO
    // (Seu código original)
    // ===================================================================
    const formAvaliacaoProduto = document.getElementById('form-avaliacao-produto');
    if (formAvaliacaoProduto) {
        formAvaliacaoProduto.addEventListener('submit', async (e) => {
            e.preventDefault();
            const url = formAvaliacaoProduto.getAttribute('action');
            const formData = new FormData(formAvaliacaoProduto);
            const csrfToken = formData.get('csrfmiddlewaretoken');
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken, 'Accept': 'application/json' },
                body: formData,
            });
            if (!response.ok) {
                console.error('Erro ao avaliar produto');
                return;
            }
            // Recarrega a página para exibir a nova avaliação e a mensagem de "já avaliou".
            window.location.reload();
        });
    }

    // ===================================================================
    // Parte 3: Função genérica para Curtir/Favoritar (Lojas e Produtos)
    // (Seu código original)
    // ===================================================================
    async function handleLikeClick(event) {
        event.preventDefault();
        const button = event.currentTarget;
        const url = button.dataset.url;
        const csrfToken = button.dataset.csrf;
        const icon = button.querySelector('i');

        if (!url || !csrfToken || !icon) {
            console.error('Botão de curtir mal configurado. Faltando data-url, data-csrf ou ícone.');
            return;
        }

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken, 'Accept': 'application/json' },
            });

            if (!response.ok) throw new Error('A resposta da rede não foi OK');
            
            const data = await response.json();

            button.classList.toggle('curtido', data.curtido || data.favoritado);
            icon.classList.toggle('bi-heart', !(data.curtido || data.favoritado));
            icon.classList.toggle('bi-heart-fill', data.curtido || data.favoritado);

            // Atualiza contadores se existirem
            const countElId = button.dataset.countTarget;
            if (countElId) {
                const countEl = document.getElementById(countElId);
                // Usamos '??' para pegar o primeiro valor não nulo (curtidas ou favoritos)
                if (countEl) countEl.textContent = data.total_curtidas ?? data.total_favoritos;
            }
        } catch (error) {
            console.error('Erro ao processar a ação de curtir:', error);
        }
    }
    // Atribui a função de clique aos botões
    document.querySelectorAll('.btn-curtir-loja, .btn-curtir-produto, .btn-favoritar-loja').forEach(btn => {
        btn.addEventListener('click', handleLikeClick);
    });
// ===================================================================
    // Parte 4: LÓGICA DO MODAL DE EDIÇÃO DE AVALIAÇÃO DA LOJA
    // (BLOCO CORRIGIDO)
    // ===================================================================
    const modalEditarAvaliacao = document.getElementById('modalEditarAvaliacao');
    
    if (modalEditarAvaliacao) {
        const form = document.getElementById('edit-avaliacao-form');
        const comentarioInput = document.getElementById('edit-comentario');
        const starLabels = form.querySelectorAll('.star-label-modal');
        const starRadios = form.querySelectorAll('input[name="nota"]');

        // Evento que dispara QUANDO O MODAL ESTÁ SENDO ABERTO
        modalEditarAvaliacao.addEventListener('show.bs.modal', (event) => {
            const button = event.relatedTarget; 
            const formAction = button.getAttribute('data-form-action');
            const nota = button.getAttribute('data-nota');
            const comentario = button.getAttribute('data-comentario');
            
            form.setAttribute('action', formAction);
            comentarioInput.value = comentario;
            
            // Limpa seleções anteriores
            starLabels.forEach(label => label.classList.remove('selected'));
            starRadios.forEach(radio => radio.checked = false);

            const radioToCheck = form.querySelector('input[name="nota"][value="' + nota + '"]');
            
            if (radioToCheck) {
                radioToCheck.checked = true;
                const labelForRadio = form.querySelector('label[for="' + radioToCheck.id + '"]');
                
                if (labelForRadio) {
                    // "Acende" a estrela clicada e todas as seguintes (visualmente à esquerda)
                    labelForRadio.classList.add('selected');
                    let el = labelForRadio;
                    // CORREÇÃO AQUI: usa nextElementSibling
                    while (el = el.nextElementSibling) { 
                        if (el.tagName === 'LABEL') {
                            el.classList.add('selected');
                        }
                    }
                }
            }
        });

        // Adiciona o comportamento de clique nas estrelas DO MODAL
        starLabels.forEach(label => {
            label.addEventListener('click', () => {
                // Limpa todas as estrelas
                starLabels.forEach(lbl => lbl.classList.remove('selected'));
                
                // "Acende" a estrela clicada e todas as seguintes (visualmente à esquerda)
                label.classList.add('selected');
                let el = label;
                // CORREÇÃO AQUI: usa nextElementSibling
                while (el = el.nextElementSibling) {
                    if (el.tagName === 'LABEL') {
                        el.classList.add('selected');
                    }
                }
            });
        });
    } // --- Fim da lógica do Modal ---

    // ===================================================================
    // Parte 5: Reutilizável: procura .star-rating e habilita meia-estrela
    // (Seu código original, agora dentro do listener unificado)
    // ===================================================================
    document.querySelectorAll('.star-rating').forEach(initStarRating);

}); // --- FIM DO 'DOMContentLoaded' PRINCIPAL ---


// ===================================================================
// Parte 6: Função initStarRating e helpers (para exibição de meia-estrela)
// (Seu código original, movido para fora do DOMContentLoaded)
// ===================================================================
function initStarRating(container) {
  const stars = Array.from(container.querySelectorAll('.star'));
  let current = parseFloat(container.dataset.rating) || 0;
  const itemType = container.dataset.itemType || null;
  const itemId = container.dataset.itemId || null;
  container.tabIndex = container.getAttribute('tabindex') || 0;

  function render(value) {
    stars.forEach((star, i) => {
      const idx = i + 1;
      let fill = 0;
      if (value >= idx) fill = 100;
      else if (value >= idx - 0.5) fill = 50;
      else fill = 0;
      star.querySelector('.fill-wrap').style.width = fill + '%';
      star.setAttribute('aria-checked', (value >= idx - 0.5 && value < idx) || value >= idx ? 'true' : 'false');
      star.setAttribute('aria-label', idx + ' estrela' + (fill === 50 ? ' e meia' : '') );
    });
    container.dataset.rating = value;
  }

  function setValueFromEvent(e, starIndex) {
    const star = stars[starIndex - 1];
    const rect = star.getBoundingClientRect();
    const isHalf = (e.clientX - rect.left) < (rect.width / 2);
    const val = starIndex - (isHalf ? 0.5 : 0);
    current = val;
    render(current);
    // dispatch event so app can catch and persist server-side if wanted
    container.dispatchEvent(new CustomEvent('rating:changed', { detail: { value: current, itemType, itemId } }));
  }

  // attach pointer handlers
  stars.forEach((star, i) => {
    const idx = i + 1;
    star.addEventListener('mousemove', (e) => {
      const rect = star.getBoundingClientRect();
      const isHalf = (e.clientX - rect.left) < (rect.width / 2);
      const hoverVal = idx - (isHalf ? 0.5 : 0);
      render(hoverVal);
    });
    star.addEventListener('mouseleave', () => render(current));
    star.addEventListener('click', (e) => setValueFromEvent(e, idx));
    // touch support (tap => full or half depending on x)
    star.addEventListener('touchstart', (e) => {
      const touch = e.touches[0];
      setValueFromEvent(touch, idx);
      e.preventDefault();
    }, { passive: false });
  });

  // keyboard support: left/right arrows adjust by 0.5, enter to confirm
  container.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
      e.preventDefault();
      current = Math.max(0.5, Math.round((current - 0.5) * 2) / 2);
      render(current);
      container.dispatchEvent(new CustomEvent('rating:changed', { detail: { value: current, itemType, itemId } }));
    } else if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
      e.preventDefault();
      current = Math.min(5, Math.round((current + 0.5) * 2) / 2);
      render(current);
      container.dispatchEvent(new CustomEvent('rating:changed', { detail: { value: current, itemType, itemId } }));
    } else if (e.key === 'Home') { current = 0; render(current); }
    else if (e.key === 'End') { current = 5; render(current); }
  });

  // initial render
  render(current);
}