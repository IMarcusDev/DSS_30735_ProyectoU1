import { api } from './api'

export interface ImageAnalysis {
  mime_valid?:          boolean
  exif_suspicious?:     boolean
  eof_suspicious?:      boolean
  histogram_suspicious?: boolean
  lsb_suspicious?:      boolean
  [key: string]: unknown
}

export interface GalleryImage {
  image_id:            string
  image_name:          string
  image_size:          number
  image_path:          string
  image_mimetype:      string
  image_state:         'Limpio' | 'Sospechoso' | 'Positivo'
  image_date_uploaded: string
  image_analysis:      ImageAnalysis | null
}

export interface SuspiciousImage {
  image: GalleryImage
  owner: { id: string; name: string }
}

export const imagesService = {
  getByAlbum:    (albumId: string)  => api.get<GalleryImage[]>(`/images/album/${albumId}`),
  getSuspicious: ()                  => api.get<SuspiciousImage[]>('/images/suspicious'),

  upload: (albumId: string, file: File) => {
    const form = new FormData()
    form.append('file', file)
    return api.upload<GalleryImage>(`/images/?album_id=${albumId}`, form)
  },

  updateState: (imageId: string, state: 'Limpio' | 'Sospechoso' | 'Positivo') =>
    api.patch<GalleryImage>(`/images/id/${imageId}`, { state }),

  delete: (imageId: string) =>
    api.delete<void>(`/images/id/${imageId}`),
}

export function getAnalysisReasons(analysis: ImageAnalysis | null): string[] {
  if (!analysis) return []
  const reasons: string[] = []
  if (analysis.lsb_suspicious)       reasons.push('Anomalía LSB detectada')
  if (analysis.eof_suspicious)       reasons.push('Marcador EOF sospechoso')
  if (analysis.histogram_suspicious) reasons.push('Histograma de color anómalo')
  if (analysis.exif_suspicious)      reasons.push('Metadatos EXIF sospechosos')
  if (!analysis.mime_valid)          reasons.push('Tipo MIME inválido')
  return reasons.length ? reasons : ['Contenido sospechoso detectado']
}
