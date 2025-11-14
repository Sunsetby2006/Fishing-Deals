use datos_tienda;

-- users
insert into users (nombre, email, contrasena, direccion, rol) values
('Omar Fernando Guevara Cavazos', 'omar.correo@gmail.com', 'Sunsetr2d2', 'Cumbres', 'Cliente'),
('Ivan Gerardo Tenorio Silverio', 'ivan.correo@gmail.com', 'contrasena', 'dir', 'Cliente'),
('Diego Alejandro Medellin Mendez', 'diego.correo@gmail.com', 'Degozc33', 'San Pedro', 'Cliente'),
('Mariana de la Garza Contel', 'mariana.correo@gmail.com', 'Mar2222', 'Cumbres', 'Cliente'),
('Natalia Paez Casados', 'natalia.correo@gmail.com', 'Nat2556', 'Cumbres', 'Cliente'),
('Brissia Smith Olguin', 'brissia.correo@gmail.com', 'Brissia26', 'Cumbres', 'Cliente'),
('Maria Fernanda Guevara Cavazos', 'fer.correo@gmail.com', 'vendedora1', 'Cumbres', 'Vendedor'),
('Anakin Skywalker', 'ani.correo@gmail.com', 'LaFuerza123', 'Naboo', 'Vendedor'),
('Billie Eillish ', 'billie.correo@gmail.com', 'OceanEyes', 'USA', 'Vendedor');

-- categorias
insert into categories (nombre) values
('Tecnologia'),
('Libros'),
('Nuevos de temporada'),
('Hogar'),
('Escuela'),
('Deportes'),
('Nuevo');

-- productos
insert into products (nombre, descripcion, precio, stock, user_id, image_url, category_id) values
('MacBook Air', 'Laptop perfecta para estudiantes de la marca Apple', 22500, 10, 7, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/macbook.jpeg?raw=true', 1),
('PC Gamer', 'Computadora equipada con lo mejor de lo mejor', 35000, 5, 7, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/pc.jpeg?raw=true', 1),
('Mouse Gamer', 'Mouse Razer con RGB customizable', 980, 30, 7, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/mouse.webp?raw=true', 1),
('Control inalámbrico Xbox', 'Color: Azul', 1500, 3, 7, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/xbox.jpeg?raw=true', 1),

('Juntos a Medianoche', 'Libro de romance', 300, 10, 8, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/juntosamedianoche.jpeg?raw=true', 2),
('Into the Pit', 'Libro de la saga de FNAF', 350, 20, 8, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/intothepit.jpeg?raw=true', 2),
('Este Invierno', 'Escrito por Alice Oseman', 280, 5, 8, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/esteinvierno.png?raw=true', 2),
('El Juego Infinito', 'Nueva edición', 400, 10, 8, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/eljuegoinfinito.jpeg?raw=true', 2),

('Pino decorativo para Hogar', 'Pino artificial perfecto para todas las casas', 899, 70, 9, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/WhatsApp%20Image%202025-11-03%20at%206.15.56%20PM.jpeg?raw=true', 3),
('Sombrero de Santa', 'Unisex y unitalla, perfecto para tus posadas', 100, 70, 9, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/Sombrero%20de%20Santa.jpeg?raw=true', 3),
('Envoltorios para regalo', 'Diseños bonitos para tus regalos esta navidad', 70, 100, 9, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/papel.jpeg?raw=true', 3),
('Taza Navideña', 'Buena opción para tus intercambios', 150, 58, 9, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/Taza%20navide%C3%B1a.jpeg?raw=true', 3),

('Sillón', 'Cómodo y resistente, perofecto para tu hogar', 899, 70, 7, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/sofa.jpeg?raw=true', 4),
('Lámpara', 'Linda lámpara de forma de capybara', 350, 18, 7, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/lampara.webp?raw=true', 4),
('Mesa', 'Mesa perfecta para decorar la sala de tu casa', 1799, 3, 7, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/mesa.jpeg?raw=true', 4),
('Alfombra', 'Alfombra 150x190 cm', 799, 8, 7, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/mat.jpg?raw=true', 4),

('Mochila', 'Mochila aesthetic para tu regreso a clases', 1050, 19, 8, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/bag.jpeg?raw=true', 5),
('Set de lápices', 'Lápices de madera escolares', 350, 30, 8, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/lapices.jpeg?raw=true', 5),
('Libretas', 'Set de libretas de cuadro chico y doble raya', 400, 20, 8, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/notebook.jpeg?raw=true', 5),
('Calculadora', 'Calculadora científica', 899, 3, 8, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/calc.jpeg?raw=true', 5),

('Pelota', 'pelota inflable para playa y albercas', 199, 100, 9, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/pelota.jpeg?raw=true', 6),
('Raquetas', 'Set de dos raquetas para jugar tenis', 700, 30, 8, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/raqueta.jpeg?raw=true', 6),
('Tachones', 'Tallas 24-29', 799, 80, 9, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/zapatillas.jpeg?raw=true', 6),
('Set de Baseball', 'Sin descripción', 899, 3, 9, 'https://github.com/Sunsetby2006/Fishing-Deals/blob/main/Imagenes/equip.webp?raw=true', 6);

-- reseñas
insert into reviews (user_id, product_id, score, coment, fecha) values
(3,1,2,'No corre genshin impact ni valorant', '2025-11-04'),
(5,2,3,'Buenísima, es muy rápida, y me encanta', '2025-11-04'),
(4,3,4,'Muy recomendado, llegó rápido y es cómodo para jugar', '2025-11-04'),
(2,4,4,'Muy bueno, pero requiere baterías', '2025-11-04'),
(1,5,5,'Un buen libro para pasar el rato, me lo acabé en una semana', '2025-11-04'),
(4,9,4,'Grande y se ve bien en mi sala', '2025-11-05'),
(3,10,5,'Lindo', '2025-11-05'),
(1,12,4,'Le gustó a mi hermana', '2025-11-05'),
(3,13,5,'Muy cómodo y el color combina con mi sala', '2025-11-05'),
(5,14,4,'Le gustó a mi sobrina', '2025-11-05'),
(2,16,1,'No me gustó el color al final', '2025-11-05'),
(1,17,5,'Todo lo que cargo cupo en la mochila', '2025-11-06'),
(6,20,5,'Funciona', '2025-11-02'),
(1,22,4,'Los mangos tienen buen agarre', '2025-11-01');

-- wishlist
insert into wishlist (user_id, product_id) values
(1, 1),
(1, 2),
(2, 5),
(3, 3),
(3, 4),
(4, 9),
(5, 13),
(6, 17);

-- carrito
insert into cart (user_id, product_id, cantidad) values
(1, 3, 2),
(1, 10, 5),
(2, 1, 1),
(3, 5, 3),
(3, 6, 2),
(4, 11, 10),
(5, 14, 1),
(6, 20, 1);

-- Pedidos
insert into purchase (user_id, fecha, total, estado) values
(1, '2025-11-06', 1960, 'Entregado'),      
(1, '2025-11-07', 500, 'Enviado'),         
(2, '2025-11-06', 22500, 'Enviado'),       
(3, '2025-11-07', 1600, 'Preparando'),     
(3, '2025-11-08', 1050, 'Entregado'),      
(4, '2025-11-08', 700, 'Entregado'),       
(5, '2025-11-09', 1149, 'Preparando'),     
(6, '2025-11-09', 899, 'Enviando'),        
(2, '2025-11-10', 35000, 'Entregado'),     
(4, '2025-11-11', 8990, 'Preparando');     

-- Detalle de pedidos
insert into purchase_info (purchase_id, product_id, cantidad, precio_unitario) values
(1, 3, 2, 980),      
(2, 10, 5, 100),     
(3, 1, 1, 22500),    
(4, 5, 2, 300),      
(4, 6, 2, 350),      
(5, 17, 1, 1050),    
(6, 22, 1, 700),     
(7, 14, 1, 350),     
(7, 16, 1, 799),     
(8, 20, 1, 899),     
(9, 2, 1, 35000),    
(10, 9, 10, 899);    
