INSERT INTO ROL (id, nombre, descripcion)
VALUES
(1, 'Administrador', 'Gestiona usuarios, pedidos, configuraciones y control total del sistema'),
(2, 'Cliente', 'Usuario que realiza pedidos y gestiona sus compras'),
(3, 'Tienda', 'Gestor de una tienda dentro del ecommerce multitienda'),
(4, 'Repartidor', 'Encargado de la entrega de los pedidos a los clientes');

INSERT INTO PROVINCIA (id, nombre) VALUES (1, 'Arequipa');
INSERT INTO DISTRITO (id, provincia_id, nombre) VALUES (1, 1, 'Cercado');

INSERT INTO CATEGORIA (id, nombre, descripcion, estadoregistro)
VALUES
(1, 'Fertilizantes', 'Productos que aportan nutrientes esenciales para el crecimiento de las plantas', 'A'),
(2, 'Herbicidas', 'Productos químicos para el control de malezas y hierbas no deseadas', 'A'),
(3, 'Insecticidas', 'Productos para la prevención y control de plagas e insectos en cultivos', 'A'),
(4, 'Fungicidas', 'Sustancias que eliminan o previenen el desarrollo de hongos en plantas', 'A'),
(5, 'Bioestimulantes', 'Productos naturales que mejoran la absorción de nutrientes y la resistencia del cultivo', 'A'),
(6, 'Semillas y Sustratos', 'Insumos para la siembra y germinación de cultivos agrícolas', 'A');

INSERT INTO ETIQUETA (id, nombre)
VALUES
(1, 'Orgánico'),
(2, 'Uso Profesional'),
(3, 'Alto Rendimiento'),
(4, 'Ecológico'),
(5, 'Certificado SENASA');

-- 2. Usuarios / vendedores / colecciones
INSERT INTO USUARIO (id, nombre, email, clave, telefono, rol_id, estado)
VALUES (2, 'AgroTienda Central', 'agrotienda@example.com', '$2b$12$ZJQ3wwKIpV8o6H5zb3eNPOjsbVhNHO2rnOaG3pxKiaKJ49oybqV5K', '987654321', 3, 'A');

INSERT INTO VENDEDOR (id, usuario_id, nombretienda, descripcion, logo, distrito_id, estado)
VALUES (
  1,
  2,
  'AgroTienda Central',
  'Tienda especializada en productos agroquímicos para cultivos agrícolas y control de plagas. Ofrece fertilizantes, pesticidas, herbicidas y bioinsumos certificados.',
  'logoTienda.png',
  1,
  'A'
);

INSERT INTO POLITICATIENDA (id, vendedor_id, politicaenvio, politicadevolucion, politicaprivacidad, fechaactualizacion, estadoregistro)
VALUES (
  1,
  1,
  'Los envíos se realizan en un plazo de 2 a 5 días hábiles según la zona. Se usan transportistas certificados.',
  'Se aceptan devoluciones dentro de los 7 días posteriores a la entrega si el producto está en su empaque original y sin uso.',
  'La tienda protege los datos personales conforme a la Ley de Protección de Datos vigente.',
  NOW(),
  'A'
);

INSERT INTO COLECCIONTIENDA (id, vendedor_id, nombre, descripcion, estadoregistro)
VALUES
(1, 1, 'Fertilizantes Premium', 'Selección de los mejores fertilizantes del mercado para cultivos de alto valor', 'A');

-- 3. Productos
INSERT INTO PRODUCTO (
  id, categoria_id, vendedor_id, colecciontienda_id, nombre, descripcion,
  precio, stock, fotoprincipal, descuento, fechainiciodescuento, fechafindescuento,
  activodescuento, estadoregistro, estado
)
VALUES
(1, 1, 1, 1, 'Urea Granulada 46%', 'Fertilizante nitrogenado altamente concentrado ideal para todo tipo de cultivos. Mejora el crecimiento vegetativo y el rendimiento.', 95.50, 150, 'producto1.png', 10.00, '2025-10-01', '2025-10-31', 1, 'A', 'A'),
(2, 2, 1, 1, 'Glifosato 480 SL', 'Herbicida sistémico de amplio espectro para control de malezas anuales y perennes. Uso agrícola certificado.', 135.90, 80, 'producto2.png', 0, NULL, NULL, 0, 'A', 'A'),
(3, 3, 1, 1, 'Lambda-Cyhalotrina 5 EC', 'Insecticida piretroide de acción de contacto e ingestión. Control efectivo contra áfidos, orugas y trips.', 110.00, 120, 'producto3.png', 5.00, '2025-10-10', '2025-11-10', 1, 'A', 'A'),
(4, 4, 1, 1, 'Tebuconazol 25 EC', 'Fungicida sistémico con acción preventiva y curativa. Controla royas, oídios y manchas foliares.', 89.90, 60, 'producto4.png', 0, NULL, NULL, 0, 'A', 'A'),
(5, 5, 1, 1, 'Bioestimulante Foliar GreenMax', 'Bioestimulante orgánico a base de aminoácidos y extractos vegetales. Mejora la absorción de nutrientes y la resistencia al estrés.', 150.00, 50, 'producto5.png', 15.00, '2025-10-15', '2025-11-15', 1, 'A', 'A'),
(6, 6, 1, 1, 'Semilla de Maíz Híbrido Amarillo', 'Semilla certificada de alto rendimiento, resistente a plagas y adaptada a diversas zonas agroecológicas.', 280.00, 40, 'producto6.png', 0, NULL, NULL, 0, 'A', 'A');

INSERT INTO PRODUCTOETIQUETA (id, producto_id, etiqueta_id)
VALUES
(1, 1, 3),
(2, 2, 2),
(3, 3, 2),
(4, 4, 2),
(5, 5, 1),
(6, 5, 4),
(7, 6, 5);

INSERT INTO PRODUCTOOPCION (id, producto_id, tipo, nombre, valor, detalle, imagen, estadoregistro)
VALUES
(1, 1, 'T', 'Presentación', 'Saco 50 kg', 'Ideal para cultivos extensivos', 'opcion1.png', 'A'),
(2, 2, 'T', 'Presentación', 'Bidón 20 L', 'Uso agrícola certificado', 'opcion2.png', 'A'),
(3, 3, 'T', 'Concentración', '5% EC', 'Formulación líquida', 'opcion3.png', 'A'),
(4, 4, 'T', 'Envase', 'Botella 1 L', 'Fungicida sistémico concentrado', 'opcion4.png', 'A'),
(5, 5, 'T', 'Formato', 'Frasco 500 ml', 'Bioestimulante líquido orgánico', 'opcion5.png', 'A'),
(6, 6, 'T', 'Peso', 'Bolsa 25 kg', 'Semilla híbrida certificada', 'opcion6.png', 'A');

-- 4. Estados generales (NECESARIO antes de CARRITO)
INSERT INTO ESTADOGENERAL (id, nombre, tipo)
VALUES
(1, 'Activo', 'CARRITO');

-- 5. Clientes y carritos
INSERT INTO USUARIO (id, nombre, email, clave, telefono, rol_id, estado)
VALUES
(3, 'Juan Pérez', 'juan.perez@agroexample.com', '$2b$12$ZJQ3wwKIpV8o6H5zb3eNPOjsbVhNHO2rnOaG3pxKiaKJ49oybqV5K', '951234567', 2, 'A'),
(4, 'María López', 'maria.lopez@agroexample.com', '$2b$12$ZJQ3wwKIpV8o6H5zb3eNPOjsbVhNHO2rnOaG3pxKiaKJ49oybqV5K', '952345678', 2, 'A'),
(5, 'Carlos Ramos', 'carlos.ramos@agroexample.com', '$2b$12$ZJQ3wwKIpV8o6H5zb3eNPOjsbVhNHO2rnOaG3pxKiaKJ49oybqV5K', '953456789', 2, 'A'),
(6, 'Lucía Torres', 'lucia.torres@agroexample.com', '$2b$12$ZJQ3wwKIpV8o6H5zb3eNPOjsbVhNHO2rnOaG3pxKiaKJ49oybqV5K', '954567890', 2, 'A');

INSERT INTO CARRITO (id, usuario_id, fechacreacion, estadogeneral_id, total)
VALUES
(1, 3, NOW(), 1, 240.50),
(2, 4, NOW(), 1, 150.00),
(3, 5, NOW(), 1, 185.90),
(4, 6, NOW(), 1, 95.50);

INSERT INTO CARRITODETALLE (id, carrito_id, producto_id, cantidad, precio, subtotal)
VALUES
(1, 1, 1, 2, 95.50, 191.00),
(2, 1, 4, 1, 49.50, 49.50),
(3, 2, 5, 1, 150.00, 150.00),
(4, 3, 2, 1, 135.90, 135.90),
(5, 3, 3, 1, 50.00, 50.00),
(6, 4, 1, 1, 95.50, 95.50);

-- 6. Reseñas
INSERT INTO RESENA (id, producto_id, usuario_id, puntuacion, comentario, fecha, estado, respuestavendedor)
VALUES
(1, 1, 3, 5, 'Excelente fertilizante, noté el cambio en mis cultivos de maíz en pocos días.', NOW(), 'A', 'Gracias Juan, nos alegra saber que obtuviste buenos resultados.'),
(2, 4, 3, 4, 'Buen fungicida, aunque el envase podría ser más resistente.', NOW(), 'A', 'Gracias por tu sugerencia, mejoraremos el envase en próximas presentaciones.'),
(3, 5, 4, 5, 'El bioestimulante me ayudó a mejorar la floración. Producto 100% recomendable.', NOW(), 'A', 'Gracias María, este producto es ideal para etapas de floración y estrés.'),
(4, 2, 5, 4, 'Buen herbicida, elimina la maleza sin afectar mis cultivos.', NOW(), 'A', 'Gracias Carlos, recuerda aplicarlo en horas de baja radiación para mejores resultados.'),
(5, 3, 5, 5, 'Muy efectivo contra orugas, con poca dosis logré controlar toda la plaga.', NOW(), 'A', 'Excelente, Carlos. La Lambda-Cyhalotrina es ideal para control rápido y duradero.'),
(6, 1, 6, 5, 'La urea de esta tienda tiene muy buena pureza, mis hortalizas crecieron mucho mejor.', NOW(), 'A', 'Nos alegra mucho escuchar eso Lucía. ¡Gracias por confiar en AgroTienda Central!'),
(7, 6, 6, 5, 'Semillas de excelente germinación. Muy homogéneas y resistentes.', NOW(), 'A', 'Gracias Lucía, siempre trabajamos con semillas certificadas para garantizar calidad.');
INSERT INTO pasarelapago (id, nombre, apikey, urlbase, estadoregistro, descripcion, logo)
VALUES (
    1,
    'QR Payment',
    'API_KEY_QR_001',
    'https://demo-qr.com',
    'A',
    'Pasarela QR para Yape/Plin',
    'qr_logo.png'
);
INSERT INTO metodopago (id, nombre, soportaqr, pasarelapago_id, estadoregistro, descripcion)
VALUES (
    1,
    'Yape / Plin QR',
    1,
    1,
    'A',
    'Pago mediante QR con Yape o Plin'
);
INSERT INTO ESTADOGENERAL (id, nombre, tipo) VALUES
(2, 'PENDIENTE_PAGO', 'PEDIDO'),
(3, 'PAGADO', 'PEDIDO'),
(4, 'PROCESANDO', 'PEDIDO'),
(5, 'ENVIADO', 'PEDIDO'),
(6, 'EN_CAMINO', 'PEDIDO'),
(7, 'ENTREGADO', 'PEDIDO'),
(8, 'CANCELADO_CLIENTE', 'PEDIDO'),
(9, 'CANCELADO_VENDEDOR', 'PEDIDO'),
(10, 'CANCELADO_PAGO', 'PEDIDO'),
(11, 'REEMBOLSO_SOLICITADO', 'PEDIDO'),
(12, 'REEMBOLSADO', 'PEDIDO'),
(13, 'DEVOLUCION_SOLICITADA', 'PEDIDO'),
(14, 'DEVUELTO', 'PEDIDO');

INSERT INTO ESTADOGENERAL (id, nombre, tipo) VALUES
(15, 'PAGO_PENDIENTE', 'PAGO'),
(16, 'PAGO_APROBADO', 'PAGO'),
(17, 'PAGO_RECHAZADO', 'PAGO'),
(18, 'PAGO_REEMBOLSADO', 'PAGO');