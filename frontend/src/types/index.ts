export interface Usuario {
  id: number;
  nombre: string;
  email: string;
  rol?: 'anfitrion' | 'huesped';
}

export interface Propiedad {
  id?: number;
  titulo: string;
  direccion: string;
  ciudad: string;
  precio_noche: number;
  capacidad: number;
  imagen_url?: string;
  anfitrion_id?: number;
}

export interface Amenidad {
  id: number;
  nombre: string;
}

export interface Reserva {
  id: number;
  propiedad_id: number;
  usuario_id: number;
  fecha_inicio: string;
  fecha_fin: string;
  precio_total: number;
}