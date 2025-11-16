/**
 * Tests pour la configuration API
 */
import api from '../api'

describe('API Configuration', () => {
  it('should have correct baseURL', () => {
    expect(api.defaults.baseURL).toBeDefined()
    expect(api.defaults.baseURL).toContain('/api/')
  })

  it('should use axios instance', () => {
    expect(api.get).toBeDefined()
    expect(api.post).toBeDefined()
    expect(api.put).toBeDefined()
    expect(api.delete).toBeDefined()
  })
})
