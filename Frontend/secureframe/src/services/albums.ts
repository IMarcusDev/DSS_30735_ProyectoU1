import { api } from './api'

export interface Album {
  id: string
  name: string
  description: string
  is_public: boolean
  date_created: string
  state: 'Pendiente' | 'Aprobado' | 'Negado'
  image_count?: number
  author_name?: string
}

export interface PendingAlbum extends Album {
  owner: { id: string; name: string }
}

export const albumsService = {
  getPublic:  ()                 => api.get<Album[]>('/albums/public'),
  getById:    (id: string)       => api.get<Album>(`/albums/id/${id}`),
  getMine:    ()                 => api.get<Album[]>('/albums/'),
  getPending: ()                 => api.get<PendingAlbum[]>('/albums/pending'),

  create: (data: { name: string; description: string; is_public: boolean }) =>
    api.post<Album>('/albums/', data),

  approve: (id: string) =>
    api.patch<Album>(`/albums/id/${id}`, { state: 'Aprobado' }),

  reject: (id: string) =>
    api.patch<Album>(`/albums/id/${id}`, { state: 'Negado' }),
}
