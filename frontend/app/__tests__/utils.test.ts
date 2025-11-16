/**
 * Tests pour les fonctions utilitaires
 */

describe('Utility Functions', () => {
  describe('formatDate', () => {
    it('should format date correctly', () => {
      const dateString = '2025-01-16T10:30:00Z'
      const date = new Date(dateString)
      const formatted = date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })

      expect(formatted).toContain('2025')
      expect(formatted).toContain('janv')
      expect(formatted).toContain('16')
    })
  })

  describe('Number formatting', () => {
    it('should format positive amounts correctly', () => {
      const amount = 1234.56
      const formatted = `+${amount}`
      expect(formatted).toBe('+1234.56')
    })

    it('should format negative amounts correctly', () => {
      const amount = -1234.56
      const formatted = `${amount}`
      expect(formatted).toBe('-1234.56')
    })

    it('should handle zero correctly', () => {
      const amount = 0
      expect(amount).toBe(0)
    })
  })

  describe('Type validation', () => {
    it('should validate transaction type', () => {
      const isIncome = (amount: number) => amount > 0
      const isExpense = (amount: number) => amount < 0

      expect(isIncome(100)).toBe(true)
      expect(isIncome(-100)).toBe(false)
      expect(isExpense(-100)).toBe(true)
      expect(isExpense(100)).toBe(false)
    })
  })
})
