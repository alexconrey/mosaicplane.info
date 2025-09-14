import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import AircraftDetail from '@/views/AircraftDetail.vue'

// Mock axios for API calls
vi.mock('axios', () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ 
      data: {
        id: 1,
        model: 'Test Aircraft',
        manufacturer: { name: 'Test Manufacturer' },
        clean_stall_speed: 45,
        vs0_speed: 42,
        vx_speed: 65,
        vy_speed: 75,
        vg_speed: 70,
        vfe_speed: 85,
        vno_speed: 120,
        vne_speed: 150,
        maneuvering_speed: 95,
        cruise_speed: 110,
        top_speed: 140,
        max_takeoff_weight: 2400,
        seating_capacity: 4,
        certification_date: '1956-07-15',
        is_mosaic_compliant: true,
        sport_pilot_eligible: true,
        engines: []
      }
    }))
  }
}))

// Mock vue-router
vi.mock('vue-router', () => ({
  useRoute: () => ({
    params: { id: '1' }
  }),
  useRouter: () => ({
    push: vi.fn()
  })
}))

describe('AircraftDetail - Aircraft Information Section', () => {
  let wrapper

  const mockAircraft = {
    id: 1,
    model: 'Test Aircraft',
    manufacturer: { name: 'Test Manufacturer' },
    clean_stall_speed: 45,
    vs0_speed: 42,
    vx_speed: 65,
    vy_speed: 75,
    vg_speed: 70,
    vfe_speed: 85,
    vno_speed: 120,
    vne_speed: 150,
    maneuvering_speed: 95,
    cruise_speed: 110,
    top_speed: 140,
    max_takeoff_weight: 2400,
    seating_capacity: 4,
    certification_date: '1956-07-15',
    is_mosaic_compliant: true,
    sport_pilot_eligible: true,
    engines: []
  }

  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    if (wrapper) {
      wrapper.unmount()
    }
  })

  describe('MOSAIC Eligibility Summary', () => {
    it('displays MOSAIC eligibility badge for sport pilot eligible aircraft', async () => {
      wrapper = mount(AircraftDetail, {
        data() {
          return {
            aircraft: mockAircraft,
            loading: false
          }
        }
      })

      await wrapper.vm.$nextTick()

      const eligibilityBadge = wrapper.find('.eligibility-badge')
      expect(eligibilityBadge.exists()).toBe(true)
      expect(eligibilityBadge.classes()).toContain('sport-pilot-eligible')
      expect(eligibilityBadge.text()).toBe('Sport Pilot Eligible')
    })

    it('displays key specifications with enhanced typography', async () => {
      wrapper = mount(AircraftDetail, {
        data() {
          return {
            aircraft: mockAircraft,
            loading: false
          }
        }
      })

      await wrapper.vm.$nextTick()

      const keySpecs = wrapper.findAll('.key-spec')
      expect(keySpecs).toHaveLength(3)
      
      const stallSpec = keySpecs.find(spec => spec.text().includes('Stall:'))
      const mtowSpec = keySpecs.find(spec => spec.text().includes('MTOW:'))
      const seatsSpec = keySpecs.find(spec => spec.text().includes('Seats:'))

      expect(stallSpec.text()).toBe('Stall: 45kt')
      expect(mtowSpec.text()).toBe('MTOW: 2,400 lbs')
      expect(seatsSpec.text()).toBe('Seats: 4')
    })

    it('displays private pilot required badge for MOSAIC LSA aircraft', async () => {
      const privatePilotAircraft = { ...mockAircraft, clean_stall_speed: 60, sport_pilot_eligible: false }
      
      wrapper = mount(AircraftDetail, {
        data() {
          return {
            aircraft: privatePilotAircraft,
            loading: false
          }
        }
      })

      await wrapper.vm.$nextTick()

      const eligibilityBadge = wrapper.find('.eligibility-badge')
      expect(eligibilityBadge.classes()).toContain('private-pilot-required')
      expect(eligibilityBadge.text()).toBe('MOSAIC LSA (Private Pilot Required)')
    })

    it('displays not eligible badge for non-MOSAIC aircraft', async () => {
      const nonMosaicAircraft = { 
        ...mockAircraft, 
        clean_stall_speed: 65, 
        sport_pilot_eligible: false, 
        is_mosaic_compliant: false 
      }
      
      wrapper = mount(AircraftDetail, {
        data() {
          return {
            aircraft: nonMosaicAircraft,
            loading: false
          }
        }
      })

      await wrapper.vm.$nextTick()

      const eligibilityBadge = wrapper.find('.eligibility-badge')
      expect(eligibilityBadge.classes()).toContain('not-mosaic-eligible')
      expect(eligibilityBadge.text()).toBe('Not MOSAIC Eligible')
    })
  })

  describe('2x2 Grid Layout', () => {
    beforeEach(async () => {
      wrapper = mount(AircraftDetail, {
        data() {
          return {
            aircraft: mockAircraft,
            loading: false
          }
        }
      })
      await wrapper.vm.$nextTick()
    })

    it('renders aircraft information section with full-width layout', () => {
      const aircraftInfoSection = wrapper.find('.card.spec-card.full-width')
      expect(aircraftInfoSection.exists()).toBe(true)
      
      const sectionTitle = aircraftInfoSection.find('h3')
      expect(sectionTitle.text()).toBe('Aircraft Information')
    })

    it('displays 2x2 grid with four info sections', () => {
      const grid = wrapper.find('.aircraft-info-grid')
      expect(grid.exists()).toBe(true)

      const infoSections = wrapper.findAll('.info-section')
      expect(infoSections).toHaveLength(4)

      const sectionTitles = infoSections.map(section => 
        section.find('h4').text()
      )

      expect(sectionTitles).toEqual([
        'Flight Envelope',
        'Performance Speeds', 
        'Aircraft Limits',
        'Certification'
      ])
    })

    it('renders flight envelope section with critical speeds', () => {
      const flightEnvelopeSection = wrapper.findAll('.info-section')[0]
      const specRows = flightEnvelopeSection.findAll('.spec-row')
      
      expect(specRows.length).toBeGreaterThan(0)
      
      // Check for key flight envelope speeds
      const rowTexts = specRows.map(row => row.text())
      expect(rowTexts.some(text => text.includes('Clean Stall (Vs1)'))).toBe(true)
      expect(rowTexts.some(text => text.includes('45kt'))).toBe(true)
      expect(rowTexts.some(text => text.includes('Maneuvering (Va)'))).toBe(true)
      expect(rowTexts.some(text => text.includes('Never Exceed (Vne)'))).toBe(true)
    })

    it('renders performance speeds section with operational speeds', () => {
      const performanceSection = wrapper.findAll('.info-section')[1]
      const specRows = performanceSection.findAll('.spec-row')
      
      expect(specRows.length).toBeGreaterThan(0)
      
      const rowTexts = specRows.map(row => row.text())
      expect(rowTexts.some(text => text.includes('Best Angle Climb (Vx)'))).toBe(true)
      expect(rowTexts.some(text => text.includes('Best Rate Climb (Vy)'))).toBe(true)
      expect(rowTexts.some(text => text.includes('Best Glide (Vg)'))).toBe(true)
    })

    it('renders aircraft limits section with weight and seating', () => {
      const limitsSection = wrapper.findAll('.info-section')[2]
      const specRows = limitsSection.findAll('.spec-row')
      
      expect(specRows).toHaveLength(2)
      
      const rowTexts = specRows.map(row => row.text())
      expect(rowTexts.some(text => text.includes('Maximum Takeoff Weight'))).toBe(true)
      expect(rowTexts.some(text => text.includes('2,400 lbs'))).toBe(true)
      expect(rowTexts.some(text => text.includes('Seating Capacity'))).toBe(true)
      expect(rowTexts.some(text => text.includes('4 seats'))).toBe(true)
    })

    it('renders certification section with regulatory info', () => {
      const certificationSection = wrapper.findAll('.info-section')[3]
      const specRows = certificationSection.findAll('.spec-row')
      
      expect(specRows).toHaveLength(3)
      
      const rowTexts = specRows.map(row => row.text())
      expect(rowTexts.some(text => text.includes('Certification Date'))).toBe(true)
      expect(rowTexts.some(text => text.includes('MOSAIC Compliant'))).toBe(true)
      expect(rowTexts.some(text => text.includes('Sport Pilot Eligible'))).toBe(true)
    })
  })

  describe('EditableField Integration', () => {
    it('maintains EditableField components for user corrections', async () => {
      wrapper = mount(AircraftDetail, {
        data() {
          return {
            aircraft: mockAircraft,
            loading: false,
            editingField: null,
            editForm: {}
          }
        }
      })

      await wrapper.vm.$nextTick()

      // Check that EditableField components are present
      const editableFields = wrapper.findAll('[class*="inline-edit"]')
      expect(editableFields.length).toBeGreaterThan(0)
      
      // Verify critical speed fields have EditableField components
      const stallSpeedField = wrapper.find('[field-name="clean_stall_speed"]')
      expect(stallSpeedField.exists()).toBe(true)
      
      const takeoffWeightField = wrapper.find('[field-name="max_takeoff_weight"]')
      expect(takeoffWeightField.exists()).toBe(true)
    })
  })

  describe('Responsive Design', () => {
    it('applies correct CSS classes for grid layout', async () => {
      wrapper = mount(AircraftDetail, {
        data() {
          return {
            aircraft: mockAircraft,
            loading: false
          }
        }
      })

      await wrapper.vm.$nextTick()

      const grid = wrapper.find('.aircraft-info-grid')
      expect(grid.exists()).toBe(true)

      const infoSections = wrapper.findAll('.info-section')
      infoSections.forEach(section => {
        expect(section.exists()).toBe(true)
      })

      const specRows = wrapper.findAll('.spec-row')
      expect(specRows.length).toBeGreaterThan(0)
    })
  })

  describe('Helper Functions', () => {
    beforeEach(async () => {
      wrapper = mount(AircraftDetail, {
        data() {
          return {
            aircraft: mockAircraft,
            loading: false
          }
        }
      })
      await wrapper.vm.$nextTick()
    })

    it('correctly identifies sport pilot eligible aircraft', () => {
      const result = wrapper.vm.getMosaicEligibilityClass(mockAircraft)
      expect(result).toBe('sport-pilot-eligible')
      
      const text = wrapper.vm.getMosaicEligibilityText(mockAircraft)
      expect(text).toBe('Sport Pilot Eligible')
    })

    it('correctly identifies private pilot required aircraft', () => {
      const privatePilotAircraft = { ...mockAircraft, clean_stall_speed: 60 }
      
      const result = wrapper.vm.getMosaicEligibilityClass(privatePilotAircraft)
      expect(result).toBe('private-pilot-required')
      
      const text = wrapper.vm.getMosaicEligibilityText(privatePilotAircraft)
      expect(text).toBe('MOSAIC LSA (Private Pilot Required)')
    })

    it('correctly identifies non-MOSAIC eligible aircraft', () => {
      const nonMosaicAircraft = { ...mockAircraft, clean_stall_speed: 65 }
      
      const result = wrapper.vm.getMosaicEligibilityClass(nonMosaicAircraft)
      expect(result).toBe('not-mosaic-eligible')
      
      const text = wrapper.vm.getMosaicEligibilityText(nonMosaicAircraft)
      expect(text).toBe('Not MOSAIC Eligible')
    })

    it('provides correct stall speed notes', () => {
      expect(wrapper.vm.getStallSpeedNote(45)).toBe('Sport pilot eligible')
      expect(wrapper.vm.getStallSpeedNote(60)).toBe('Private pilot required')
      expect(wrapper.vm.getStallSpeedNote(65)).toBe('Exceeds MOSAIC limits')
    })
  })

  describe('Conditional V-Speed Display', () => {
    it('conditionally renders V-speed rows based on data availability', async () => {
      const aircraftWithLimitedData = {
        ...mockAircraft,
        vx_speed: null,
        vy_speed: null,
        vg_speed: null,
        vfe_speed: null
      }

      wrapper = mount(AircraftDetail, {
        data() {
          return {
            aircraft: aircraftWithLimitedData,
            loading: false
          }
        }
      })

      await wrapper.vm.$nextTick()

      const performanceSection = wrapper.findAll('.info-section')[1]
      const specRows = performanceSection.findAll('.spec-row')
      
      // Should only show cruise speed (which has data)
      expect(specRows.length).toBeLessThan(5)
      
      const rowTexts = specRows.map(row => row.text())
      expect(rowTexts.some(text => text.includes('Cruise Speed'))).toBe(true)
    })

    it('shows all V-speeds when data is complete', async () => {
      wrapper = mount(AircraftDetail, {
        data() {
          return {
            aircraft: mockAircraft,
            loading: false
          }
        }
      })

      await wrapper.vm.$nextTick()

      const performanceSection = wrapper.findAll('.info-section')[1]
      const specRows = performanceSection.findAll('.spec-row')
      
      expect(specRows.length).toBeGreaterThanOrEqual(5)
      
      const rowTexts = specRows.map(row => row.text())
      expect(rowTexts.some(text => text.includes('Best Angle Climb (Vx)'))).toBe(true)
      expect(rowTexts.some(text => text.includes('Best Rate Climb (Vy)'))).toBe(true)
      expect(rowTexts.some(text => text.includes('Best Glide (Vg)'))).toBe(true)
      expect(rowTexts.some(text => text.includes('Max Flaps Extended (Vfe)'))).toBe(true)
      expect(rowTexts.some(text => text.includes('Cruise Speed'))).toBe(true)
    })
  })
})