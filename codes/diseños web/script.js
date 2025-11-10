document.addEventListener('DOMContentLoaded', () => {
    // Obtener el ID del producto desde sessionStorage (seteado en home.html)
    const PRODUCT_ID = sessionStorage.getItem('selectedProductId') || 1; // Default a 1 si no hay ID
    const API_URL = `http://127.0.0.1:8000/api/product/${PRODUCT_ID}`;

    // Función para generar las estrellas de calificación
    function renderStars(score) {
        let starsHtml = '';
        const fullStars = Math.floor(score);
        const hasHalfStar = score % 1 >= 0.25 && score % 1 <= 0.75;

        for (let i = 0; i < 5; i++) {
            if (i < fullStars) {
                starsHtml += '<i class="fas fa-star"></i>'; // Estrella llena
            } else if (i === fullStars && hasHalfStar) {
                starsHtml += '<i class="fas fa-star-half-alt"></i>'; // Media estrella
            } else {
                starsHtml += '<i class="far fa-star"></i>'; // Estrella vacía
            }
        }
        return starsHtml;
    }

    //filtrado? supongo
    function filtrarItems(precioMin, precioMax){
        const result = loadProductDetails.filter(producto => producto.precio >= precioMin && producto.precio <= precioMax);
    }

    // Función para formatear fecha
    function formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString('es-ES', options);
    }

    // Función para cambiar la imagen principal
    function changeMainImage(imageUrl) {
        document.getElementById('main-product-image').src = imageUrl;
    }

    // Función para navegar al home
    function goToHome() {
        window.location.href = '../home.html';
    }

    // Función principal para cargar los datos del producto
    async function loadProductDetails() {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            const product = data.product;
            const reviews = data.reviews;
            const variants = data.variants;

            // 1. Renderizar Datos Principales
            document.getElementById('productTitle').textContent = product.nombre;
            document.getElementById('product-name-display').textContent = product.nombre;
            document.getElementById('main-product-image').src = product.image_url;
            document.getElementById('description-text').textContent = product.descripcion;
            document.getElementById('stock-display').textContent = `Stock disponible: ${product.stock} unidades`;
            
            // Formatear precio
            const priceParts = product.precio.toFixed(2).split('.');
            document.getElementById('price-display').textContent = `$${priceParts[0]}.${priceParts[1]}`;

            // 2. Renderizar Calificaciones
            document.getElementById('average-score-display').textContent = data.average_score.toFixed(1);
            document.getElementById('total-reviews-display').textContent = data.total_reviews;
            document.getElementById('stars-display').innerHTML = renderStars(data.average_score);

            // 3. Crear miniaturas (usando la misma imagen por ahora)
            const thumbnailsContainer = document.getElementById('product-thumbnails');
            for (let i = 0; i < 3; i++) {
                const thumbnailItem = document.createElement('div');
                thumbnailItem.classList.add('thumbnail-item');
                thumbnailItem.innerHTML = `<img src="${product.image_url}" alt="Miniatura ${i + 1}">`;
                thumbnailItem.addEventListener('click', () => changeMainImage(product.image_url));
                thumbnailsContainer.appendChild(thumbnailItem);
            }

            // 4. Renderizar Variantes
            const variantContainer = document.getElementById('variant-options-container');
            variants.forEach((variant, index) => {
                const btn = document.createElement('button');
                btn.classList.add('variant-btn');
                // Marcar el primero como seleccionado por defecto
                if (index === 0) {
                    btn.classList.add('variant-btn-selected');
                }
                // Formatear precio para la etiqueta de variante
                const formattedPrice = variant.precio.toFixed(2);
                btn.innerHTML = `${variant.etiqueta}<br><span style="font-weight: bold;">$${formattedPrice}</span>`;
                
                btn.addEventListener('click', () => {
                    // Lógica para seleccionar la variante
                    document.querySelectorAll('.variant-btn').forEach(b => b.classList.remove('variant-btn-selected'));
                    btn.classList.add('variant-btn-selected');
                    // Actualizar el precio principal
                    const mainPriceParts = variant.precio.toFixed(2).split('.');
                    document.getElementById('price-display').textContent = `$${mainPriceParts[0]}.${mainPriceParts[1]}`;
                });

                variantContainer.appendChild(btn);
            });

            // 5. Renderizar Reseña Destacada
            const featuredReviewContainer = document.getElementById('featured-review-container');
            if (reviews.length > 0) {
                const featuredReview = reviews[0];
                featuredReviewContainer.innerHTML = `
                    <h3>Reseña Destacada</h3>
                    <p class="review-text">"${featuredReview.coment}"</p>
                    <span class="review-user-name">- ${featuredReview.user_name}</span>
                    <span class="review-stars">${renderStars(featuredReview.score)}</span>
                    <span class="review-date">${formatDate(featuredReview.fecha)}</span>
                `;

                // Mostrar todas las reseñas si hay más de una
                if (reviews.length > 1) {
                    const allReviewsSection = document.getElementById('all-reviews-section');
                    allReviewsSection.style.display = 'block';
                    
                    const reviewsList = document.getElementById('reviews-list');
                    reviews.slice(1).forEach(review => {
                        const reviewElement = document.createElement('div');
                        reviewElement.classList.add('review-item');
                        reviewElement.innerHTML = `
                            <div class="review-header">
                                <span class="review-user">${review.user_name}</span>
                                <span class="review-stars">${renderStars(review.score)}</span>
                                <span class="review-date">${formatDate(review.fecha)}</span>
                            </div>
                            <p class="review-comment">"${review.coment}"</p>
                        `;
                        reviewsList.appendChild(reviewElement);
                    });
                }
            } else {
                featuredReviewContainer.innerHTML = `
                    <p class="review-text">Este producto aún no tiene reseñas. ¡Sé el primero en opinar!</p>
                `;
            }

            // 6. Agregar funcionalidad a los botones de acción
            document.querySelector('.btn-add-to-cart').addEventListener('click', () => {
                const selectedVariant = document.querySelector('.variant-btn-selected').textContent.split('\n')[0];
                alert(`Producto añadido al carrito: ${product.nombre} - ${selectedVariant}`);
            });

            document.querySelector('.btn-buy-now').addEventListener('click', () => {
                const selectedVariant = document.querySelector('.variant-btn-selected').textContent.split('\n')[0];
                alert(`Procediendo a comprar: ${product.nombre} - ${selectedVariant}`);
            });

            // 7. Agregar funcionalidad al logo/breadcrumb para volver al home
            document.querySelector('.breadcrumb').addEventListener('click', goToHome);

        } catch (error) {
            console.error("Error al cargar los detalles del producto:", error);
            document.getElementById('product-name-display').textContent = "Error al cargar el producto.";
            document.getElementById('description-text').textContent = "No se pudo cargar la información del producto. Por favor, intenta más tarde.";
            
            // Mostrar mensaje de error en la reseña
            document.getElementById('featured-review-container').innerHTML = `
                <p class="review-text">Error al cargar las reseñas. Verifica que el servidor esté funcionando.</p>
            `;
        }
    }

    loadProductDetails();
});