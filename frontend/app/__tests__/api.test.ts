/**
 * Tests pour la configuration API
 */
import api from '../api'

describe('API Configuration', () => {
  it('should have correct baseURL', () => {
    expect(api.defaults.baseURL).toBeDefined()
    expect(api.defaults.baseURL).toContain('/api/')
    expect(api.defaults.baseURL).toMatch(/\/api\/$/)
  })

  it('should use axios instance', () => {
    expect(api.get).toBeDefined()
    expect(api.post).toBeDefined()
    expect(api.put).toBeDefined()
    expect(api.delete).toBeDefined()
  })

  it('should have default baseURL when env var is not set', () => {
    const baseURL = api.defaults.baseURL
    expect(baseURL).toBe('http://localhost:8000/api/')
  })
})
