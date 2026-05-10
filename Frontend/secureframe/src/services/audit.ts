import { api } from './api'

export interface AuditEntry {
  audit_id:    string
  action:      'album_approved' | 'album_rejected' | 'image_approved' | 'image_deleted'
  target_type: 'album' | 'image'
  target_id:   string
  target_name: string
  timestamp:   string
}

export const auditService = {
  getMyLog(): Promise<AuditEntry[]> {
    return api.get<AuditEntry[]>('/audit/')
  },
}
