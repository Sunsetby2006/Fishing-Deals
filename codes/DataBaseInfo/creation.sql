create database if not exists datos_tienda;
use datos_tienda;

-- usres
create table if not exists users (
	user_id int auto_increment primary key,
    nombre varchar(100) not null,
    email varchar(100) not null,
    contrasena varchar(100) not null,
    direccion varchar(100)not null,
    rol enum ('Cliente', 'Vendedor') not null
);

-- categorías
create table if not exists categories (
	category_id int auto_increment primary key,
    nombre varchar(50) not null unique
);

-- productos
create table if not exists products (
	product_id int auto_increment primary key,
    nombre varchar(100) not null,
    descripcion varchar(300) not null,
    precio decimal(10,2) not null,
    stock int not null,
    user_id int not null,
	category_id int not null,
    image_url varchar(500)not null,
    foreign key(user_id) references users(user_id)
		on delete cascade
        on update cascade
);

-- pedidos
create table if not exists purchase (
	purchase_id int auto_increment primary key,
    user_id int not null,
    fecha date not null,
    total int not null,
    estado enum ('Preparando', 'Enviando', 'Enviado', 'Entregado') not null,
	foreign key (user_id) references users(user_id)
		on delete cascade
        on update cascade
);

-- info de pedidos
create table if not exists purchase_info (
	info_id int auto_increment primary key,
    purchase_id int not null,
    product_id int not null,
    cantidad int not null,
    precio_unitario decimal(10,2) not null,
    foreign key (purchase_id) references purchase(purchase_id)
		on delete cascade
        on update cascade,
	foreign key (product_id)  references products(product_id)
		on delete cascade
        on update cascade
);

-- reviews
create table if not exists reviews (
	review_id int auto_increment primary key,
    user_id int not null,
    product_id int not null,
    score int check(score between 1 and 5),
    coment varchar(300),
    fecha date not null,
    foreign key (user_id) references users(user_id)
		on delete cascade
        on update cascade,
    foreign key (product_id) references products(product_id)
		on delete cascade
        on update cascade,
	unique (user_id, product_id)
);

-- wishlist
create table if not exists wishlist (
	wishlist_id int auto_increment primary key,
    user_id int not null,
    product_id int not null,
    fecha_agregado timestamp default current_timestamp,
    foreign key (user_id) references users(user_id)
		on delete cascade
        on update cascade,
	foreign key (product_id) references products(product_id)
		on delete cascade
        on update cascade,
	unique (user_id, product_id)
);

-- carrito
create table if not exists cart (
	cart_id int auto_increment primary key,
    user_id int not null,
    product_id int not null,
    cantidad int not null default 1,
    fecha_agregado timestamp default current_timestamp,
    foreign key (user_id) references users(user_id)
		on delete cascade
        on update cascade,
	foreign key (product_id) references products(product_id)
		on delete cascade
        on update cascade,
	unique (user_id, product_id),
    check (cantidad > 0)
);

-- ventas
create table if not exists sells (
    sell_id int auto_increment primary key,
    user_id int not null,
    product_id int not null,
    ganancia int not null,
    foreign key(user_id) references users(user_id)
        on delete cascade
        on update cascade,
    foreign key(product_id) references products(product_id)
        on delete cascade
        on update cascade,
);
