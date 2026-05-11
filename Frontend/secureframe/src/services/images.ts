import { api } from './api'

export interface ImageAnalysisDetails {
  mime:      { valid: boolean; mime: string }
  exif:      { exif: Record<string, string>; gps: Record<string, string>; risks: string[] }
  eof:       { suspicious: boolean; extra_bytes?: number; reason?: string }
  histogram: { variance: number; suspicious: boolean }
  lsb:       { lsb_ratio: number; suspicious: boolean }
}

export interface ImageAnalysis {
  suspicious: boolean
  risks:      string[]
  details:    ImageAnalysisDetails
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

  // The backend already computes a human-readable risks array — use it directly
  if (analysis.risks.length > 0) return analysis.risks

  // Fallback: derive from details sub-fields
  const reasons: string[] = []
  if (!analysis.details.mime.valid)           reasons.push(`MIME inválido: ${analysis.details.mime.mime}`)
  if (analysis.details.exif.risks.length)     reasons.push(...analysis.details.exif.risks)
  if (analysis.details.eof.suspicious)        reasons.push(analysis.details.eof.reason ?? 'Marcador EOF sospechoso')
  if (analysis.details.histogram.suspicious)  reasons.push(`Histograma anómalo (varianza ${analysis.details.histogram.variance.toFixed(0)})`)
  if (analysis.details.lsb.suspicious)        reasons.push(`LSB anómalo (ratio ${analysis.details.lsb.lsb_ratio.toFixed(4)})`)

  return reasons.length ? reasons : ['Contenido sospechoso detectado']
}
